from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[2]
def logs_dir(): return REPO_ROOT / '.ai' / 'logs'
def scripts_dir(): return REPO_ROOT / '.ai' / 'scripts'
def active_project(): return 'default'
def project_scraped_dir(): return REPO_ROOT / 'content' / active_project() / 'scraped'
def project_content_root(): return REPO_ROOT / 'content' / active_project()