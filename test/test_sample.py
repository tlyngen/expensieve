import pytest


def test_method1():
    test_value = True
    require_value = True
    assert test_value == require_value,\
        f"test failed because: {test_value} != {require_value}"
    print(f"test passed because: {test_value} == {require_value}")
