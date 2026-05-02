import pytest
from ..core import APIDesignMastery

@pytest.fixture
def api_mastery():
    return APIDesignMastery()

def test_lint_openapi_spec_fail(api_mastery):
    bad_spec = {
        "paths": {
            "/test": {
                "get": {"responses": {}}
            }
        }
    }
    violations = api_mastery.lint_openapi_spec(bad_spec)
    assert len(violations) > 0
    assert "Missing description" in violations[0]

def test_generate_mock_response(api_mastery):
    assert isinstance(api_mastery.generate_mock_response({}), dict)
