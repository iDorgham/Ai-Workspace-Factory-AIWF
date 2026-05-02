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


class TestMemoryManagerGuards(unittest.TestCase):
    def setUp(self):
        ensure_paths_module()
        module_path = Path(".ai/scripts/core/memory_manager.py").resolve()
        self.mod = load_module(module_path, "memory_manager_test")

    def test_allows_scraped_index_file(self):
        self.assertFalse(
            self.mod.is_forbidden_path("content/demo/scraped/index.json")
        )

    def test_blocks_raw_scraped_content_paths(self):
        self.assertTrue(
            self.mod.is_forbidden_path("content/demo/scraped/acme/scraped/content/blog/a.md")
        )
        self.assertTrue(
            self.mod.is_forbidden_path("content/demo/scraped/acme/scraped/images/a.png")
        )


if __name__ == "__main__":
    unittest.main()
