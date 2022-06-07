"""Primary functions for poly-to-poly area-weighted mapping."""
import logging
import sys
import time
from typing import Any
from typing import Optional
from typing import Union

import geopandas as gpd
import netCDF4
import numpy as np
import pandas as pd
import xarray as xr
from pygeos import GEOSException
from pyproj import CRS
from shapely.geometry import box
from shapely.geometry import Polygon

# from numba import jit

logger = logging.getLogger(__name__)


def _get_print_on(numrows: int) -> int:
    """Return an interval to print progress of run_weights() function.

    Args:
        numrows (int): Number of rows: as in number of polygons

    Returns:
        int: Reasonable interval to print progress statements. Prints at about 10%
    """
    if numrows <= 10:
        print_on = 1
    elif numrows <= 100:
        print_on = 10
    elif numrows <= 1000:
        print_on = 100
    elif numrows <= 10000:
        print_on = 1000
    elif numrows <= 100000:
        print_on = 10000
    else:
        print_on = 50000
    return int(print_on)


def _get_crs(crs_in: Any) -> CRS:
    """Return pyproj.CRS given integer or string.

    Args:
        crs_in (Any): integer: epsg code or pyproj string

    Returns:
        CRS: pyproj.CRS
    """
    in_crs = CRS.from_user_input(crs_in)
    # if type(crs_in) == int:
    #     in_crs = CRS.from_epsg(crs_in)
    # elif type(crs_in) == str:
    #     in_crs = CRS.from_proj4(crs_in)
    return in_crs


