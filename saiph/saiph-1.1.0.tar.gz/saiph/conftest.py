from typing import Any, Dict, List

import numpy as np
import pandas as pd
import pytest

from saiph.models import Model
from saiph.reduction import DUMMIES_PREFIX_SEP

_iris_csv = pd.read_csv("tests/fixtures/iris.csv")
_wbcd_csv = pd.read_csv("tests/fixtures/breast_cancer_wisconsin.csv")
_wbcd_supplemental_csv = pd.read_csv("tests/fixtures/wbcd_supplemental.csv")
_wbcd_supplemental_coordinates_csv = pd.read_csv(
    "tests/fixtures/wbcd_supplemental_coordinates.csv"
)


@pytest.fixture
def iris_df() -> pd.DataFrame:
    return _iris_csv.copy()


@pytest.fixture
def iris_quanti_df() -> pd.DataFrame:
    return _iris_csv.drop("variety", axis=1).copy()


@pytest.fixture()
def quanti_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "variable_1": [4, 5, 6, 7],
            "variable_2": [10, 20, 30, 40],
            "variable_3": [100, 50, -30, -50],
        }
    )


@pytest.fixture()
def quali_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "tool": ["wrench", "wrench", "hammer", "hammer"],
            "fruit": ["apple", "orange", "apple", "apple"],
        }
    )


@pytest.fixture
def mixed_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "variable_1": [4, 5, 6, 7],
            "tool": ["wrench", "wrench", "hammer", "hammer"],
        }
    )


@pytest.fixture
def mixed_df2() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "tool": ["toaster", "hammer"],
            "score": ["aa", "ab"],
            "size": [1.0, 4.0],
            "age": [55, 62],
        }
    )


@pytest.fixture
def wbcd_quali_df() -> pd.DataFrame:
    """Wisconsin breast cancer dataframe.

    Columns are categorical variables.
    """
    return _wbcd_csv.drop(columns=["Sample_code_number"]).astype("category").copy()


@pytest.fixture
def wbcd_supplemental_df() -> pd.DataFrame:
    """Supplemental synthetic individuals of the WBCD dataset."""
    return _wbcd_supplemental_csv.astype("category").copy()


@pytest.fixture
def wbcd_supplemental_coord() -> pd.DataFrame:
    """Synthetic coordinates of supplemental individuals of the WBCD dataset."""
    return _wbcd_supplemental_coordinates_csv.copy()


@pytest.fixture
def mapping() -> Dict[str, List[str]]:
    sep = DUMMIES_PREFIX_SEP
    return {
        "tool": [f"tool{sep}hammer", f"tool{sep}wrench"],
        "fruit": [f"fruit{sep}apple", f"fruit{sep}orange"],
    }


def check_model_equality(
    test: Model,
    expected: Model,
) -> None:
    """Verify that two Model instances are the same."""
    for key, value in expected.__dict__.items():
        test_item = test.__dict__[key]
        expected_item = value
        check_equality(test_item, expected_item)


def check_equality(
    test: Any,
    expected: Any,
) -> None:
    """Check equality of dataframes, series and np.arrays."""
    if isinstance(test, pd.DataFrame) and isinstance(expected, pd.DataFrame):
        pd.testing.assert_frame_equal(test, expected)
    elif isinstance(test, pd.Series) and isinstance(expected, pd.Series):
        pd.testing.assert_series_equal(test, expected)
    elif isinstance(test, np.ndarray) and isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(test, expected)
    else:
        assert test == expected
