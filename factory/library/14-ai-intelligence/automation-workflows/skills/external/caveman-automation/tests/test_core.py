import pytest
import os
from ..core import CavemanAutomation

@pytest.fixture
def caveman():
    return CavemanAutomation()

def test_check_idempotency(caveman):
    assert caveman.check_idempotency("script.sh") is True

def test_validate_posix_compliance(caveman):
    assert caveman.validate_posix_compliance("script.sh") is True

def test_log_append(caveman, tmp_path):
    log_file = tmp_path / "test.log"
    caveman.log_append(str(log_file), "Test Entry")
    assert log_file.read_text().strip() == "Test Entry"
