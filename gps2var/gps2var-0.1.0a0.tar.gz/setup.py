# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gps2var']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.5,<2.0.0', 'pyproj>=3.2.1,<4.0.0', 'rasterio>=1.2.10,<2.0.0']

setup_kwargs = {
    'name': 'gps2var',
    'version': '0.1.0a0',
    'description': 'Fast reading of geospatial variables by GPS coordinates',
    'long_description': '# gps2var\n`gps2var` is a Python library providing fast loading of geospatial variables from raster files by GPS coordinates and with interpolation.\nIn particular, it allows parallel calls with coordinates specified as large NumPy arrays of arbitrary shapes, and is compatible with PyTorch data loaders.\n\n## Examples\n### Reading from a single file\n```python\nPATH = "/vsizip/wc2.1_30s_bio.zip/wc2.1_30s_bio_1.tif"  # WorldClim annual mean temperature\n\nwith gps2var.RasterValueReader(PATH, interpolation=\'bilinear\') as reader:\n    lat, lon = 48.858222, 2.2945\n    reader.get(lon, lat)  # [11.94036207]\n```\n\n### Parallel reading from multiple files\n`MultiRasterValueReader` reads from multiple raster files and concatenates the results.\n\n```python\n# min and max temperature by month (averages for 1970-2000)\nPATHS = [f"/vsizip/wc2.1_30s_{var}.zip/wc2.1_30s_{var}_{i:02}.tif"\n         for var in ["tmin" , "tmax"] for i in range(1, 13)]\n\nwith gps2var.MultiRasterValueReader(PATHS, num_threads=len(PATHS)) as reader:\n    lat, lon = 48.858222, 2.2945\n    reader.get(lon, lat).reshape(2, 12)\n    \n# [[ 2.3  2.5  4.6  6.3 10.1 13.  15.  14.9 12.   8.8  5.   3.4]\n#  [ 7.2  8.4 11.9 14.9 19.2 22.  24.7 24.8 20.9 15.9 10.6  8. ]]\n```\n\nSet `use_multiprocessing=True` to create a separate process for each raster. This is likely to be faster than the default (i.e. multithreading), at least if the number of rasters is large.\n\n## API\n\n### `RasterValueReader`\n\nCan be created with a path to a file that can be read by Rasterio, or an open Rasterio `DatasetReader`. The behavior can be customized with keyword parameters; the most important ones are:\n- `crs`: The coordinate reference system to use for querying. By default this is EPSG:4326, i.e. longitude and latitude (in this order) as used by GPS.\n- `interpolation`: `"nearest"` (default) or `"bilinear"` (slower).\n- `fill_value`: The value (scalar) with which to replace missing values. Defaults to `np.nan`.\n- `feat_dtype`: The dtype to which to convert the result. Defaults to `np.float32`.\n- `feat_center`: Center each of the features at the given value. Defaults to `None` (no centering).\n- `feat_scale`: Scale each of the (centered) features by multiplying it by the given value. Defaults to `None` (no scaling).\n- `block_shape`: The shape of the blocks read into memory (and stored in the GDAL block cache).\n- `preload_all`: Indicates whether the whole dataset should be loaded into memory instead of loading one block at a time. Defaults to `False`.\n\nAnother option is to wrap all these arguments in a `RasterReaderSpec` (or simply a dictionary) and pass it as the first argument.\n\n### `RasterValueReaderPool`\n\nLike `RasterValueReader`, but spawns `num_workers` worker processes that all read from the same file concurrently.\nBesides `get()` (which blocks until the result is ready), it provides `async_get()`, which returns a `concurrent.futures.Future`.\n\n### `MultiRasterValueReader`\n\nExpects as the first argument a list of file paths, `RasterReaderSpec`s, or `dict`s, and reads from each file in a separate thread or process. Additional options to be applied to all items can be passed as keyword arguments. Additionally, the following parameters are accepted:\n- `use_multiprocessing`: If `True`, each raster will be processed in a separate process. \n- `num_threads`: The number of threads to use for parallel reading. By default, this is set to the number of rasters. Set to 0 to read in the main thread.\n\n### `ProcessManager`\n\nA `multiprocessing.BaseManager` – a context manager that spawns a separate process. It provides `RasterValueReader()`, `MultiRasterValueReader()`, and `RasterValueReaderPool()` methods that create the corresponding reader in that process and return a proxy object that can be used in much the same way as the reader itself. A nice property of a proxy object is that it can be copied between processes without copying the underlying reader, so it works with PyTorch `DataLoader`.\n\n## PyTorch `DataLoader` and parallelism\nSimply using a `RasterValueReader` with a PyTorch `DataLoader` with `num_workers > 0` and with the `"fork"` [start method](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods) (default on Unix) **will not work**.\n\nHere are examples of usage that do work:\n- Using `multiprocessing.set_start_method("spawn")`. This will create a copy of the reader in each worker process.\n- Setting `preload_all=True` so that the whole raster is loaded into memory.\n- Using `MultiRasterValueReader` as above, but with `use_multiprocessing=True`. This way, each raster wil be read in a separate process.\n- Using `ProcessManager`, e.g.:\n\n  ```python\n  # in __init__:\n  self.manager = gps2var.ProcessManager()\n  self.manager.start()  # start a new process\n  self.reader = manager.RasterValueReader(path)  # proxy object\n  \n  # in __getitem__:\n  self.reader.get(lon, lat)\n  ```\n  \n  In this case, the reader is placed in a separate process and the workers connect to it using the proxy object.\n',
    'author': 'Ondřej Cífka',
    'author_email': 'cifkao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cifkao/gps2var',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