def get_cells_poly_2d(
    xr_a: xr.Dataset, lon_str: str, lat_str: str, in_crs: Any
) -> gpd.GeoDataFrame:
    """Get cell polygons associated with 2d lat/lon coordinates.

    Args:
        xr_a (xr.Dataset): _description_
        lon_str (str): _description_
        lat_str (str): _description_
        in_crs (Any): _description_

    Returns:
        gpd.GeoDataFrame: _description_
    """
    lon = xr_a[lon_str]
    lat = xr_a[lat_str]
    count = 0
    poly = []
    lon_n = [
        lon[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jm1 = [
        lon[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jm1 = [
        lon[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1 = [
        lon[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jp1 = [
        lon[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jp1 = [
        lon[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jp1 = [
        lon[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1 = [
        lon[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jm1 = [
        lon[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]

    lat_n = [
        lat[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jm1 = [
        lat[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jm1 = [
        lat[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1 = [
        lat[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jp1 = [
        lat[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jp1 = [
        lat[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jp1 = [
        lat[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1 = [
        lat[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jm1 = [
        lat[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]

    # print(len(lon_n), len(lat_n), type(lon_n), np.shape(lon_n))
    numcells = len(lon_n)
    index = np.array(range(numcells))
    i_index = np.empty(numcells)
    j_index = np.empty(numcells)
    count = 0
    for i in range(1, lon.shape[0] - 1):
        for j in range(1, lon.shape[1] - 1):
            i_index[count] = i
            j_index[count] = j
            count += 1

    tpoly_1_lon = [
        [lon_n[i], lon_jm1[i], lon_ip1_jm1[i], lon_ip1[i]] for i in range(numcells)
    ]
    tpoly_1_lat = [
        [lat_n[i], lat_jm1[i], lat_ip1_jm1[i], lat_ip1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_1_lon), tpoly_1_lon[0])
    newp = [Polygon(zip(tpoly_1_lon[i], tpoly_1_lat[i])) for i in range(numcells)]
    p1 = [p.centroid for p in newp]
    # print(type(newp), newp[0], len(p1))

    tpoly_2_lon = [
        [lon_n[i], lon_ip1[i], lon_ip1_jp1[i], lon_jp1[i]] for i in range(numcells)
    ]
    tpoly_2_lat = [
        [lat_n[i], lat_ip1[i], lat_ip1_jp1[i], lat_jp1[i]] for i in range(numcells)
    ]
    print(len(tpoly_2_lon), tpoly_2_lon[0])
    newp = [Polygon(zip(tpoly_2_lon[i], tpoly_2_lat[i])) for i in range(numcells)]
    p2 = [p.centroid for p in newp]

    tpoly_3_lon = [
        [lon_n[i], lon_jp1[i], lon_im1_jp1[i], lon_im1[i]] for i in range(numcells)
    ]
    tpoly_3_lat = [
        [lat_n[i], lat_jp1[i], lat_im1_jp1[i], lat_im1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_3_lon[i], tpoly_3_lat[i])) for i in range(numcells)]
    p3 = [p.centroid for p in newp]

    tpoly_4_lon = [
        [lon_n[i], lon_im1[i], lon_im1_jm1[i], lon_jm1[i]] for i in range(numcells)
    ]
    tpoly_4_lat = [
        [lat_n[i], lat_im1[i], lat_im1_jm1[i], lat_jm1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_4_lon[i], tpoly_4_lat[i])) for i in range(numcells)]
    p4 = [p.centroid for p in newp]

    lon_point_list = [[p1[i].x, p2[i].x, p3[i].x, p4[i].x] for i in range(numcells)]
    lat_point_list = [[p1[i].y, p2[i].y, p3[i].y, p4[i].y] for i in range(numcells)]

    poly = [Polygon(zip(lon_point_list[i], lat_point_list[i])) for i in range(numcells)]

    df = pd.DataFrame({"i_index": i_index, "j_index": j_index})
    gmcells = gpd.GeoDataFrame(df, index=index, geometry=poly, crs=in_crs)
    # tpoly_1 = [Polygon(x) for x in newp]
    # p1 = tpoly_1.centroid
    return gmcells


def get_cells_poly(
    xr_a: xr.Dataset,
    x: str,
    y: str,
    var: str,
    crs_in: Any,
    verbose: Optional[bool] = False,
) -> gpd.GeoDataFrame:
    """Get cell polygons associated with "nodes" in xarray gridded data.

    Args:
        xr_a (xr.Dataset): _description_
        x (str): _description_
        y (str): _description_
        var (str): _description_
        crs_in (Any): _description_
        verbose (Optional[bool], optional): _description_. Defaults to False.

    Returns:
        gpd.GeoDataFrame: _description_
    """
    tlon = xr_a[x]
    tlat = xr_a[y]
    in_crs = _get_crs(crs_in)
    # if type(crs_in) == int:
    #     in_crs = CRS.from_epsg(crs_in)
    # elif type(crs_in) == str:
    #     in_crs = CRS.from_proj4(crs_in)

    # out_crs = _get_crs(4326)
    lon, lat = np.meshgrid(tlon, tlat)
    poly = []
    if verbose:
        logger.info("calculating surrounding cell vertices")
    start = time.perf_counter()
    lon_n = [
        lon[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jm1 = [
        lon[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jm1 = [
        lon[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1 = [
        lon[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_ip1_jp1 = [
        lon[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_jp1 = [
        lon[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jp1 = [
        lon[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1 = [
        lon[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]
    lon_im1_jm1 = [
        lon[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lon.shape[1] - 1)
    ]

    lat_n = [
        lat[i, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jm1 = [
        lat[i, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jm1 = [
        lat[i + 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1 = [
        lat[i + 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_ip1_jp1 = [
        lat[i + 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_jp1 = [
        lat[i, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jp1 = [
        lat[i - 1, j + 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1 = [
        lat[i - 1, j]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    lat_im1_jm1 = [
        lat[i - 1, j - 1]
        for i in range(1, lon.shape[0] - 1)
        for j in range(1, lat.shape[1] - 1)
    ]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating surrounding cell vertices in {round(end-start, 2)} second(s)"
        )

    # print(len(lon_n), len(lat_n), type(lon_n), np.shape(lon_n))
    numcells = len(lon_n)
    index = np.array(range(numcells))
    i_index = np.empty(numcells)
    j_index = np.empty(numcells)
    count = 0
    for i in range(1, lon.shape[0] - 1):
        for j in range(1, lon.shape[1] - 1):
            i_index[count] = i
            j_index[count] = j
            count += 1

    if verbose:
        logger.info("calculating cell 1 centroids")
    start = time.perf_counter()
    tpoly_1_lon = [
        [lon_n[i], lon_jm1[i], lon_ip1_jm1[i], lon_ip1[i]] for i in range(numcells)
    ]
    tpoly_1_lat = [
        [lat_n[i], lat_jm1[i], lat_ip1_jm1[i], lat_ip1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_1_lon), tpoly_1_lon[0])
    newp = [Polygon(zip(tpoly_1_lon[i], tpoly_1_lat[i])) for i in range(numcells)]
    p1 = [p.centroid for p in newp]
    # print(type(newp), newp[0], len(p1))
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 1 centroids in {round(end-start, 2)} second(s)"
        )
    del tpoly_1_lat, tpoly_1_lon

    if verbose:
        logger.info("calculating cell 2 centroids")
    start = time.perf_counter()
    tpoly_2_lon = [
        [lon_n[i], lon_ip1[i], lon_ip1_jp1[i], lon_jp1[i]] for i in range(numcells)
    ]
    tpoly_2_lat = [
        [lat_n[i], lat_ip1[i], lat_ip1_jp1[i], lat_jp1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_2_lon), tpoly_2_lon[0])
    newp = [Polygon(zip(tpoly_2_lon[i], tpoly_2_lat[i])) for i in range(numcells)]
    p2 = [p.centroid for p in newp]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 2 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_2_lat, tpoly_2_lon, newp

    if verbose:
        logger.info("calculating cell 3 centroids")
    start = time.perf_counter()
    tpoly_3_lon = [
        [lon_n[i], lon_jp1[i], lon_im1_jp1[i], lon_im1[i]] for i in range(numcells)
    ]
    tpoly_3_lat = [
        [lat_n[i], lat_jp1[i], lat_im1_jp1[i], lat_im1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_3_lon[i], tpoly_3_lat[i])) for i in range(numcells)]
    p3 = [p.centroid for p in newp]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 3 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_3_lat, tpoly_3_lon, newp

    if verbose:
        logger.info("calculating cell 4 centroids")
    start = time.perf_counter()
    tpoly_4_lon = [
        [lon_n[i], lon_im1[i], lon_im1_jm1[i], lon_jm1[i]] for i in range(numcells)
    ]
    tpoly_4_lat = [
        [lat_n[i], lat_im1[i], lat_im1_jm1[i], lat_jm1[i]] for i in range(numcells)
    ]
    # print(len(tpoly_3_lon), tpoly_3_lon[0])
    newp = [Polygon(zip(tpoly_4_lon[i], tpoly_4_lat[i])) for i in range(numcells)]
    p4 = [p.centroid for p in newp]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished calculating cell 4 centroids in {round(end-start, 2)} second(s)"
        )

    del tpoly_4_lat, tpoly_4_lon, newp
    del (
        lon_n,
        lon_jm1,
        lon_ip1_jm1,
        lon_ip1,
        lon_ip1_jp1,
        lon_jp1,
        lon_im1_jp1,
        lon_im1,
        lon_im1_jm1,
    )
    del (
        lat_n,
        lat_jm1,
        lat_ip1_jm1,
        lat_ip1,
        lat_ip1_jp1,
        lat_jp1,
        lat_im1_jp1,
        lat_im1,
        lat_im1_jm1,
    )

    if verbose:
        logger.info("creating bounding polygons")
    start = time.perf_counter()
    lon_point_list = [[p1[i].x, p2[i].x, p3[i].x, p4[i].x] for i in range(numcells)]
    lat_point_list = [[p1[i].y, p2[i].y, p3[i].y, p4[i].y] for i in range(numcells)]
    poly = [Polygon(zip(lon_point_list[i], lat_point_list[i])) for i in range(numcells)]
    end = time.perf_counter()
    if verbose:
        logger.info(
            f"finished creating bounding polygons in {round(end-start, 2)} second(s)"
        )

    if verbose:
        logger.info("reprojecting cells")
    start = time.perf_counter()
    # grd_shp = xr_a[var].values.shape
    df = pd.DataFrame({"i_index": i_index, "j_index": j_index})
    gmcells = gpd.GeoDataFrame(df, index=index, geometry=poly, crs=in_crs)
    # gmcells.to_crs(crs=out_crs, inplace=True)
    end = time.perf_counter()
    if verbose:
        logger.info(f"finished reprojecting cells in {round(end-start, 2)} second(s)")

    return gmcells


def generate_weights(
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

    for index, row in poly.iterrows():
        count = 0
        hru_area = poly.loc[poly[poly_idx] == row[poly_idx]].geometry.area.sum()
        possible_matches_index = list(
            spatial_index.intersection(row["geometry"].bounds)
        )
        if not (len(possible_matches_index) == 0):
            possible_matches = grid_cells.iloc[possible_matches_index]
            try:
                precise_matches = possible_matches[
                    possible_matches.intersects(row["geometry"])
                ]
            except GEOSException:
                print(f"error: index={index}, row={row}")
            if not (len(precise_matches) == 0):
                res_intersection = gpd.overlay(
                    poly.loc[[index]], precise_matches, how="intersection"
                )
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
    return wght_df


def _generate_weights_pershp(
    poly: gpd.GeoDataFrame,
    poly_idx: str,
    grid_cells: gpd.GeoDataFrame,
    wght_gen_crs: str,
) -> pd.DataFrame:
    """Generate weights for aggragations of poly-to-poly mapping.

    Args:
        poly (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        wght_gen_crs (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """
    # check if poly_idx in in poly
    if poly_idx not in poly.columns:
        logger.error(
            f"Error: poly_idx ({poly_idx}) is not found in the poly ({poly.columns})"
        )
        return

    grid_out_crs = _get_crs(wght_gen_crs)
    start = time.perf_counter()
    grid_cells.to_crs(grid_out_crs, inplace=True)

    if not poly.crs:
        raise ValueError(f"polygons don't contain a valid crs: {poly.crs}")

    poly.to_crs(grid_out_crs, inplace=True)
    end = time.perf_counter()
    logger.info(
        f"Reprojecting to epsg:{wght_gen_crs} finished in  {round(end-start, 2)} second(s)"
    )

    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    logger.info(
        f"Spatial index generations finished in {round(end-start, 2)} second(s)"
    )
    start = time.perf_counter()
    tcount = 0

    numrows = len(poly.index)
    print_on = _get_print_on(numrows)

    # in order, i_index, j_index, poly_index, weight values
    i_index = []
    j_index = []
    p_index = []
    wghts = []

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
            if not (len(precise_matches) == 0):
                res_intersection = gpd.overlay(
                    poly.loc[[index]], precise_matches, how="intersection"
                )
                for nindex, nrow in res_intersection.iterrows():

                    tmpfloat = float(res_intersection.area.iloc[nindex] / hru_area)
                    i_index.append(int(nrow["i_index"]))
                    j_index.append(int(nrow["j_index"]))
                    p_index.append(str(nrow[poly_idx]))
                    wghts.append(tmpfloat)
                    count += 1
                tcount += 1
                if tcount % print_on == 0:
                    logger.info(index, flush=True)

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
    wght_df = wght_df.astype({"i": int, "j": int, "wght": float, poly_idx: str})
    end = time.perf_counter()
    logger.info(f"Weight generations finished in {round(end-start, 2)} second(s)")
    return wght_df


def getaverage(data: np.ndarray, wghts: np.ndarray) -> float:
    """Get average of array (data) using weights (wghts).

    Args:
        data (np.ndarray): _description_
        wghts (np.ndarray): _description_

    Returns:
        float: _description_
    """
    try:
        v_ave = np.average(data, weights=wghts)
    except ZeroDivisionError:
        print("zero division error")
        v_ave = netCDF4.default_fillvals["f8"]
    return v_ave


def getaverage_wtime(data: np.ndarray, wghts: np.ndarray) -> float:
    """Get average of array (data) using weights (wghts).

    Args:
        data (np.ndarray): _description_
        wghts (np.ndarray): _description_

    Returns:
        float: _description_
    """
    try:
        v_ave = np.average(data, weights=wghts, axis=1)
    except ZeroDivisionError:
        print("zero division error")
        v_ave = netCDF4.default_fillvals["f8"]
    return v_ave


def np_get_wval(ndata: np.ndarray, wghts: np.ndarray) -> float:
    """Get masked average.

    Args:
        ndata (np.ndarray): _description_
        wghts (np.ndarray): _description_

    Returns:
        float: _description_
    """
    mdata = np.ma.masked_array(ndata, np.isnan(ndata))
    tmp = np.ma.average(mdata, weights=wghts)

    # if tmp is np.ma.masked:
    #     # if verbose:
    #     #     print(f"returning masked value: {hru_id}", ndata)
    #     # return netCDF4.default_fillvals['f8']
    #     return tmp

    # else:
    return tmp


def np_get_wval_wtime(ndata: np.ndarray, wghts: np.ndarray) -> float:
    """Get masked average.

    Args:
        ndata (np.ndarray): _description_
        wghts (np.ndarray): _description_

    Returns:
        float: _description_
    """
    mdata = np.ma.masked_array(ndata, np.isnan(ndata))
    tmp = np.ma.average(mdata, weights=wghts, axis=1)

    # if tmp is np.ma.masked:
    #     # if verbose:
    #     #     print(f"returning masked value: {hru_id}", ndata)
    #     # return netCDF4.default_fillvals['f8']
    #     return tmp

    # else:
    return tmp


def run_weights(
    var: str,
    time: str,
    ds: xr.Dataset,
    wght_file: Union[str, pd.DataFrame],
    shp: gpd.GeoDataFrame,
    geom_id: str,
) -> Union[gpd.GeoDataFrame, np.ndarray]:
    """Run aggregation mapping ds to shp.

    Args:
        var (str): _description_
        time (str): _description_
        ds (xr.Dataset): _description_
        wght_file (Union[str, pd.DataFrame]): _description_
        shp (gpd.GeoDataFrame): _description_
        geom_id (str): _description_

    Returns:
        Union[gpd.GeoDataFrame, np.ndarray]: _description_
    """
    wghts = _get_wieght_df(wght_file, geom_id)

    gdf = shp
    # gdf.reset_index(drop=True, inplace=True)
    # gdf1 = gdf.sort_values(geom_id).dissolve(by=geom_id)
    gdf1 = gdf.dissolve(by=geom_id)

    geo_index = np.asarray(gdf1.index, dtype=type(gdf1.index.values[0]))
    n_geo = len(geo_index)

    print_on = _get_print_on(n_geo)
    unique_geom_ids = wghts.groupby(geom_id)
    ds_vars = [i for i in ds.data_vars]
    # if var not in ds_vars:
    #     raise KeyError(f"var: {var} not in ds vars: {ds_vars}")
    #     return None, None

    nts = len(ds.coords[time].values)
    try:
        native_dtype = ds[var].values.dtype
    except KeyError:
        print(f"var: {var} not in ds vars: {ds_vars}")
        return None, None
    val_interp = np.empty((n_geo, nts), dtype=native_dtype)
    var_vals = ds[var].values

    # for t in np.arange(nts):
    #     # val_flat_interp = (
    #     #     ds[var].values[t, 1 : grd_shp[1] - 1, 1 : grd_shp[2] - 1].flatten()
    #     # )
    print(f"processing time for var: {var}")
    for i in np.arange(len(geo_index)):
        weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
        tw = weight_id_rows.wght.values
        i_ind = np.array(weight_id_rows.i.values)
        j_ind = np.array(weight_id_rows.j.values)

        vals = var_vals[:, i_ind, j_ind]

        # tgid = weight_id_rows.grid_ids.values
        # tmp = getaverage(val_flat_interp[tgid], tw)
        tmp = getaverage_wtime(vals, tw)
        try:
            if np.isnan(tmp).any():
                # val_interp[t, i] = np_get_wval(
                #     val_flat_interp[tgid], tw, geo_index[i]
                # )
                val_interp[i, :] = np_get_wval_wtime(vals, tw)
            else:
                val_interp[i, :] = tmp
        except KeyError:
            val_interp[i, :] = netCDF4.default_fillvals["f8"]

        if i % print_on == 0:
            print(f"    Processing {var} for feature {geo_index[i]}", flush=True)

    # print(val_interp)
    return gdf1, val_interp


def build_subset(
    param_json: pd.DataFrame,
    grid_json: pd.DataFrame,
    bounds: np.ndarray,
    date_min: str,
    date_max: Optional[str] = None,
) -> dict:
    """Create a dictionary to use with xarray .sel() method to subset by time and space.

    Args:
        param_json (pd.DataFrame): _description_
        grid_json (pd.DataFrame): _description_
        bounds (np.ndarray): _description_
        date_min (str): _description_
        date_max (str, optional): _description_. Defaults to None.

    Returns:
        dict: _description_
    """
    xname = grid_json.X_name.values[0]
    yname = grid_json.Y_name.values[0]
    # print(type(xname), type(yname))
    tname = param_json.T_name.values[0]
    minx = bounds[0]
    maxx = bounds[2]
    miny = bounds[1]
    maxy = bounds[3]
    gridorder = bool(int(grid_json.toptobottom.values[0]))
    ss_dict = {}
    if not gridorder:
        if date_max is None:
            ss_dict = {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: date_min,
            }
        else:
            ss_dict = {
                xname: slice(minx, maxx),
                yname: slice(maxy, miny),
                tname: slice(date_min, date_max),
            }
    else:
        if date_max is None:
            ss_dict = {
                xname: slice(minx, maxx),
                yname: slice(miny, maxy),
                tname: date_min,
            }
        else:
            ss_dict = {
                xname: slice(minx, maxx),
                yname: slice(miny, maxy),
                tname: slice(date_min, date_max),
            }
    return ss_dict


def _get_shp_file(
    shp_file: str, grid_json: gpd.GeoDataFrame
) -> Union[gpd.GeoDataFrame, np.ndarray]:
    """Return GeoDataFrame and bounds of shapefile.

    Args:
        shp_file (str): _description_
        grid_json (gpd.GeoDataFrame): _description_

    Returns:
        Union[gpd.GeoDataFrame, np.ndarray]: _description_
    """
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf = gpd.read_file(shp_file)
    gdf.to_crs(grid_json.proj.values[0], inplace=True)
    # buffer polygons bounding box by twice max resolution of grid
    bbox = box(*gdf.total_bounds)
    gdf_bounds = bbox.buffer(
        2 * max(grid_json.resX.values[0], grid_json.resY.values[0])
    ).bounds
    # TODO: need to rethink buffer - leaving it out for now
    # gdf_bounds = gdf.total_bounds.buffer(2.0*buffer)
    return gdf, gdf_bounds


def get_data_via_catalog(
    params_json: gpd.GeoDataFrame,
    grid_json: gpd.GeoDataFrame,
    bounds: np.ndarray,
    begin_date: str,
    end_date: Optional[str] = None,
) -> xr.Dataset:
    """Get xarray spatial and temporal subset.

    Args:
        params_json (gpd.GeoDataFrame): _description_
        grid_json (gpd.GeoDataFrame): _description_
        bounds (np.ndarray): _description_
        begin_date (str): _description_
        end_date (str, optional): _description_. Defaults to None.

    Returns:
        xr.Dataset: _description_
    """
    ds_url = params_json.URL.values[0]
    # get grid data subset to polygons buffered bounding box
    ss_dict = build_subset(params_json, grid_json, bounds, begin_date, end_date)
    # gridMET requires the '#fillmismatch' see:
    # https://discourse.oceanobservatories.org/
    # t/
    # accessing-data-on-thredds-opendap-via-python-netcdf4-or-xarray
    # -dealing-with-fillvalue-type-mismatch-error/61
    ds = xr.open_dataset(ds_url + "#fillmismatch", decode_coords=True, chunks={})
    varname = params_json.varname.values[0]
    return ds[varname].sel(**ss_dict)


def _get_data_via_subset(
    params_json: gpd.GeoDataFrame,
    grid_json: gpd.GeoDataFrame,
    bounds: np.ndarray,
    begin_date: str,
    end_date: Optional[str] = None,
) -> xr.Dataset:
    """Get xarray spatial and temporal subset.

    Args:
        params_json (gpd.GeoDataFrame): _description_
        grid_json (gpd.GeoDataFrame): _description_
        bounds (np.ndarray): _description_
        begin_date (str): _description_
        end_date (str, optional): _description_. Defaults to None.

    Returns:
        xr.Dataset: _description_
    """
    ds_url = params_json.URL.values[0]
    # get grid data subset to polygons buffered bounding box
    ss_dict = build_subset(params_json, grid_json, bounds, begin_date, end_date)
    # gridMET requires the '#fillmismatch' see:
    # https://discourse.oceanobservatories.org/
    # t/
    # accessing-data-on-thredds-opendap-via-python-netcdf4-or-xarray
    # -dealing-with-fillvalue-type-mismatch-error/61
    ds = xr.open_dataset(ds_url + "#fillmismatch", decode_coords=True, chunks={})

    return ds.sel(**ss_dict)


def calc_weights_catalog(
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
    wght_gen = generate_weights(
        poly=gdf,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        grid_cells_crs=grid_json.proj.values[0],
        filename=wght_gen_file,
        wght_gen_crs=wght_gen_proj,
    )

    return wght_gen


def calc_weights_catalog_pershp(
    params_json: pd.DataFrame,
    grid_json: pd.DataFrame,
    geo_s: gpd.GeoDataFrame,
    wght_gen_proj: Any,
) -> pd.DataFrame:
    """Calculate area-intersected weights of grid to feature.

    Args:
        params_json (pd.DataFrame): _description_
        grid_json (pd.DataFrame): _description_
        geo_s (gpd.GeoDataFrame): _description_
        wght_gen_proj (Any): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # ds_URL = params_json.URL.values[0]
    ds_proj = grid_json.proj.values[0]
    # only need one time step for generating weights so choose the first time from the param_cat
    date = params_json.duration.values[0].split("/")[0]

    # read shapefile, calculate total_bounds, and project to grid's projection
    geo_s.to_crs(grid_json.proj.values[0], inplace=True)
    bbox = box(*geo_s.total_bounds)
    geo_s_bounds = bbox.buffer(
        2 * max(grid_json.resX.values[0], grid_json.resY.values[0])
    ).bounds

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
    # gdf_grid = gpd.GeoDataFrame.from_features(gridpoly)
    # gdf_grid.set_crs(4326, inplace=True)
    gdf_grid.to_crs(grid_json.proj.values[0], inplace=True)

    # calculate the intersection weights and generate weight_file
    # assumption is that the first column in the shp_file is the id to use for
    # calculating weights
    apoly_idx = geo_s.columns[0]
    wght_gen = _generate_weights_pershp(
        poly=geo_s,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        grid_cells_crs=grid_json.proj.values[0],
        wght_gen_crs=wght_gen_proj,
    )

    return wght_gen


def _run_weights_catalog_pershp(
    params_json: gpd.GeoDataFrame,
    grid_json: gpd.GeoDataFrame,
    wght_file: pd.DataFrame,
    shp: gpd.GeoDataFrame,
    begin_date: str,
    end_date: str,
) -> Union[gpd.GeoDataFrame, np.ndarray]:
    """Run area-weighted aggragation of grid to feature.

    Args:
        params_json (gpd.GeoDataFrame): _description_
        grid_json (gpd.GeoDataFrame): _description_
        wght_file (pd.DataFrame): _description_
        shp (gpd.GeoDataFrame): _description_
        begin_date (str): _description_
        end_date (str): _description_

    Returns:
        Union[gpd.GeoDataFrame, np.ndarray]: _description_
    """
    poly_idx = shp.columns[0]
    wghts = _get_wieght_df(wght_file, poly_idx)

    # read shapefile, calculate total_bounds, and project to grid's projection
    shp.to_crs(grid_json.proj.values[0], inplace=True)
    bbox = box(*shp.total_bounds)
    b_buf = max(grid_json.resX.values[0], grid_json.resY.values[0])
    gdf_bounds = bbox.buffer(2 * b_buf).bounds
    # gdf_bounds = shp.total_bounds

    # get sub-setted xarray dataset
    ds = get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=begin_date,
        end_date=end_date,
    )

    # shp.reset_index(drop=True, inplace=True)
    gdf1 = shp.dissolve(by=poly_idx)

    geo_index = np.asarray(gdf1.index, dtype=type(gdf1.index.values[0]))
    n_geo = len(geo_index)

    print_on = _get_print_on(n_geo)
    unique_geom_ids = wghts.groupby(poly_idx)

    var = str(params_json.varname.values[0])
    time = str(params_json.T_name.values[0])
    ds_vars = [i for i in ds.data_vars]
    # if var not in ds_vars:
    #     raise KeyError(f"var: {var} not in ds vars: {ds_vars}")
    #     return None, None

    nts = len(ds.coords[time].values)
    try:
        native_dtype = ds[var].values.dtype
    except KeyError:
        print(f"var: {var} not in ds vars: {ds_vars}")
        return None, None
    val_interp = np.empty(nts, dtype=native_dtype)
    # dvar = np.array([var for _ in range(nts)], dtype=str)
    # dates = ds.coords[time].values
    var_vals = ds[var].values
    i = 0
    # for t in np.arange(nts):
    #     # val_flat_interp = (
    #     #     ds[var].values[t, 1 : grd_shp[1] - 1, 1 : grd_shp[2] - 1].flatten()
    #     # )
    # for i in np.arange(len(geo_index)):

    weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
    tw = weight_id_rows.wght.values
    i_ind = np.array(weight_id_rows.i.values)
    j_ind = np.array(weight_id_rows.j.values)

    vals = var_vals[:, i_ind, j_ind]

    # tgid = weight_id_rows.grid_ids.values
    # tmp = getaverage(val_flat_interp[tgid], tw)
    tmp = getaverage_wtime(vals, tw)
    try:
        if np.isnan(tmp).any():
            # val_interp[t, i] = np_get_wval(
            #     val_flat_interp[tgid], tw, geo_index[i]
            # )
            val_interp[:] = np_get_wval_wtime(vals, tw)
        else:
            val_interp[:] = tmp
    except KeyError:
        val_interp[:] = netCDF4.default_fillvals["f8"]

    if i % print_on == 0:
        print(f"    Processing {var} for feature {geo_index[i]}", flush=True)

    # print(val_interp)
    # pd_data = {"variable": dvar}
    # # ndf = pd.DataFrame(pd_data)
    # ndf = pd.DataFrame(
    #     pd_data, index=pd.DatetimeIndex(dates, name="date"), columns=[geo_index[:]]
    # )
    # ndf[geo_index[i]] = val_interp
    return gdf1, val_interp


def run_weights_catalog(
    params_json: gpd.GeoDataFrame,
    grid_json: gpd.GeoDataFrame,
    wght_file: Union[str, pd.DataFrame],
    shp_file: str,
    begin_date: str,
    end_date: str,
) -> Union[gpd.GeoDataFrame, np.ndarray]:
    """Run area-weighted aggragation of grid to feature.

    Args:
        params_json (gpd.GeoDataFrame): _description_
        grid_json (gpd.GeoDataFrame): _description_
        wght_file (Union[str, pd.DataFrame]): _description_
        shp_file (str): _description_
        begin_date (str): _description_
        end_date (str): _description_

    Returns:
        Union[gpd.GeoDataFrame, np.ndarray]: _description_
    """
    # read shapefile, calculate total_bounds, and project to grid's projection
    shp, gdf_bounds = _get_shp_file(shp_file=shp_file, grid_json=grid_json)
    wghts = _get_wieght_df(wght_file, shp.columns[0])

    # get sub-setted xarray dataset
    ds = get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=begin_date,
        end_date=end_date,
    )
    #     ds.load()
    #     dslist.append(ds)
    # ds = xr.concat(dslist, axis=params_json.T_name.values[0])

    poly_idx = shp.columns[0]
    shp.reset_index(drop=True, inplace=True)
    gdf = shp.sort_values(poly_idx).dissolve(by=poly_idx)
    # gdf = shp.dissolve(by=poly_idx)

    geo_index = np.asarray(gdf.index, dtype=type(gdf.index.values[0]))
    n_geo = len(geo_index)

    print_on = _get_print_on(n_geo)
    unique_geom_ids = wghts.groupby(poly_idx)

    var = str(params_json.varname.values[0])
    time = str(params_json.T_name.values[0])
    # ds_vars = [i for i in ds.data_vars]
    # if var not in ds_vars:
    #     raise KeyError(f"var: {var} not in ds vars: {ds_vars}")
    #     return None, None

    nts = len(ds.coords[time].values)
    # tv = ds.coords[time].values
    native_dtype = ds.dtype
    val_interp = np.empty((n_geo, nts), dtype=native_dtype)

    try:
        print(f"loading {var} values", flush=True)
        ds.load()
        var_vals = ds.values
        print(f"finished loading {var} values", flush=True)
    except Exception:
        print("error loading data")

    for i in np.arange(len(geo_index)):
        weight_id_rows = unique_geom_ids.get_group(str(geo_index[i]))
        tw = weight_id_rows.wght.values
        i_ind = np.array(weight_id_rows.i.values)
        j_ind = np.array(weight_id_rows.j.values)

        vals = var_vals[:, i_ind, j_ind]
        tmp = getaverage_wtime(vals, tw)

        try:
            if np.isnan(tmp[:]).any():
                val_interp[i, :] = netCDF4.default_fillvals["f8"]
            else:
                val_interp[i, :] = tmp
        except KeyError:
            val_interp[i, :] = netCDF4.default_fillvals["f8"]

        if i % print_on == 0:
            print(f"    Processing {var} for feature {geo_index[i]}", flush=True)

    return gdf, val_interp


def get_data_subset_catalog(
    params_json: gpd.GeoDataFrame,
    grid_json: gpd.GeoDataFrame,
    shp_file: str,
    begin_date: str,
    end_date: str,
) -> xr.Dataset:
    """Get xarray subset data.

    Args:
        params_json (gpd.GeoDataFrame): _description_
        grid_json (gpd.GeoDataFrame): _description_
        shp_file (str): _description_
        begin_date (str): _description_
        end_date (str): _description_

    Returns:
        xr.Dataset: _description_
    """
    # read shapefile, calculate total_bounds, and project to grid's projection
    shp, gdf_bounds = _get_shp_file(shp_file=shp_file, grid_json=grid_json)

    # get sub-setted xarray dataset
    ds = get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=begin_date,
        end_date=end_date,
    )

    return ds


def _get_wieght_df(
    wght_file: Union[str, pd.DataFrame], poly_idx: str
) -> Union[pd.DataFrame, None]:
    if isinstance(wght_file, pd.DataFrame):
        wghts = wght_file
    elif isinstance(wght_file, str):
        wghts = pd.read_csv(
            wght_file, dtype={"i": int, "j": int, "wght": float, poly_idx: str}
        )
    else:
        sys.exit("wght_file must be one of string or pandas.DataFrame")
    return wghts


def _date_range(start, end, intv):
    from datetime import datetime

    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y-%m-%d")
    yield end.strftime("%Y-%m-%d")


def _get_catalog_time_increment(param: pd.DataFrame) -> Union[int, str]:
    interval = param["interval"].values[0].split(" ")
    return int(interval[0]), str(interval[1])
