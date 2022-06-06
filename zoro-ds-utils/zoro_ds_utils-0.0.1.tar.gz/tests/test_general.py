from typing import Any

import pytest

from zoro_ds_utils import general


def is_exception_type(value: Any) -> bool:
    """Returns True if `value` is a subclass of `Exception`, otherwise False."""
    try:
        # issubclass() throws a TypeError if `value` is not a class.
        if issubclass(value, Exception):
            return True
    except TypeError:
        pass

    return False


@pytest.mark.parametrize(
    "d, keys, default, expected",
    [
        ({}, ["foo"], None, None),  # KeyError
        ({"foo": 5}, ["foo"], None, 5),  # Success!
        ({"foo": 5}, ["foo", "bar"], None, None),  # TypeError
        ({"foo": 5}, ["foo"], -1, 5),  # Success  # Override default
        ({"foo": 5}, ["bar"], -1, -1),  # KeyError  # Override default
    ],
)
def test_safe_nested_get(d, keys, default, expected):
    assert general.safe_nested_get(d, keys, default) == expected


@pytest.mark.parametrize(
    "d, keys, value, expected",
    [
        ({}, ["foo"], "foovalue", {"foo": "foovalue"}),
        ({}, ["foo", "bar"], "barvalue", {"foo": {"bar": "barvalue"}}),
        (
            {"foo": "foovalue"},
            ["foo", "bar"],  # Can't replace existing str value with dict
            "barvalue",
            TypeError,
        ),
        (
            {"foo": {"value1": 3}},
            ["foo"],
            {"value2": 6},
            {"foo": {"value2": 6}},  # value1 was lost
        ),
    ],
)
def test_safe_nested_set(d, keys, value, expected):
    if not is_exception_type(expected):
        # General case: No exception thrown, check the function return value.
        general.safe_nested_set(d, keys, value)
        assert d == expected
    else:
        # Check for expected exception, e.g. TypeError
        with pytest.raises(expected):
            general.safe_nested_set(d, keys, value)


@pytest.mark.parametrize(
    "d, updates, expected",
    [
        ({}, {"foo": "foovalue"}, {"foo": "foovalue"}),
        (
            {"foo": {"value1": 3}},
            {"foo": {"value2": 6}},
            {"foo": {"value1": 3, "value2": 6}},  # Old key/values preserved
        ),
        (
            {"foo": {"value1": 3}},
            {"foo": {"value1": 4, "value2": 6}},
            {"foo": {"value1": 4, "value2": 6}},  # Update old, insert new
        ),
        (
            {"_zoro_mlops": {"first_attempt_start_date": "2020-05-10"}},
            {
                "MONITOR": {
                    "CPU": "1",
                    "ENV_VARS": {
                        "GOOGLE_PROJECT_BQ": "gcp-dw",
                        "RUN_ID": "2020.05.10.07.57.01-rc",
                        "STRATEGY_NAME": "similar_content",
                    },
                    "IMAGE": "gcr.io/zorodataplatform/ds-cc-product-recs:dev",
                    "MEMORY": "1G",
                    "RELEASE_TYPE": "dev",
                    "SCRIPT": "performance_monitoring.py",
                    "TIMEOUT": 1800,
                },
                "NOTIFICATIONS": {
                    "FAILURE": {"SLACK_IDS": ["G01J6646M16"]},
                    "SUCCESS": {"SLACK_IDS": ["G01J6646M16"]},
                },
                "RELEASE_TYPE": "dev",
            },
            {
                "_zoro_mlops": {"first_attempt_start_date": "2020-05-10"},
                "MONITOR": {
                    "CPU": "1",
                    "ENV_VARS": {
                        "GOOGLE_PROJECT_BQ": "gcp-dw",
                        "RUN_ID": "2020.05.10.07.57.01-rc",
                        "STRATEGY_NAME": "similar_content",
                    },
                    "IMAGE": "gcr.io/zorodataplatform/ds-cc-product-recs:dev",
                    "MEMORY": "1G",
                    "RELEASE_TYPE": "dev",
                    "SCRIPT": "performance_monitoring.py",
                    "TIMEOUT": 1800,
                },
                "NOTIFICATIONS": {
                    "FAILURE": {"SLACK_IDS": ["G01J6646M16"]},
                    "SUCCESS": {"SLACK_IDS": ["G01J6646M16"]},
                },
                "RELEASE_TYPE": "dev",
            },
        ),
    ],
)
def test_safe_nested_update(d, updates, expected):
    general.safe_nested_update(d, updates)
    assert d == expected
