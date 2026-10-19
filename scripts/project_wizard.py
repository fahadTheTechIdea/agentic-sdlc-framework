"""Interactive project decision wizard; Python 3.11+, no external packages."""
import argparse
import json
import logging
from pathlib import Path
import sys

from wizard_core import (ORIGINS, add_deliverable, answer_node, atomic_write, conflicts, load_catalog,
                         load_session, new_session, profile, questions, require,
                         safe_destination, save_session, summary, switch_profile)

ROOT = Path(__file__).resolve().parents[1]
LOG = logging.getLogger('sdlc.wizard')


def choose_profile(catalog):
    families = sorted({p['family'] for p in catalog['profiles']})
    print('Choose a project family:')
    for i, family in enumerate(families, 1):
        print(f'  {i}. {family}')
    family = input('Family number or name: ').strip()
    if family.isdigit() and 1 <= int(family) <= len(families):
        family = families[int(family) - 1]
    candidates = [p for p in catalog['profiles'] if p['family'] == family]
    require(bool(candidates), 'Unknown family; rerun profiles to see choices')
    for i, p in enumerate(candidates, 1):
        print(f"  {i}. {p['id']} — {p['framework']}")
    selected = input('Profile number or ID: ').strip()
    if selected.isdigit() and 1 <= int(selected) <= len(candidates):
        return candidates[int(selected) - 1]['id']
    require(any(p['id'] == selected for p in candidates), 'Unknown profile in selected family')
    return selected


def parse_input(raw, node):
    choices = node.get('choices', [])
    def selection(text):
        text = text.strip()
        if text.isdigit() and 1 <= int(text) <= len(choices):
            return choices[int(text) - 1]
        return text
    if node['type'] == 'multi':
        return [selection(x) for x in raw.split(',') if x.strip()]
    return selection(raw) if node['type'] == 'choice' else raw.strip()


def interactive(path, state, catalog, expected):
    print('Project decision wizard. Do not enter passwords, tokens or private personal data.')
    print('Each accepted answer is saved. :back :skip :review :quit :na REASON; custom text is allowed.')
    deferred, visited, forced = set(), [], None
    while True:
        active = {(did, n['id']): (did, n, a) for did, n, a in questions(state, catalog)}
        current = active.get(forced) if forced else None
        forced = None
        if current is None:
            current = next((x for key, x in active.items() if key not in deferred and
                            (not x[2] or x[2]['status'] in ('in_progress', 'needs_review'))), None)
        if current is None:
            print(summary(state, catalog))
            print('Session saved. Deferred decisions and external checks remain open; use run to resume or answer to edit.')
            return 0
        did, node, old = current
        print(f"\n[{did} / {node['id']}] {node['question']}")
        for i, option in enumerate(node.get('choices', []), 1):
            print(f'  {i}. {option}')
        if node['type'] == 'multi':
            print('Select multiple numbers or custom values separated by commas.')
        if old:
            print(f"Previous: {json.dumps(old['value'], ensure_ascii=False)} [{old['status']}]")
        raw = input('> ').strip()
        key = (did, node['id'])
        if raw == ':quit':
            print('Stopped. Previously accepted answers remain saved.')
            return 0
        if raw == ':review':
            print(summary(state, catalog))
            continue
        if raw == ':back':
            while visited:
                candidate = visited.pop()
                if candidate in active:
                    forced = candidate
                    break
            continue
        if raw.startswith(':') and raw != ':skip' and not raw.startswith(':na '):
            print('Unknown command; use :back, :skip, :review, :quit or :na REASON.')
            continue
        # Mutate a fresh copy: validation/save failures do not alter live session state.
        from copy import deepcopy
        candidate = deepcopy(state)
        try:
            na = raw.startswith(':na ')
            value = None if na or raw == ':skip' else parse_input(raw, node)
            answer_node(candidate, catalog, did, node['id'], value,
                        reason=raw[4:].strip() if na else ('Deferred by user' if raw == ':skip' else ''), na=na)
        except ValueError as exc:
            print(f'Answer not saved: {exc}')
            forced = key
            continue
        # Persistence errors terminate this run so the next invocation reloads state.
        expected = save_session(path, candidate, catalog, expected)
        state = candidate
        visited.append(key)
        if raw == ':skip':
            deferred.add(key)
        for issue in conflicts(state, catalog):
            print(f"Needs decision: {issue['reason']}")


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest='command', required=True)
    commands.add_parser('profiles', help='List implemented decision profiles; not qualified technology support')
    commands.add_parser('validate-catalog', help='Validate the versioned catalog')
    start = commands.add_parser('start', help='Preview a new session; --write saves it')
    start.add_argument('project', type=Path)
    start.add_argument('--name')
    start.add_argument('--mode', choices=('new', 'existing'), default='new')
    start.add_argument('--profile')
    start.add_argument('--state', type=Path)
    start.add_argument('--write', action='store_true')
    start.add_argument('--interactive', action='store_true')
    for name in ('run', 'show', 'questions', 'answer', 'add', 'profile', 'export'):
        sub = commands.add_parser(name)
        sub.add_argument('state', type=Path)
        if name == 'show':
            sub.add_argument('--json', action='store_true')
        if name == 'questions':
            sub.add_argument('--all', action='store_true', help='Include already resolved active questions')
            sub.add_argument('--next', action='store_true', help='Return only the first unresolved question')
        if name == 'answer':
            sub.add_argument('node')
            sub.add_argument('--deliverable', default='main')
            sub.add_argument('--value', help='JSON string, string array, or null (unknown)')
            sub.add_argument('--origin', choices=ORIGINS, default='user')
            sub.add_argument('--source', default='')
            sub.add_argument('--reason', default='')
            sub.add_argument('--na', action='store_true')
        if name in ('add', 'profile'):
            sub.add_argument('deliverable')
            sub.add_argument('--profile', required=True)
        if name == 'export':
            sub.add_argument('--output', type=Path)
            sub.add_argument('--write', action='store_true')
    return result


