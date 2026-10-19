"""Behavior and failure-oriented tests for the real wizard engine and terminal CLI."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from wizard_core import (add_deliverable, answer_node, conflicts, digest, layer_statuses,
                         load_catalog, load_session, new_session, profile, questions,
                         save_session, summary, switch_profile, validate_session)


class WizardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT / 'wizard/catalog.json')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = new_session(self.catalog, self.root, 'Test project', 'new', 'dotnet.blazor.web')
        self.path = self.root / '.sdlc/wizard.json'

    def node(self, suffix, group='L02', pid='dotnet.blazor.web'):
        return f'{group}.{pid}.{suffix}'

    def answer(self, suffix, value, group='L02', **kwargs):
        return answer_node(self.state, self.catalog, 'main', self.node(suffix, group), value, **kwargs)

    def cli(self, *args, stdin=None):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/project_wizard.py'), *map(str, args)],
                              input=stdin, capture_output=True, text=True, encoding='utf-8', timeout=15)

    def bad_catalog(self, mutate):
        data = deepcopy(self.catalog)
        mutate(data)
        # Retain real framework root for blueprint validation; fail mutated data first.
        with patch('wizard_core.read_json', return_value=data):
            with self.assertRaises(ValueError):
                load_catalog(ROOT / 'wizard/catalog.json')

    def test_catalog_rejects_missing_layer_duplicate_binding_cycle_and_condition(self):
        self.bad_catalog(lambda d: d['profiles'][0]['roots'].pop('L07'))
        self.bad_catalog(lambda d: d['profiles'].append(deepcopy(d['profiles'][0])))
        self.bad_catalog(lambda d: d['profiles'][0]['nodes'][1].update(binding=d['profiles'][0]['nodes'][0]['binding']))
        self.bad_catalog(lambda d: d['profiles'][0]['nodes'][0].update(depends_on=[d['profiles'][0]['nodes'][2]['id']]))
        self.bad_catalog(lambda d: d['profiles'][0]['nodes'][5].update(when={'node': 'missing', 'equals': 'x'}))
        self.bad_catalog(lambda d: d['profiles'][0].update(conflicts=[{'node': 'missing'}]))
        self.bad_catalog(lambda d: d['profiles'][0].update(blueprint='../outside.md'))

    def test_profiles_have_distinct_questions_and_all_game_groups(self):
        self.assertEqual(len(self.catalog['profiles']), 19)
        blazor = profile(self.catalog, 'dotnet.blazor.web')
        django = profile(self.catalog, 'python.django.web')
        self.assertNotEqual(blazor['nodes'][4]['question'], django['nodes'][4]['question'])
        self.assertNotIn('webassembly', json.dumps(django).lower())
        for p in self.catalog['profiles']:
            self.assertTrue(set(f'L{i:02}' for i in range(1, 9)) <= set(p['roots']))
            if p['family'] == 'game':
                self.assertTrue(set(f'G{i:02}' for i in range(1, 10)) <= set(p['roots']))

    def test_conditional_branch_changes_and_hidden_answers_are_retained(self):
        branch = self.node('variant_web_app', 'L03')
        self.assertNotIn(branch, [n['id'] for _, n, _ in questions(self.state, self.catalog)])
        self.answer('variant', 'web_app')
        answer_node(self.state, self.catalog, 'main', branch, 'SSR with server interactivity')
        self.answer('variant', 'standalone_webassembly')
        self.assertEqual(self.state['deliverables']['main']['answers'][branch]['status'], 'needs_review')
        self.assertNotIn(branch, [n['id'] for _, n, _ in questions(self.state, self.catalog)])
        self.assertIn('preserved answer needs review', summary(self.state, self.catalog))
        with self.assertRaisesRegex(ValueError, 'not active'):
            answer_node(self.state, self.catalog, 'main', branch, 'must not accept hidden input')

    def test_transitive_invalidation_preserves_unrelated_answers(self):
        self.answer('variant', 'web_app')
        self.answer('persistence', 'hybrid', 'L04')
        self.answer('offline_sync', 'server authority', 'L04')
        self.answer('delivery', 'plan_only', 'L08')
        self.answer('variant', 'standalone_webassembly')
        answers = self.state['deliverables']['main']['answers']
        self.assertEqual(answers[self.node('offline_sync', 'L04')]['status'], 'needs_review')
        self.assertEqual(answers[self.node('delivery', 'L08')]['status'], 'resolved')
        self.assertTrue(any(x['action'] == 'answer_invalidated' for x in self.state['history']))

    def test_mixed_deliverables_and_profile_switch_keep_history(self):
        self.answer('variant', 'web_app')
        add_deliverable(self.state, self.catalog, 'api', 'java.spring.api')
        answer_node(self.state, self.catalog, 'api', 'L02.java.spring.api.variant', 'servlet')
        old_api = deepcopy(self.state['deliverables']['api'])
        switch_profile(self.state, self.catalog, 'main', 'python.django.web')
        self.assertEqual(self.state['deliverables']['api'], old_api)
        self.assertEqual(self.state['deliverables']['main']['answers'], {})
        history = self.state['history'][-1]
        self.assertEqual(history['previous']['profile'], 'dotnet.blazor.web')
        self.assertEqual(history['previous']['answers'][self.node('variant')]['value'], 'web_app')
        before = deepcopy(self.state)
        with self.assertRaisesRegex(ValueError, 'Unknown profile'):
            switch_profile(self.state, self.catalog, 'main', 'missing.stack')
        self.assertEqual(self.state, before)

    def test_answer_types_provenance_unknown_and_na(self):
        with self.assertRaises(ValueError):
            self.answer('variant', ['web_app'])
        with self.assertRaisesRegex(ValueError, 'source'):
            self.answer('variant', 'web_app', origin='observed')
        self.answer('variant', 'web_app', origin='observed', source='project.csproj:4')
        self.answer('versions', None, reason='Toolchain not inspected')
        self.assertEqual(self.state['deliverables']['main']['answers'][self.node('versions')]['status'], 'in_progress')
        with self.assertRaises(ValueError):
            self.answer('services', None, 'L06', na=True, reason='No reporting wanted')
        switch_profile(self.state, self.catalog, 'main', 'dotnet.worker')
        worker = 'L03.dotnet.worker.interface'
        with self.assertRaises(ValueError):
            answer_node(self.state, self.catalog, 'main', worker, None, na=True)
        answer_node(self.state, self.catalog, 'main', worker, None, na=True, reason='Headless; operator output in L06')
        self.assertEqual(self.state['deliverables']['main']['answers'][worker]['status'], 'not_applicable')

    def test_custom_and_unknown_answers_never_claim_qualified_support(self):
        self.answer('variant', 'custom reviewed variant')
        text = summary(self.state, self.catalog)
        self.assertIn('custom reviewed variant', text)
        self.assertIn('remain not_run', text)
        self.assertEqual(layer_statuses(self.state, self.catalog, 'main')['L02'], 'in_progress')

    def test_godot_csharp_web_conflict_and_language_switch(self):
        switch_profile(self.state, self.catalog, 'main', 'godot.csharp.game')
        answer_node(self.state, self.catalog, 'main', 'L01.godot.csharp.game.targets', ['web'])
        self.assertTrue(conflicts(self.state, self.catalog))
        self.assertEqual(layer_statuses(self.state, self.catalog, 'main')['L01'], 'blocked')
        switch_profile(self.state, self.catalog, 'main', 'godot.gdscript.game')
        self.assertEqual(conflicts(self.state, self.catalog), [])
        self.assertTrue(self.state['history'][-1]['previous']['answers'])

    def test_saved_resume_preserves_state_and_rejects_collision(self):
        self.answer('variant', 'web_app', origin='observed', source='actual-file:7')
        expected = save_session(self.path, self.state, self.catalog)
        resumed, baseline = load_session(self.path, self.catalog)
        self.assertEqual(resumed, self.state)
        self.assertEqual(baseline, expected)
        with self.assertRaises(ValueError):
            save_session(self.path, self.state, self.catalog)
        self.assertEqual(digest(self.path), expected)

    def test_stale_writer_lock_and_failed_replace_preserve_previous_save(self):
        first = save_session(self.path, self.state, self.catalog)
        self.answer('variant', 'web_app')
        latest = save_session(self.path, self.state, self.catalog, first)
        with self.assertRaisesRegex(ValueError, 'changed'):
            save_session(self.path, self.state, self.catalog, first)
        lock = self.path.with_name(self.path.name + '.lock')
        lock.write_text('another writer')
        with self.assertRaisesRegex(ValueError, 'locked'):
            save_session(self.path, self.state, self.catalog, latest)
        self.assertTrue(lock.exists())
        lock.unlink()
        with patch('wizard_core.os.replace', side_effect=OSError('simulated disk failure')):
            with self.assertRaises(OSError):
                save_session(self.path, self.state, self.catalog, latest)
        self.assertEqual(digest(self.path), latest)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_symlink_state_parent_refused(self):
        outside = self.root / 'outside'
        outside.mkdir()
        link = self.root / 'linked'
        try:
            link.symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('OS cannot create symlinks')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            save_session(link / 'state.json', self.state, self.catalog)
        self.assertEqual(list(outside.iterdir()), [])

    def test_malformed_state_and_duplicate_keys_fail_without_overwrite(self):
        save_session(self.path, self.state, self.catalog)
        body = self.path.read_bytes()
        bad = deepcopy(self.state)
        bad['schema_version'] = 2
        with self.assertRaises(ValueError):
            save_session(self.path, bad, self.catalog, digest(self.path))
        self.assertEqual(self.path.read_bytes(), body)
        for change in ({'profile_revision': 999}, {'answers': {'invented': {}}}):
            bad = deepcopy(self.state)
            bad['deliverables']['main'].update(change)
            with self.assertRaises(ValueError):
                validate_session(bad, self.catalog)
        self.path.write_text('{"schema_version":1,"schema_version":1}')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            load_session(self.path, self.catalog)

    def test_invalid_metadata_timestamp_history_and_boolean_schema_fail(self):
        for change in ({'schema_version': True}, {'created_at': '2026-10-19'},
                       {'inventory': {}}, {'history': [1]}):
            bad = deepcopy(self.state)
            bad.update(change)
            with self.assertRaises(ValueError):
                validate_session(bad, self.catalog)

    def test_interactive_family_selection_and_noninteractive_edits(self):
        result = self.cli('start', self.root, '--write', '--interactive', stdin='api\n1\n:quit\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsInstance(result.stdout, str)
        self.assertIn('Spring', result.stdout)
        self.assertEqual(load_session(self.path, self.catalog)[0]['deliverables']['main']['profile'], 'java.spring.api')
        result = self.cli('add', self.path, 'client', '--profile', 'dotnet.maui.mobile')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli('answer', self.path, 'L02.dotnet.maui.mobile.variant', '--deliverable', 'client', '--value', '"blazor_hybrid"')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli('show', self.path, '--json')
        self.assertEqual(json.loads(result.stdout)['deliverables']['client']['answers']['L02.dotnet.maui.mobile.variant']['value'], 'blazor_hybrid')
        output = self.root / 'new-decisions.md'
        result = self.cli('export', self.path, '--output', output, '--write')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('blazor_hybrid', output.read_text())

    def test_existing_inventory_is_path_only_and_preview_writes_nothing(self):
        (self.root / 'global.json').write_text('private config body must never appear')
        (self.root / 'secret.env').write_text('secret payload')
        result = self.cli('start', self.root, '--mode', 'existing', '--profile', 'dotnet.maui.mobile')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.path.exists())
        state = new_session(self.catalog, self.root, 'Existing', 'existing', 'dotnet.maui.mobile')
        self.assertEqual(state['inventory']['paths'], ['global.json'])
        self.assertNotIn('private config', json.dumps(state))
        self.assertNotIn('secret payload', json.dumps(state))

    def test_inventory_failure_is_reported_before_any_state_write(self):
        def unreadable(*args, **kwargs):
            kwargs['onerror'](PermissionError('unreadable fixture directory'))
        with patch('wizard_core.os.walk', side_effect=unreadable):
            with self.assertRaisesRegex(PermissionError, 'unreadable'):
                new_session(self.catalog, self.root, 'Existing', 'existing', 'dotnet.maui.mobile')
        self.assertFalse(self.path.exists())

    def test_interactive_back_defer_review_quit_and_resume(self):
        result = self.cli('start', self.root, '--profile', 'dotnet.blazor.web', '--write', '--interactive',
                          stdin='first purpose\n:back\nrevised purpose\n:skip\n:review\n:quit\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        state, _ = load_session(self.path, self.catalog)
        self.assertEqual(state['deliverables']['main']['answers'][self.node('intent', 'L01')]['value'], 'revised purpose')
        self.assertEqual(state['deliverables']['main']['answers'][self.node('targets', 'L01')]['value'], None)
        result = self.cli('run', self.path, stdin='browser\nweb_app\n:quit\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        state, _ = load_session(self.path, self.catalog)
        self.assertEqual(state['deliverables']['main']['answers'][self.node('variant')]['value'], 'web_app')

    def test_interrupted_input_preserves_accepted_answers(self):
        result = self.cli('start', self.root, '--profile', 'godot.gdscript.game', '--write', '--interactive', stdin='Puzzle prototype\n')
        self.assertEqual(result.returncode, 130)
        state, _ = load_session(self.path, self.catalog)
        self.assertEqual(len(state['deliverables']['main']['answers']), 1)

    def test_export_preview_no_overwrite_and_cli_invalid_input(self):
        save_session(self.path, self.state, self.catalog)
        output = self.root / 'existing-plan.md'
        output.write_text('user work')
        result = self.cli('export', self.path, '--output', output)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(output.read_text(), 'user work')
        result = self.cli('export', self.path, '--output', output, '--write')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(output.read_text(), 'user work')
        result = self.cli('answer', self.path, self.node('variant'), '--value', 'not JSON')
        self.assertEqual(result.returncode, 1)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(load_session(self.path, self.catalog)[0], self.state)

    def test_host_question_api_is_read_only_and_respects_conditional_visibility(self):
        self.answer('intent', 'Website fixture', 'L01')
        save_session(self.path, self.state, self.catalog)
        before = digest(self.path)
        result = self.cli('questions', self.path, '--next')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['questions'][0]['node']['id'], self.node('targets', 'L01'))
        self.assertIn('browser', data['questions'][0]['node']['choices'])
        result = self.cli('questions', self.path, '--all')
        ids = [x['node']['id'] for x in json.loads(result.stdout)['questions']]
        self.assertNotIn(self.node('variant_web_app', 'L03'), ids)
        self.assertEqual(digest(self.path), before)


if __name__ == '__main__':
    unittest.main()
