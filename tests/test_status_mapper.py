import pytest

from src.status_mapper import map_status


def test_map_pass_status():
    assert map_status("PASS") == 1


def test_map_fail_status_lowercase():
    assert map_status("fail") == 2


def test_map_blocked_status_with_spaces():
    assert map_status(" BLOCKED ") == 4


def test_invalid_status_raises_error():
    with pytest.raises(ValueError):
        map_status("DONE")