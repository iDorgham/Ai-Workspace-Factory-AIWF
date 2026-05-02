import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace


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


class TestScraperEngineReliability(unittest.TestCase):
    def setUp(self):
        ensure_paths_module()
        module_path = Path(".ai/scripts/scraper/scraper_engine.py").resolve()
        self.mod = load_module(module_path, "scraper_engine_test")

    def test_projects_fallback_homepage_fetch_failure_does_not_crash(self):
        self.mod.detect_all_deltas = lambda scope: {"acme": {"base_url": "https://example.com"}}
        self.mod.build_delta_payload = lambda deltas: {
            "competitors": {"acme": {"new_urls": [], "updated_urls": [], "deleted_urls": []}},
            "total_new_urls": 0,
        }
        self.mod.fetch_url = lambda url, timeout=10: (None, 500)
        self.mod.log_sync_delta = lambda *args, **kwargs: None

        def fake_sync_module():
            return SimpleNamespace(write_sync_state=lambda *args, **kwargs: True)

        import sys

        sys.modules["sync_state_writer"] = fake_sync_module()
        result = self.mod.run_scrape(scope="projects")
        self.assertIn("acme", result["competitor_results"])
        self.assertEqual(result["competitor_results"]["acme"]["status"], "partial")

    def test_sync_state_write_failure_is_counted(self):
        self.mod.detect_all_deltas = lambda scope: {"acme": {"base_url": "https://example.com"}}
        self.mod.build_delta_payload = lambda deltas: {
            "competitors": {"acme": {"new_urls": ["https://example.com/blog/x"], "updated_urls": [], "deleted_urls": []}},
            "total_new_urls": 1,
        }
        self.mod.fetch_url = lambda url, timeout=10: ("<title>X</title><h1>X</h1>", 200)
        self.mod.sanitize_scraped_content = lambda html, url: {"clean_content": html}
        self.mod.save_scraped_content = lambda slug, content_type, parsed: ("/tmp/file.md", [], [])
        self.mod.log_sync_delta = lambda *args, **kwargs: None

        def fake_sync_module():
            return SimpleNamespace(write_sync_state=lambda *args, **kwargs: False)

        import sys

        sys.modules["sync_state_writer"] = fake_sync_module()
        result = self.mod.run_scrape(scope="all")
        self.assertGreaterEqual(result["total_errors"], 1)
        self.assertEqual(result["competitor_results"]["acme"]["status"], "partial")


if __name__ == "__main__":
    unittest.main()
