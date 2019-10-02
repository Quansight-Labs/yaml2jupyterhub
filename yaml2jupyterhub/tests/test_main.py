import pytest

from yaml2jupyterhub.main import flatten, load_config


def test_flatten():
    d = {"a": 1, "b": 2}
    expected = {"a": 1, "b": 2}
    result = flatten(d)
    assert result == expected


def test_flatten_nested():
    d = {"a": 1, "b": 2, "c": {"d": 3, "e": 4}}
    expected = {"a": 1, "b": 2, "c-d": 3, "c-e": 4}
    result = flatten(d)
    assert result == expected


def test_load_config_raises():
    with pytest.raises(ValueError, match="Could not find configuration file"):
        load_config("/this/path/does/not/exist.yaml")
