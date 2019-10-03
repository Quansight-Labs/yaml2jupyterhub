from yaml2jupyterhub.utils import flatten


def test_flatten():
    d = {"a": 1, "b": 2}
    expected = {"a": 1, "b": 2}
    result = flatten(d)
    assert result == expected


def test_flatten_nested():
    d = {"a": 1, "b": 2, "c": {"d": 3, "e": 4}}
    expected = {"a": 1, "b": 2, "c_d": 3, "c_e": 4}
    result = flatten(d)
    assert result == expected
