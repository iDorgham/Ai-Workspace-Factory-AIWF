import pytest
from ..core import FineTuningMastery

@pytest.fixture
def ft_mastery():
    return FineTuningMastery()

def test_validate_jsonl_format(ft_mastery):
    valid_data = [{
        "messages": [
            {"role": "system", "content": "You are a bot"},
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello"}
        ]
    }]
    assert ft_mastery.validate_jsonl_format(valid_data) is True

def test_scrub_pii(ft_mastery):
    text = "Contact me at test@example.com or call +1 555-0199."
    scrubbed = ft_mastery.scrub_pii(text)
    assert "[EMAIL_REDACTED]" in scrubbed
    assert "[PHONE_REDACTED]" in scrubbed
