"""MCA projection module."""
from itertools import chain, repeat
from typing import Any, Optional, Tuple

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from saiph.models import Model
from saiph.reduction import DUMMIES_PREFIX_SEP
from saiph.reduction.utils.check_params import fit_check_params
from saiph.reduction.utils.common import (
    column_multiplication,
    diag,
    get_dummies_mapping,
    get_explained_variance,
    get_grouped_modality_values,
    get_modalities_types,
    get_projected_column_names,
    get_uniform_row_weights,
    row_division,
    row_multiplication,
)
from saiph.reduction.utils.svd import SVD


def fit(
    df: pd.DataFrame,
    nf: Optional[int] = None,
    col_weights: Optional[NDArray[np.float_]] = None,
) -> Model:
    """Fit a MCA model on data.

    Parameters:
        df: Data to project.
        nf: Number of components to keep. default: min(df.shape)
        col_weights: Weight assigned to each variable in the projection
            (more weight = more importance in the axes). default: np.ones(df.shape[1])

    Returns:
        model: The model for transforming new data.
    """
    nf = nf or min(pd.get_dummies(df).shape)

    _col_weights = col_weights if col_weights is not None else np.ones(df.shape[1])

    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    fit_check_params(nf, _col_weights, df)

    modalities_types = get_modalities_types(df)

    # initiate row and columns weights
    row_weights = get_uniform_row_weights(len(df))

    modality_numbers = []
    for column in df.columns:
        modality_numbers += [len(df[column].unique())]

    col_weights_dummies: NDArray[Any] = np.array(
        list(
            chain.from_iterable(
                repeat(i, j) for i, j in zip(_col_weights, modality_numbers)
            )
        )
    )

    df_scale, _modalities, r, c = center(df)
    df_scale, T, D_c = _diag_compute(df_scale, r, c)

    # get the array gathering proportion of each modality among individual (N/n)
    df_dummies = pd.get_dummies(df.astype("category"), prefix_sep=DUMMIES_PREFIX_SEP)
    dummies_col_prop = len(df_dummies) / df_dummies.sum(axis=0)

    # apply the weights and compute the svd
    Z = ((T * col_weights_dummies).T * row_weights).T
    U, s, V = SVD(Z)

    explained_var, explained_var_ratio = get_explained_variance(
        s, df_dummies.shape[0], nf
    )

    U = U[:, :nf]
    s = s[:nf]
    V = V[:nf, :]

    model = Model(
        original_dtypes=df.dtypes,
        original_categorical=df.columns.to_list(),
        original_continuous=[],
        dummy_categorical=df_dummies.columns.to_list(),
        U=U,
        V=V,
        explained_var=explained_var,
        explained_var_ratio=explained_var_ratio,
        variable_coord=pd.DataFrame(D_c @ V.T),
        _modalities=_modalities,
        D_c=D_c,
        type="mca",
        is_fitted=True,
        nf=nf,
        column_weights=col_weights_dummies,
        row_weights=row_weights,
        dummies_col_prop=dummies_col_prop,
        modalities_types=modalities_types,
    )

    return model


def fit_transform(
    df: pd.DataFrame,
    nf: Optional[int] = None,
    col_weights: Optional[NDArray[np.float_]] = None,
) -> Tuple[pd.DataFrame, Model]:
    """Fit a MCA model on data and return transformed data.

    Parameters:
        df: Data to project.
        nf: Number of components to keep. default: min(df.shape)
        col_weights: Weight assigned to each variable in the projection
            (more weight = more importance in the axes). default: np.ones(df.shape[1])

    Returns:
        model: The model for transforming new data.
        coord: The transformed data.
    """
    model = fit(df, nf, col_weights)
    coord = transform(df, model)
    return coord, model


def center(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, NDArray[Any], NDArray[Any], NDArray[Any]]:
    """Center data and compute modalities.

    Used as internal function during fit.

    **NB**: saiph.reduction.mca.scaler is better suited when a Model is already fitted.

    Parameters:
        df: DataFrame to center.

    Returns:
        df_centered: The centered DataFrame.
        _modalities: Modalities for the MCA
        row_sum: Sums line by line
        column_sum: Sums column by column
    """
    df_scale = pd.get_dummies(df.astype("category"), prefix_sep=DUMMIES_PREFIX_SEP)
    _modalities = df_scale.columns.values

    # scale data
    df_scale /= df_scale.sum().sum()

    row_sum = np.sum(df_scale, axis=1)
    column_sum = np.sum(df_scale, axis=0)
    return df_scale, _modalities, row_sum, column_sum


