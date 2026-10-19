"""Failure-oriented checks for governance records, adapter drift and safe adoption."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from adopt import install, plan
from sync_adapters import sync
from validate_framework import validate, validate_evidence, validate_raci


class FrameworkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "framework"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))

    def test_baseline_is_consistent(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_required_file_fails(self):
        (self.root / "core/EVIDENCE_POLICY.md").unlink()
        self.assertTrue(any("EVIDENCE_POLICY" in x for x in validate(self.root)))

    def test_broken_link_fails(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[missing](absent.md)\n")
        self.assertTrue(any("absent.md" in x for x in validate(self.root)))

    def test_link_escape_fails_even_when_file_exists(self):
        (self.base / "outside.md").write_text("outside", encoding="utf-8")
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[outside](../outside.md)\n")
        self.assertTrue(any("escaping link" in x for x in validate(self.root)))

    def test_encoded_link_and_code_example(self):
        (self.root / "with space.md").write_text("content", encoding="utf-8")
        with (self.root / "README.md").open("a", encoding="utf-8") as stream:
            stream.write("\n[space](with%20space.md)\n`[inline](absent.md)`\n```text\n[example](absent.md)\n```\n")
        self.assertEqual(validate(self.root), [])

    def test_version_drift_fails(self):
        (self.root / "VERSION").write_text("9.9.9\n", encoding="utf-8")
        self.assertTrue(any("VERSION" in x for x in validate(self.root)))

    def test_adapter_drift_is_detected_and_check_does_not_write(self):
        path = self.root / ".claude/skills/sdlc-orchestrator/SKILL.md"
        path.write_text("changed", encoding="utf-8")
        self.assertTrue(sync(self.root, check=True))
        self.assertEqual(path.read_text(), "changed")
        self.assertEqual(sync(self.root), [])
        self.assertEqual(sync(self.root, check=True), [])

    def test_unregistered_skill_fails(self):
        path = self.root / "skills/unknown/SKILL.md"
        path.parent.mkdir()
        path.write_text("---\nname: unknown\ndescription: Example\n---\n", encoding="utf-8")
        self.assertTrue(any("inventory" in x for x in validate(self.root)))

    def test_wrapper_symlink_parent_cannot_write_outside(self):
        external = self.base / "external"
        external.mkdir()
        wrapper_dir = self.root / ".claude/skills/sdlc-orchestrator"
        shutil.rmtree(wrapper_dir)
        try:
            wrapper_dir.symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest("OS account cannot create symlinks")
        self.assertTrue(any("symlink" in x for x in sync(self.root)))
        self.assertEqual(list(external.iterdir()), [])

    def test_manifest_path_escape_fails(self):
        path = self.root / "framework.json"
        data = json.loads(path.read_text())
        (self.base / "outside.md").write_text("outside", encoding="utf-8")
        data["required_files"].append("../outside.md")
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("outside root" in x for x in validate(self.root)))

    def test_invalid_manifest_shape_has_readable_error(self):
        (self.root / "framework.json").write_text("[]", encoding="utf-8")
        self.assertTrue(any("JSON object" in x for x in validate(self.root)))

    def test_cli_missing_optional_record_exits_nonzero(self):
        result = subprocess.run([sys.executable, str(self.root / "scripts/validate_framework.py"),
                                 "--evidence", str(self.base / "missing.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR: evidence:", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "record.json"
        self.data = {"framework_version": "1.2.0", "checks": [{
            "id": "CHECK-1", "claim": "Scoped check", "status": "verified",
            "revision": "a" * 40, "timestamp": "2026-10-19T10:00:00+03:00",
            "environment": "disposable fixture", "scope": "test fixture only",
            "command": "example check (fixture, not executed)", "exit_code": 0,
            "output": "output.txt", "limitations": ["Synthetic fixture, not real evidence."]}]}
        (self.root / "output.txt").write_text("synthetic fixture", encoding="utf-8")

    def evidence(self):
        self.path.write_text(json.dumps(self.data), encoding="utf-8")
        validate_evidence(self.path, "1.2.0")

    def test_executed_record_accepts_structural_contract(self):
        self.evidence()

    def test_evidence_commands_are_never_executed(self):
        marker = self.root / "must-not-exist.txt"
        self.data["checks"][0]["command"] = f'echo unsafe > "{marker}"'
        self.evidence()
        self.assertFalse(marker.exists())

    def test_pass_with_nonzero_exit_is_rejected(self):
        self.data["checks"][0]["exit_code"] = 1
        with self.assertRaisesRegex(ValueError, "disagree"):
            self.evidence()

    def test_failed_record_requires_nonzero_exit(self):
        self.data["checks"][0]["status"] = "failed"
        with self.assertRaisesRegex(ValueError, "disagree"):
            self.evidence()
        self.data["checks"][0]["exit_code"] = 2
        self.evidence()

    def test_boolean_exit_is_rejected(self):
        self.data["checks"][0]["exit_code"] = False
        with self.assertRaisesRegex(ValueError, "disagree"):
            self.evidence()

    def test_missing_output_is_rejected(self):
        self.data["checks"][0]["output"] = "absent.txt"
        with self.assertRaisesRegex(ValueError, "missing file"):
            self.evidence()

    def test_output_escape_is_rejected(self):
        self.data["checks"][0]["output"] = "../outside.txt"
        with self.assertRaisesRegex(ValueError, "outside root"):
            self.evidence()

    def test_unzoned_timestamp_is_rejected(self):
        self.data["checks"][0]["timestamp"] = "2026-10-19T10:00:00"
        with self.assertRaisesRegex(ValueError, "time zone"):
            self.evidence()

    def test_unverified_needs_reason(self):
        self.data["checks"][0] = {"id": "X", "claim": "Not run", "status": "not_run", "limitations": []}
        with self.assertRaisesRegex(ValueError, "limitations"):
            self.evidence()

    def test_duplicate_check_ids_are_rejected(self):
        self.data["checks"].append(copy.deepcopy(self.data["checks"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.evidence()

    def test_malformed_record_is_rejected(self):
        self.data["checks"] = [None]
        with self.assertRaisesRegex(ValueError, "object"):
            self.evidence()

    def test_raci_requires_one_non_agent_accountable_and_responsible(self):
        data = json.loads((ROOT / "templates/RACI.json").read_text())
        self.path.write_text(json.dumps(data), encoding="utf-8")
        validate_raci(self.path)
        for field, values, message in (("A", [], "exactly one"),
                                       ("A", ["builder"], "agent"),
                                       ("R", [], "responsible"),
                                       ("C", ["unknown"], "unregistered"),
                                       ("A", ["owner", "builder"], "exactly one")):
            with self.subTest(field=field, values=values):
                bad = copy.deepcopy(data)
                bad["assignments"][0][field] = values
                self.path.write_text(json.dumps(bad), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, message):
                    validate_raci(self.path)


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name)

    def test_preview_has_no_writes(self):
        planned = plan(ROOT, self.target, "codex")
        self.assertIn("AGENTS.md", planned)
        self.assertIn(".agents/skills/sdlc-orchestrator/SKILL.md", planned)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_preserves_existing_instructions_and_installs_valid_snapshot(self):
        existing = self.target / "AGENTS.md"
        existing.write_text("Project rules\n", encoding="utf-8")
        planned = plan(ROOT, self.target, "codex")
        self.assertNotIn("AGENTS.md", planned)
        install(self.target, planned)
        self.assertEqual(existing.read_text(), "Project rules\n")
        self.assertIn("sdlc-orchestrator", (self.target / ".agentic-framework/INTEGRATE.md").read_text())
        wrapper = (self.target / ".agents/skills/sdlc-orchestrator/SKILL.md").read_text()
        self.assertIn(".agentic-framework/skills/sdlc-orchestrator/SKILL.md", wrapper)
        self.assertEqual(validate(self.target / ".agentic-framework"), [])

    def test_all_adapters_install_and_validate(self):
        for adapter, instruction in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md"), ("generic", None)):
            with self.subTest(adapter=adapter):
                target = self.target / adapter
                target.mkdir()
                install(target, plan(ROOT, target, adapter))
                if instruction:
                    self.assertTrue((target / instruction).is_file())
                else:
                    self.assertFalse((target / "AGENTS.md").exists())
                self.assertEqual(validate(target / ".agentic-framework"), [])

    def test_collision_refuses_before_any_write(self):
        collision = self.target / ".agents/skills/sdlc-orchestrator/SKILL.md"
        collision.parent.mkdir(parents=True)
        collision.write_text("User skill", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "collision"):
            plan(ROOT, self.target, "codex")
        self.assertFalse((self.target / ".agentic-framework").exists())
        self.assertEqual(collision.read_text(), "User skill")

    def test_existing_installation_refused(self):
        (self.target / ".agentic-framework").mkdir()
        with self.assertRaisesRegex(ValueError, "existing framework"):
            plan(ROOT, self.target, "claude")

    def test_file_in_destination_parent_refused(self):
        (self.target / ".agents").write_text("user file", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsafe destination parent"):
            plan(ROOT, self.target, "codex")
        self.assertFalse((self.target / ".agentic-framework").exists())

    def test_source_or_descendant_target_refused(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            plan(ROOT, ROOT, "codex")

    def test_symlink_parent_refused(self):
        external = self.target / "external"
        external.mkdir()
        try:
            (self.target / ".agents").symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest("OS account cannot create symlinks")
        with self.assertRaisesRegex(ValueError, "unsafe destination parent"):
            plan(ROOT, self.target, "codex")
        self.assertEqual(list(external.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
