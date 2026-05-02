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
                    "def active_project(): return 'default'",
                    "def logs_dir(): return REPO_ROOT / '.ai' / 'logs'",
                    "def project_scraped_dir(): return REPO_ROOT / 'content' / active_project() / 'scraped'",
                    "def scripts_dir(): return REPO_ROOT / '.ai' / 'scripts'",
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


class TestCliRouter(unittest.TestCase):
    def setUp(self):
        ensure_paths_module()
        module_path = Path(".ai/scripts/core/cli_router.py").resolve()
        self.mod = load_module(module_path, "cli_router_test")

    def test_tool_execution_skips_when_router_unavailable(self):
        self.mod.TOOL_ROUTER_LOAD_ERROR = "import_failed"
        result = self.mod.build_tool_execution("/sync", "sync")
        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["reason"], "tool_router_unavailable")

    def test_non_accuracy_intent_skips_tool_execution(self):
        result = self.mod.build_tool_execution("/approve", "approve")
        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["reason"], "intent_not_accuracy_routed")

    def test_design_command_routes_with_default_list_action(self):
        result = self.mod.parse_command("/design")
        self.assertEqual(result["intent"], "design_catalog")
        self.assertEqual(result["entities"]["action"], "list")
        self.assertEqual(result["primary_agent"], "guide-agent")

    def test_design_command_extracts_selected_pack(self):
        result = self.mod.parse_command("/design use stripe")
        self.assertEqual(result["intent"], "design_catalog")
        self.assertEqual(result["entities"]["action"], "use")
        self.assertEqual(result["entities"]["design"], "stripe")


if __name__ == "__main__":
    unittest.main()