def scaler(model: Model, df: pd.DataFrame) -> pd.DataFrame:
    """Scale data using modalities from model.

    Parameters:
        model: Model computed by fit.
        df: DataFrame to scale.

    Returns:
        df_scaled: The scaled DataFrame.
    """
    df_scaled = pd.get_dummies(df.astype("category"), prefix_sep=DUMMIES_PREFIX_SEP)
    if model._modalities is not None:
        for mod in model._modalities:
            if mod not in df_scaled:
                df_scaled[mod] = 0
    df_scaled = df_scaled[model._modalities]

    # scale
    df_scaled /= df_scaled.sum().sum()
    df_scaled /= np.array(np.sum(df_scaled, axis=1))[:, None]
    return df_scaled


def _diag_compute(
    df_scale: pd.DataFrame, r: NDArray[Any], c: NDArray[Any]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Compute diagonal matrices and scale data."""
    eps: np.float_ = np.finfo(float).eps
    if df_scale.shape[0] >= 10000:
        D_r = diag(1 / (eps + np.sqrt(r)), use_scipy=True)
    else:
        D_r = diag(1 / (eps + np.sqrt(r)), use_scipy=False)
    D_c = diag(1 / (eps + np.sqrt(c)), use_scipy=False)

    T = D_r @ (df_scale - np.outer(r, c)) @ D_c
    return df_scale / np.array(r)[:, None], T, D_c


def transform(df: pd.DataFrame, model: Model) -> pd.DataFrame:
    """Scale and project into the fitted numerical space.

    Parameters:
        df: DataFrame to transform.
        model: Model computed by fit.

    Returns:
        coord: Coordinates of the dataframe in the fitted space.
    """
    df_scaled = scaler(model, df)
    coord = df_scaled @ model.D_c @ model.V.T
    coord.columns = get_projected_column_names(model.nf)
    return coord


def get_variable_contributions(
    model: Model, df: pd.DataFrame, explode: bool = False
) -> pd.DataFrame:
    """Compute the contributions of the `df` variables within the fitted space.

    Parameters:
        model: Model computed by fit.
        df: dataframe to compute contributions from
        explode: whether to split the contributions of each modality (True)
            or sum them as the contribution of the whole variable (False)

    Returns:
        contributions
    """
    if not model.is_fitted:
        raise ValueError(
            "Model has not been fitted. Call fit() to create a Model instance."
        )
    df = pd.get_dummies(df.astype("category"), prefix_sep=DUMMIES_PREFIX_SEP)

    centered_df = df / df.sum().sum()

    # Column and row weights
    col_sum = centered_df.sum(axis=0)
    row_sum = centered_df.sum(axis=1)
    scaled_df = row_division(centered_df, row_sum).T

    weighted_df = row_division(scaled_df, col_sum).T - 1

    weighted_df = column_multiplication(weighted_df, np.sqrt(col_sum))
    weighted_df = row_multiplication(weighted_df, np.sqrt(row_sum))

    min_nf = min(min(weighted_df.shape), model.nf)

    weighted_V, eig = _compute_svd(weighted_df, min_nf, col_sum)

    # computing the contribution
    coord_col = weighted_V**2
    coord_col = (coord_col * col_sum.values[:, np.newaxis]) / eig
    coord_col = coord_col * 100
    coordinates = pd.DataFrame(
        coord_col, columns=get_projected_column_names(min_nf), index=df.columns
    )

    if explode:
        return coordinates

    mapping = get_dummies_mapping(model.original_categorical, model.dummy_categorical)
    coordinates = get_grouped_modality_values(mapping, coordinates)

    return coordinates


def _compute_svd(
    weighted: pd.DataFrame, min_nf: int, col_sum: pd.DataFrame
) -> Tuple[pd.DataFrame, NDArray[np.float_]]:

    U, s, V = SVD(weighted.T, svd_flip=False)

    U = U[:, :min_nf]
    V = V.T[:, :min_nf]
    s = s[:min_nf]

    U, V = V, U
    eigenvalues = np.power(s, 2)

    sign = np.sign(np.sum(U))
    signed_V = column_multiplication(pd.DataFrame(V), sign)

    signed_V = row_division(signed_V, np.sqrt(col_sum).values)
    weighted_V = column_multiplication(signed_V, np.sqrt(eigenvalues)).values

    return weighted_V, eigenvalues


def stats(model: Model, df: pd.DataFrame, explode: bool = False) -> Model:
    """Compute the contributions.

    Parameters:
        model: Model computed by fit.
        df : dataframe to compute contributions from in the original space
        explode: whether to split the contributions of each modality (True)
            or sum them as the contribution of the whole variable (False)

    Returns:
        model.
    """
    contributions = get_variable_contributions(model, df, explode=explode)
    model.contributions = contributions
    return model
