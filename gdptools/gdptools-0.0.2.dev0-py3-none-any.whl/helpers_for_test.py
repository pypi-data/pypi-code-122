"""Helper functions for testing area-weighted aggragation."""
import logging
import time
from typing import Any
from typing import Optional

import geopandas as gpd
import pandas as pd
from pygeos import GEOSException
from pyproj import CRS
from shapely.geometry import box

from .helpers import _get_crs
from .helpers import _get_print_on
from .helpers import _get_shp_file
from .helpers import get_cells_poly
from .helpers import get_data_via_catalog

# from numba import jit

logger = logging.getLogger(__name__)


def _generate_weights_test(
    poly: gpd.GeoDataFrame,
    poly_idx: str,
    grid_cells: gpd.GeoDataFrame,
    grid_cells_crs: str,
    wght_gen_crs: str,
    filename: Optional[str] = None,
) -> pd.DataFrame:
    """Generate weights for aggragations of poly-to-poly mapping.

    Args:
        poly (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        grid_cells_crs (str): _description_
        wght_gen_crs (str): _description_
        filename (Optional[str], optional): _description_. Defaults to None.

    Returns:
        pd.DataFrame: _description_
    """
    # check if poly_idx in in poly
    if poly_idx not in poly.columns:
        print(f"Error: poly_idx ({poly_idx}) is not found in the poly ({poly.columns})")
        return

    grid_in_crs = _get_crs(grid_cells_crs)
    grid_out_crs = _get_crs(wght_gen_crs)

    start = time.perf_counter()
    grid_cells.set_crs(grid_in_crs, inplace=True)
    grid_cells.to_crs(grid_out_crs, inplace=True)
    if not poly.crs:
        print(f"polygons don't contain a valid crs: {poly.crs}")
        return False
    poly.to_crs(grid_out_crs, inplace=True)
    end = time.perf_counter()
    print(
        f"Reprojecting to epsg:{wght_gen_crs} finished in  {round(end-start, 2)} second(s)"
    )

    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    print(f"Spatial index generations finished in {round(end-start, 2)} second(s)")
    start = time.perf_counter()
    tcount = 0

    numrows = len(poly.index)
    print_on = _get_print_on(numrows)

    # in order, i_index, j_index, poly_index, weight values
    i_index = []
    j_index = []
    p_index = []
    wghts = []
    pm = []
    resint = []

    for index, row in poly.iterrows():
        count = 0
        hru_area = poly.loc[poly[poly_idx] == row[poly_idx]].geometry.area.sum()
        possible_matches_index = list(
            spatial_index.intersection(row["geometry"].bounds)
        )
        if not (len(possible_matches_index) == 0):
            possible_matches = grid_cells.iloc[possible_matches_index]
            precise_matches = possible_matches[
                possible_matches.intersects(row["geometry"])
            ]
            pm.append(precise_matches)
            if not (len(precise_matches) == 0):
                res_intersection = gpd.overlay(
                    poly.loc[[index]], precise_matches, how="intersection"
                )
                resint.append(res_intersection)
                for nindex, row in res_intersection.iterrows():

                    tmpfloat = float(res_intersection.area.iloc[nindex] / hru_area)
                    i_index.append(int(row["i_index"]))
                    j_index.append(int(row["j_index"]))
                    p_index.append(str(row[poly_idx]))
                    wghts.append(tmpfloat)
                    count += 1
                tcount += 1
                if tcount % print_on == 0:
                    print(tcount, index, flush=True)

        else:
            print("no intersection: ", index, str(row[poly_idx]), flush=True)

    wght_df = pd.DataFrame(
        {
            poly_idx: p_index,
            "i": i_index,
            "j": j_index,
            "wght": wghts,
        }
    )
    if filename:
        wght_df.to_csv(filename)
    end = time.perf_counter()
    logger.info(f"Weight generations finished in {round(end-start, 2)} second(s)")
    return wght_df, pm, res_intersection


def calc_weights_catalog_test(
    params_json: pd.DataFrame,
    grid_json: pd.DataFrame,
    shp_file: str,
    wght_gen_file: str,
    wght_gen_proj: Any,
) -> pd.DataFrame:
    """Calculate area-intersected weights of grid to feature.

    Args:
        params_json (pd.DataFrame): _description_
        grid_json (pd.DataFrame): _description_
        shp_file (str): _description_
        wght_gen_file (str): _description_
        wght_gen_proj (Any): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # ds_URL = params_json.URL.values[0]
    ds_proj = grid_json.proj.values[0]
    # only need one time step for generating weights so choose the first time from the param_cat
    date = params_json.duration.values[0].split("/")[0]

    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf, gdf_bounds = _get_shp_file(shp_file=shp_file, grid_json=grid_json)

    date = params_json.duration.values[0].split("/")[0]
    # get sub-setted xarray dataset
    ds_ss = get_data_via_catalog(
        params_json=params_json, grid_json=grid_json, bounds=gdf_bounds, begin_date=date
    )

    # get grid polygons to calculate intersection with polygon of interest - shp_file
    xname = grid_json.X_name.values[0]
    yname = grid_json.Y_name.values[0]
    var = params_json.variable.values[0]
    gdf_grid = get_cells_poly(ds_ss, x=xname, y=yname, var=var, crs_in=ds_proj)
    # gdf_grid = gpd.GeoDataFrame.from_features(gridpoly)

    # calculate the intersection weights and generate weight_file
    # assumption is that the first column in the shp_file is the id to use for
    # calculating weights
    apoly_idx = gdf.columns[0]
    wght_gen, pm, inter_sect = _generate_weights_test(
        poly=gdf,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        grid_cells_crs=grid_json.proj.values[0],
        filename=wght_gen_file,
        wght_gen_crs=wght_gen_proj,
    )

    return ds_ss, gdf_grid, pm, inter_sect, wght_gen
