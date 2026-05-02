import pytest
from ..core import SaaSPlatformsMastery

@pytest.fixture
def saas_mastery():
    return SaaSPlatformsMastery()

def test_audit_tenant_isolation(saas_mastery):
    assert saas_mastery.audit_tenant_isolation({"tenant_id": 1}) is True
    assert saas_mastery.audit_tenant_isolation({}) is False

def test_validate_webhooks(saas_mastery):
    urls = ["https://secure.com", "http://unsecure.com"]
    result = saas_mastery.validate_webhooks(urls)
    assert len(result) == 1
    assert "http://unsecure.com" in result