def main(argv=None):
    # Windows redirected pipes otherwise use a legacy encoding, breaking Unicode answers.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    args = parser().parse_args(argv)
    try:
        catalog = load_catalog(ROOT / 'wizard/catalog.json')
        if args.command == 'validate-catalog':
            print(f"Catalog valid: {len(catalog['profiles'])} decision profiles.")
            return 0
        if args.command == 'profiles':
            for p in catalog['profiles']:
                print(f"{p['id']} | {p['family']} | {p['framework']} | revision {p['revision']}")
            print('Decision trees only; versions, exports and external gates require actual evidence.')
            return 0
        if args.command == 'start':
            require(not args.interactive or args.write, '--interactive needs --write to save accepted answers')
            pid = args.profile or (choose_profile(catalog) if args.interactive else None)
            require(pid is not None, 'Choose --profile or use --interactive --write')
            profile(catalog, pid)
            state = new_session(catalog, args.project, args.name or args.project.resolve().name, args.mode, pid)
            if not args.write:
                print(summary(state, catalog))
                print('Preview only: no files written.')
                return 0
            path = args.state or args.project / '.sdlc/wizard.json'
            expected = save_session(path, state, catalog)
            print(f'Session created: {path}')
            return interactive(path, state, catalog, expected) if args.interactive else 0
        state, expected = load_session(args.state, catalog)
        if args.command == 'run':
            return interactive(args.state, state, catalog, expected)
        if args.command == 'show':
            print(json.dumps(state, indent=2, ensure_ascii=False) if args.json else summary(state, catalog))
            return 0
        if args.command == 'questions':
            selected = [{'deliverable': did, 'node': node, 'previous': old}
                        for did, node, old in questions(state, catalog)
                        if args.all or not old or old['status'] in ('in_progress', 'needs_review')]
            print(json.dumps({'questions': selected[:1] if args.next else selected,
                              'conflicts': conflicts(state, catalog),
                              'external_evidence': 'not_run'}, indent=2, ensure_ascii=False))
            return 0
        if args.command == 'export':
            body = summary(state, catalog)
            if not args.write:
                print(body)
                print('Preview only: no files written.')
                return 0
            require(args.output is not None, 'Export --write needs --output; existing artifacts are never overwritten')
            output = safe_destination(args.output)
            require(output.parent.is_dir(), 'Export output folder must exist')
            atomic_write(output, body.encode('utf-8'))
            print(f'Decision summary exported: {output}')
            return 0
        if args.command == 'answer':
            require(args.value is not None or args.na, 'Supply --value JSON or --na with a reason')
            value = json.loads(args.value) if args.value is not None else None
            answer_node(state, catalog, args.deliverable, args.node, value, args.origin, args.source, args.reason, args.na)
        elif args.command == 'add':
            add_deliverable(state, catalog, args.deliverable, args.profile)
        elif args.command == 'profile':
            switch_profile(state, catalog, args.deliverable, args.profile)
        save_session(args.state, state, catalog, expected)
        print('Saved. Dependent answers needing review and history are preserved.')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        # CLI owns diagnostics; never log submitted answer values or file contents.
        LOG.error('Wizard operation failed (%s): %s', type(exc).__name__, exc)
        print('No successful completion claimed. Inspect state and retry the failed operation.', file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print('\nStopped. Previously saved answers are preserved.', file=sys.stderr)
        return 130


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
    raise SystemExit(main())
