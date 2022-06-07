"""kernal functions for poly-to-poly area-weighted mapping."""
import logging
from typing import Any

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

from gdptools.helpers import _generate_weights_pershp
from gdptools.helpers import _run_weights_catalog_pershp
from gdptools.helpers import get_cells_poly
from gdptools.helpers import get_data_via_catalog

logger = logging.getLogger(__name__)


def intersect_by_weighted_area(
    params_json: pd.DataFrame,
    grid_json: pd.DataFrame,
    gdf: gpd.GeoDataFrame,
    begin_date: str,
    end_date: str,
    wght_gen_proj: Any,
):
    """Calculate weighted-area-intersection between grid and shape.

    Args:
        params_json (pd.DataFrame): _description_
        grid_json (pd.DataFrame): _description_
        gdf (gpd.GeoDataFrame): _description_
        begin_date (str): _description_
        end_date (str): _description_
        wght_gen_proj (Any): _description_

    Returns:
        _type_: _description_
    """
    # ds_URL = params_json.URL.values[0]
    ds_proj = grid_json.proj.values[0]
    # only need one time step for generating weights so choose the first time from the param_cat
    date = params_json.duration.values[0].split("/")[0]

    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf.to_crs(grid_json.proj.values[0], inplace=True)
    bbox = box(*gdf.total_bounds)
    b_buf = max(grid_json.resX.values[0], grid_json.resY.values[0])
    geo_s_bounds = bbox.buffer(2 * b_buf).bounds
    # geo_s_bounds = gdf.total_bounds

    date = params_json.duration.values[0].split("/")[0]
    # get sub-setted xarray dataset
    ds_ss = get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=geo_s_bounds,
        begin_date=date,
    )
    # get grid polygons to calculate intersection with polygon of interest - shp_file
    xname = grid_json.X_name.values[0]
    yname = grid_json.Y_name.values[0]
    var = params_json.variable.values[0]
    gdf_grid = get_cells_poly(ds_ss, x=xname, y=yname, var=var, crs_in=ds_proj)
    # gdf_grid = gpd.GeoDataFrame.from_features(gridpoly, crs=ds_proj)

    # calculate the intersection weights and generate weight_file
    # assumption is that the first column in the shp_file is the id to use for
    # calculating weights
    apoly_idx = gdf.columns[0]
    wght_gen = _generate_weights_pershp(
        poly=gdf,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        wght_gen_crs=wght_gen_proj,
    )

    newgdf, vals = _run_weights_catalog_pershp(
        params_json=params_json,
        grid_json=grid_json,
        wght_file=wght_gen,
        shp=gdf,
        begin_date=begin_date,
        end_date=end_date,
    )
    return newgdf, vals
