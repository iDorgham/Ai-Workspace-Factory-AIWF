import pytest
from ..core import OpenClawOrchestration

@pytest.fixture
def claw():
    return OpenClawOrchestration()

def test_apply_stealth_config(claw):
    config = {}
    result = claw.apply_stealth_config(config)
    assert result["rate_limit"] == 5
    assert result["rotating_user_agents"] is True

def test_purify_html(claw):
    assert claw.purify_html("<html></html>") == "<html></html>"
