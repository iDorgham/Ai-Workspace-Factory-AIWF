import pytest
from ..core import ComputerUseMastery

@pytest.fixture
def computer_use():
    return ComputerUseMastery()

def test_calculate_precise_offset(computer_use):
    coords = (100, 200)
    window = (1920, 1080)
    assert computer_use.calculate_precise_offset(coords, window) == coords

def test_verify_ui_transition(computer_use):
    assert computer_use.verify_ui_transition("state1", "state2") is True
    assert computer_use.verify_ui_transition("state1", "state1") is False
