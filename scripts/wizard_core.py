"""Versioned decision catalog, session state and guarded persistence for the wizard."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

LAYERS = tuple(f'L{i:02}' for i in range(1, 9))
GAMES = tuple(f'G{i:02}' for i in range(1, 10))
ORIGINS = ('user', 'observed', 'recommendation', 'inferred')
STATES = ('resolved', 'in_progress', 'needs_review', 'not_applicable')
ID = re.compile(r'[a-z0-9][a-z0-9_.-]*\Z')


def stamp():
    return datetime.now(timezone.utc).isoformat()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def redirected(path):
    if path.is_symlink():
        return True
    # Path.is_junction arrived after our minimum Python 3.11; reject Windows
    # reparse destinations with the available stat attributes on older runtimes.
    return bool(os.name == 'nt' and path.exists() and
                path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def zoned_timestamp(value):
    require(isinstance(value, str), 'Timestamp must be text')
    try:
        parsed = datetime.fromisoformat(value)
        require(parsed.utcoffset() is not None, 'Timestamp needs a zone')
    except (TypeError, ValueError) as exc:
        raise ValueError('Invalid zoned timestamp') from exc


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    path = Path(path)
    require(path.stat().st_size <= 4 * 1024 * 1024, 'JSON file exceeds 4 MiB')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    def constant(value):
        raise ValueError(f'Nonstandard JSON constant refused: {value}')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=constant)


def load_catalog(path):
    data = read_json(path)
    require(isinstance(data, dict) and type(data.get('schema_version')) is int and data['schema_version'] == 1, 'Unsupported catalog schema')
    require(isinstance(data.get('profiles'), list) and data['profiles'], 'Catalog needs profiles')
    ids = set()
    for p in data['profiles']:
        require(isinstance(p, dict), 'Profile must be an object')
        pid = p.get('id')
        require(isinstance(pid, str) and ID.fullmatch(pid) and pid not in ids, 'Invalid/duplicate profile ID')
        ids.add(pid)
        require(type(p.get('revision')) is int and p['revision'] > 0, f'{pid}: invalid revision')
        for key in ('family', 'ecosystem', 'framework', 'blueprint'):
            require(nonempty(p.get(key)), f'{pid}: missing {key}')
        require(isinstance(p.get('nodes'), list) and p['nodes'], f'{pid}: missing nodes')
        groups = LAYERS + (GAMES if p['family'] == 'game' else ())
        require(isinstance(p.get('roots'), dict) and set(p['roots']) == set(groups), f'{pid}: incomplete layer roots')
        nodes, bindings = {}, set()
        for n in p['nodes']:
            require(isinstance(n, dict), f'{pid}: invalid node')
            nid = n.get('id')
            require(nonempty(nid) and nid not in nodes and nid.startswith(f"{n.get('group')}.{pid}."), f'{pid}: invalid/duplicate node ID')
            require(n.get('group') in groups and n.get('owner') in LAYERS, f'{nid}: invalid owner/group')
            require(nonempty(n.get('question')), f'{nid}: missing question')
            require(n.get('type') in ('text', 'choice', 'multi'), f'{nid}: invalid answer type')
            require(nonempty(n.get('binding')) and n['binding'] not in bindings, f'{nid}: conflicting output binding')
            bindings.add(n['binding'])
            require(type(n.get('allow_na')) is bool, f'{nid}: missing N/A policy')
            choices = n.get('choices', [])
            require(isinstance(choices, list) and all(nonempty(x) for x in choices) and len(choices) == len(set(choices)), f'{nid}: invalid choices')
            require(n['type'] == 'text' or bool(choices), f'{nid}: choices required')
            dependencies = n.get('depends_on')
            require(isinstance(dependencies, list) and all(nonempty(x) for x in dependencies) and len(dependencies) == len(set(dependencies)), f'{nid}: invalid dependencies')
            nodes[nid] = n
        for group, root in p['roots'].items():
            require(root in nodes and nodes[root]['group'] == group and 'when' not in nodes[root], f'{pid}: invalid root {group}')
        for nid, n in nodes.items():
            require(all(x in nodes and x != nid for x in n['depends_on']), f'{nid}: missing dependency')
            if 'when' in n:
                w = n['when']
                require(isinstance(w, dict) and set(w) == {'node', 'equals'} and w['node'] in n['depends_on'], f'{nid}: invalid condition')
                parent = nodes[w['node']]
                require(parent['type'] == 'choice' and w['equals'] in parent['choices'], f'{nid}: invalid conditional target')
        visiting, visited = set(), set()
        def visit(nid):
            require(nid not in visiting, f'{pid}: dependency cycle')
            if nid in visited:
                return
            visiting.add(nid)
            for dep in nodes[nid]['depends_on']:
                visit(dep)
            visiting.remove(nid)
            visited.add(nid)
        for nid in nodes:
            visit(nid)
        require(isinstance(p.get('conflicts'), list), f'{pid}: invalid conflict rules')
        for rule in p['conflicts']:
            require(isinstance(rule, dict) and nonempty(rule.get('node')) and rule['node'] in nodes,
                    f'{pid}: invalid conflict node')
            require(nodes[rule['node']]['type'] == 'multi' and nonempty(rule.get('contains')) and
                    nonempty(rule.get('reason')), f'{pid}: invalid conflict condition')
        blueprint = Path(p['blueprint'])
        framework = Path(path).resolve().parent.parent
        require(not blueprint.is_absolute() and '\\' not in p['blueprint'] and ':' not in p['blueprint'] and
                (framework / blueprint).resolve().is_relative_to(framework) and
                (framework / blueprint).is_file(), f'{pid}: missing/escaping blueprint')
    return data


def profile(catalog, pid):
    found = next((x for x in catalog['profiles'] if x['id'] == pid), None)
    require(found is not None, f'Unknown profile: {pid}; use profiles to list implemented decision trees')
    return found


def validate_value(node, value):
    if value is None:  # Explicitly unresolved; never a passing compatibility claim.
        return
    if node['type'] == 'multi':
        require(isinstance(value, list) and value and all(nonempty(x) for x in value), 'Expected a nonempty string array')
        require(len(value) == len(set(value)), 'Duplicate selections')
    else:
        require(nonempty(value), 'Expected nonempty text')
    # Choices permit explicit custom text; it remains a user choice, not qualified support.


def validate_session(state, catalog):
    require(isinstance(state, dict) and type(state.get('schema_version')) is int and state['schema_version'] == 1, 'Unsupported session schema')
    require(nonempty(state.get('name')) and nonempty(state.get('project_root')), 'Session needs project name/root')
    require(state.get('mode') in ('new', 'existing'), 'Invalid project mode')
    zoned_timestamp(state.get('created_at'))
    inv = state.get('inventory')
    require(isinstance(inv, dict) and isinstance(inv.get('paths'), list) and
            all(nonempty(x) for x in inv['paths']) and type(inv.get('truncated')) is bool and
            nonempty(inv.get('scope')), 'Invalid inventory')
    require(isinstance(state.get('history'), list), 'Missing history')
    for item in state['history']:
        require(isinstance(item, dict) and nonempty(item.get('action')), 'Invalid history event')
        zoned_timestamp(item.get('at'))
    require(isinstance(state.get('deliverables'), dict) and state['deliverables'], 'Missing deliverables')
    for did, d in state['deliverables'].items():
        require(isinstance(did, str) and ID.fullmatch(did) and isinstance(d, dict), 'Invalid deliverable ID')
        p = profile(catalog, d.get('profile'))
        require(type(d.get('profile_revision')) is int and d['profile_revision'] == p['revision'], f'{did}: profile revision changed; explicit migration required')
        require(isinstance(d.get('answers'), dict), 'Invalid answers')
        nodes = {n['id']: n for n in p['nodes']}
        for nid, answer in d['answers'].items():
            require(nid in nodes and isinstance(answer, dict), f'{did}: unknown answer node')
            require(answer.get('origin') in ORIGINS and answer.get('status') in STATES, f'{nid}: invalid provenance/status')
            for key in ('source', 'reason', 'updated_at'):
                require(isinstance(answer.get(key), str), f'{nid}: missing {key}')
            require('value' in answer, f'{nid}: missing value')
            validate_value(nodes[nid], answer['value'])
            validate_answer(nodes[nid], answer)
    return state


def validate_answer(node, answer):
    if answer['origin'] == 'observed':
        require(nonempty(answer['source']), 'Observed answers need a source locator')
    if answer['status'] == 'not_applicable':
        require(node['allow_na'] and nonempty(answer['reason']) and answer['value'] is None, 'N/A needs an allowed node, null value and reason')
    elif answer['status'] == 'resolved':
        require(answer['value'] is not None, 'Resolved answer cannot be unknown')
    elif answer['status'] == 'in_progress':
        require(answer['value'] is None, 'Deferred answer must remain unknown')
    zoned_timestamp(answer['updated_at'])


def inventory(root):
    """Bounded path-only observations; do not read configuration or secrets."""
    names = {'global.json', 'pyproject.toml', 'requirements.txt', 'package.json', 'Cargo.toml',
             'project.godot', 'pubspec.yaml', 'pom.xml', 'build.gradle', 'build.gradle.kts', 'framework.json'}
    skip = {'.git', 'node_modules', '.venv', 'venv', 'bin', 'obj', '.godot', 'Library', 'snapshots'}
    found, scanned = [], 0
    def report_error(error):
        raise error
    for parent, dirs, files in os.walk(root, followlinks=False, onerror=report_error):
        scanned += 1
        if scanned > 4000:
            return {'paths': found, 'truncated': True, 'scope': 'path-only; no version or stack inferred'}
        dirs[:] = sorted(d for d in dirs if d not in skip and not redirected(Path(parent, d)))
        for name in sorted(files):
            scanned += 1
            if scanned > 4000 or len(found) >= 100:
                return {'paths': found, 'truncated': True, 'scope': 'path-only; no version or stack inferred'}
            path = Path(parent, name)
            if (name in names or path.suffix in ('.csproj', '.sln', '.uproject')) and not path.is_symlink():
                found.append(path.relative_to(root).as_posix())
    return {'paths': found, 'truncated': False, 'scope': 'path-only; no version or stack inferred'}


def new_session(catalog, root, name, mode, pid):
    root = Path(root).resolve()
    require(root.is_dir(), 'Project folder must already exist')
    state = {'schema_version': 1, 'name': name, 'project_root': str(root), 'mode': mode,
             'created_at': stamp(), 'inventory': inventory(root) if mode == 'existing' else {'paths': [], 'truncated': False, 'scope': 'new project; no inventory'},
             'deliverables': {}, 'history': []}
    add_deliverable(state, catalog, 'main', pid)
    return validate_session(state, catalog)


def event(state, action, **details):
    state['history'].append({'at': stamp(), 'action': action, **deepcopy(details)})


def add_deliverable(state, catalog, did, pid):
    require(isinstance(did, str) and ID.fullmatch(did) and did not in state['deliverables'], 'Invalid/duplicate deliverable ID')
    p = profile(catalog, pid)
    state['deliverables'][did] = {'profile': pid, 'profile_revision': p['revision'], 'answers': {}}
    event(state, 'deliverable_added', deliverable=did, profile=pid)


def switch_profile(state, catalog, did, pid):
    require(did in state['deliverables'], 'Unknown deliverable')
    p = profile(catalog, pid)
    old = state['deliverables'][did]
    if old['profile'] == pid and old['profile_revision'] == p['revision']:
        return
    event(state, 'profile_changed', deliverable=did, previous=old, selected=pid)
    state['deliverables'][did] = {'profile': pid, 'profile_revision': p['revision'], 'answers': {}}


def visibility(node, answers):
    if 'when' not in node:
        return 'active'
    parent = answers.get(node['when']['node'])
    if not parent or parent['status'] not in ('resolved', 'not_applicable'):
        return 'pending'
    return 'active' if parent['value'] == node['when']['equals'] else 'hidden'


def answer_node(state, catalog, did, nid, value, origin='user', source='', reason='', na=False):
    require(did in state['deliverables'], 'Unknown deliverable')
    d = state['deliverables'][did]
    p = profile(catalog, d['profile'])
    nodes = {n['id']: n for n in p['nodes']}
    require(nid in nodes, 'Unknown node for selected profile')
    require(visibility(nodes[nid], d['answers']) == 'active', 'Conditional question is not active')
    answer = {'value': value, 'origin': origin, 'source': source, 'reason': reason,
              'status': 'not_applicable' if na else ('in_progress' if value is None else 'resolved'), 'updated_at': stamp()}
    require(origin in ORIGINS and isinstance(source, str) and isinstance(reason, str), 'Invalid answer provenance')
    validate_value(nodes[nid], value)
    validate_answer(nodes[nid], answer)
    old = d['answers'].get(nid)
    event(state, 'answer_changed', deliverable=did, node=nid, previous=old)
    d['answers'][nid] = answer
    changed = old is None or old['value'] != value or old['status'] != answer['status']
    if changed:
        affected, pending = set(), [nid]
        while pending:
            parent = pending.pop()
            for candidate in p['nodes']:
                cid = candidate['id']
                if parent in candidate['depends_on'] and cid not in affected:
                    affected.add(cid)
                    pending.append(cid)
        for cid in sorted(affected):
            if cid in d['answers']:
                event(state, 'answer_invalidated', deliverable=did, node=cid, previous=d['answers'][cid], cause=nid)
                d['answers'][cid]['status'] = 'needs_review'
                d['answers'][cid]['reason'] = f'Dependency changed: {nid}'
    return validate_session(state, catalog)


def conflicts(state, catalog):
    result = []
    for did, d in state['deliverables'].items():
        p = profile(catalog, d['profile'])
        for rule in p.get('conflicts', []):
            answer = d['answers'].get(rule['node'])
            if answer and answer['status'] == 'resolved' and rule['contains'] in answer['value']:
                result.append({'deliverable': did, 'node': rule['node'], 'reason': rule['reason']})
    return result


def questions(state, catalog):
    for did, d in state['deliverables'].items():
        for node in profile(catalog, d['profile'])['nodes']:
            if visibility(node, d['answers']) == 'active':
                yield did, node, d['answers'].get(node['id'])


def summary(state, catalog):
    lines = [f"# Project decisions: {state['name']}", '', f"Mode: {state['mode']}; project: {state['project_root']}", '',
             'Decision collection only. Technology compatibility, application checks and store gates remain not_run.', '']
    for did, d in state['deliverables'].items():
        p = profile(catalog, d['profile'])
        lines += [f"## {did}: {p['id']} (profile revision {p['revision']})", '', f"Blueprint: {p['blueprint']}", '']
        for group, status in layer_statuses(state, catalog, did).items():
            lines.append(f'- {group}: {status}')
        lines.append('')
        for n in p['nodes']:
            a = d['answers'].get(n['id'])
            visible = visibility(n, d['answers'])
            if visible != 'active':
                if a:
                    lines.append(f"- {n['id']}: {visible}; preserved answer needs review")
                continue
            status = a['status'] if a else 'not_started'
            value = json.dumps(a['value'], ensure_ascii=False) if a else 'unknown'
            lines.append(f"- {n['id']} [{status}]: {value}")
            if a:
                lines.append(f"  Origin: {a['origin']}; source: {a['source'] or 'unspecified'}; reason: {a['reason'] or 'none'}")
    issues = conflicts(state, catalog)
    lines += ['', '## Conflicts / external gates', '']
    lines += [f"- BLOCKED {x['deliverable']}: {x['reason']}" for x in issues]
    if not issues:
        lines.append('- No catalog conflict detected. This does not verify compatibility or support.')
    lines += ['- Verify official technology/standards sources and applicable store policy for the selected target.',
              '- Map these decisions into existing specification, SDD/ADR, tracker, service/assurance and verification records.',
              '- No application commands, dependencies, Git operations or store submissions were executed.', '']
    return '\n'.join(lines)


def layer_statuses(state, catalog, did):
    d = state['deliverables'][did]
    p = profile(catalog, d['profile'])
    blocked = {x['node'] for x in conflicts(state, catalog) if x['deliverable'] == did}
    result = {}
    for group in p['roots']:
        nodes = [n for n in p['nodes'] if n['group'] == group and visibility(n, d['answers']) != 'hidden']
        statuses = [d['answers'].get(n['id'], {}).get('status', 'not_started') for n in nodes]
        if any(n['id'] in blocked for n in nodes):
            result[group] = 'blocked'
        elif 'needs_review' in statuses:
            result[group] = 'needs_review'
        elif all(x == 'not_started' for x in statuses):
            result[group] = 'not_started'
        elif all(x == 'not_applicable' for x in statuses):
            result[group] = 'not_applicable'
        elif all(x in ('resolved', 'not_applicable') for x in statuses):
            result[group] = 'resolved'
        else:
            result[group] = 'in_progress'
    return result


def safe_destination(path):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        require(not redirected(part), 'Symlink/junction/reparse destination refused')
    return path


def save_session(path, state, catalog, expected=None):
    """Atomic state file; cooperative lock and digest detect competing wizard writes."""
    validate_session(state, catalog)
    body = (json.dumps(state, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    return atomic_write(path, body, expected)


def atomic_write(path, body, expected=None):
    """Guarded atomic file creation/replacement shared by sessions and exports."""
    path = safe_destination(path)
    require(len(body) <= 4 * 1024 * 1024, 'File exceeds 4 MiB; archive history before continuing')
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + '.lock')
    safe_destination(lock)
    try:
        lock_stream = lock.open('xb')
    except FileExistsError as exc:
        raise ValueError('Session is locked; inspect an interrupted or concurrent writer before retrying') from exc
    temporary = None
    try:
        with lock_stream:
            if expected is None:
                require(not path.exists(), 'Existing state refused; use resume commands')
            else:
                require(path.is_file() and digest(path) == expected, 'Session changed since load; reload before saving')
            descriptor, name = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp', dir=path.parent)
            temporary = Path(name)
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(body)
                stream.flush()
                os.fsync(stream.fileno())
            if expected is None:
                os.link(temporary, path)  # Exclusive install; never overwrite a collision.
            else:
                require(digest(path) == expected, 'Session changed during save; reload before saving')
                os.replace(temporary, path)
            return digest(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
        lock.unlink()


def load_session(path, catalog):
    path = safe_destination(path)
    require(path.stat().st_size <= 4 * 1024 * 1024, 'Session exceeds 4 MiB')
    raw = path.read_bytes()
    # Hash before/after parsing so a concurrent edit cannot be adopted as our baseline.
    result = validate_session(read_json(path), catalog)
    require(path.read_bytes() == raw, 'Session changed while loading; retry')
    return result, hashlib.sha256(raw).hexdigest()
