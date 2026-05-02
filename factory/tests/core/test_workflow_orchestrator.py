import importlib.util
import unittest
from pathlib import Path


def ensure_paths_module():
    paths_file = Path(".ai/scripts/paths.py").resolve()
    paths_file.parent.mkdir(parents=True, exist_ok=True)
    if not paths_file.exists():
        paths_file.write_text(
            "\n".join(
                [
                    "from pathlib import Path",
                    "REPO_ROOT = Path(__file__).resolve().parents[2]",
                    "def logs_dir(): return REPO_ROOT / '.ai' / 'logs'",
                    "def scripts_dir(): return REPO_ROOT / '.ai' / 'scripts'",
                    "def active_project(): return 'default'",
                    "def project_scraped_dir(): return REPO_ROOT / 'content' / active_project() / 'scraped'",
                    "def project_content_root(): return REPO_ROOT / 'content' / active_project()",
                ]
            ),
            encoding="utf-8",
        )


def load_module(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class TestWorkflowOrchestrator(unittest.TestCase):
    def setUp(self):
        ensure_paths_module()
        module_path = Path(".ai/scripts/core/workflow_orchestrator.py").resolve()
        self.mod = load_module(module_path, "workflow_orchestrator_test")

    def test_rejects_invalid_payload(self):
        result = self.mod.orchestrate({"intent": "sync"})
        self.assertEqual(result["status"], "invalid_payload")
        self.assertIn("primary_agent", result["blocked_reason"])

    def test_stage_marked_completed_only_on_success(self):
        in_memory_state = {
            "pipeline_state": {"stages_completed": []},
            "workspace_state": {"competitors_registered": 1},
        }

        self.mod.load_state = lambda: in_memory_state
        self.mod.save_state = lambda state: in_memory_state.update(state)
        self.mod.log_action = lambda *args, **kwargs: None
        self.mod.load_skill_map = lambda: {}

        context = self.mod.orchestrate(
            {
                "intent": "sync",
                "primary_agent": "scraper-agent",
                "status": "ready",
                "raw_command": "/sync",
                "sub_agents": [],
                "entities": {},
                "output_paths": [],
                "tool_execution": {},
            }
        )

        # Not completed at orchestration start.
        self.assertEqual(in_memory_state["pipeline_state"]["stages_completed"], [])

        self.mod.finalize(context, {"status": "failed", "details": {}, "errors": []})
        self.assertEqual(in_memory_state["pipeline_state"]["stages_completed"], [])

        self.mod.finalize(context, {"status": "success", "details": {}, "errors": []})
        self.assertIn("scrape", in_memory_state["pipeline_state"]["stages_completed"])


if __name__ == "__main__":
    unittest.main()
