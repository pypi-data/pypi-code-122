import os
from tempfile import TemporaryDirectory
import pytest
import pandas as pd
from dataframe_packing import load_frames_from_tar, save_frames_to_tar

def test_make_tar_nogzip():
    with TemporaryDirectory(prefix='rev_processing__') as temp_dir:
        df1 = pd.DataFrame([[1, 2], [3, 1]], columns=['a', 'b'])
        df1_name = "name1.csv"
        df2 = pd.DataFrame([[1, 2], [3.6, 1]], columns=['c', 'd'])
        df2_name = "name2"

        df_dict = {df1_name:df1, df2_name:df2}
        tar_loc = os.path.join(temp_dir, "test_make_tar")

        save_frames_to_tar(df_dict, tar_loc)


def test_make_tar_gzip():
    with TemporaryDirectory(prefix='rev_processing__') as temp_dir:
        df1 = pd.DataFrame([[1, 2], [3, 1]], columns=['a', 'b'])
        df1_name = "name1.csv"
        df2 = pd.DataFrame([[1, 2], [3.6, 1]], columns=['c', 'd'])
        df2_name = "name2"

        df_dict = {df1_name:df1, df2_name:df2}
        tar_loc = os.path.join(temp_dir, "test_make_tar")

        save_frames_to_tar(df_dict, tar_loc, gzip=True)


def test_load_tar_gzip():
    with TemporaryDirectory(prefix='rev_processing__') as temp_dir:
        df1 = pd.DataFrame([[1, 2], [3, 1]], columns=['a', 'b'])
        df1_name = "name1.csv"
        df2 = pd.DataFrame([[1, 2], [3.6, 1]], columns=['c', 'd'])
        df2_name = "name2"

        df_dict = {df1_name:df1, df2_name:df2}
        tar_loc = os.path.join(temp_dir, "test_make_tar.tar")

        saved_loc = save_frames_to_tar(df_dict, tar_loc, gzip=True)
        df_dict = load_frames_from_tar(saved_loc, gzip=True)
        
def test_load_tar_gzip2():
    with TemporaryDirectory(prefix='rev_processing__') as temp_dir:
        df1 = pd.DataFrame([[1, 2], [3, 1]], columns=['a', 'b'])
        df1_name = "name1.csv"
        df2 = pd.DataFrame([[1, 2], [3.6, 1]], columns=['c', 'd'])
        df2_name = "name2"

        df_dict = {df1_name:df1, df2_name:df2}
        tar_loc = os.path.join(temp_dir, "test_make_tar")

        saved_loc = save_frames_to_tar(df_dict, tar_loc, gzip=True)
        df_dict = load_frames_from_tar(saved_loc, gzip=True)

def test_load_tar_gzip2():
    with TemporaryDirectory(prefix='rev_processing__') as temp_dir:
        df1 = pd.DataFrame([[1, 2], [3, 1]], columns=['a', 'b'])
        df1_name = "name1.csv"
        df2 = pd.DataFrame([[1, 2], [3.6, 1]], columns=['c', 'd'])
        df2_name = "name2"

        df_dict = {df1_name:df1, df2_name:df2}
        tar_loc = os.path.join(temp_dir, "test_make_tar.tar.gz")
        saved_loc = save_frames_to_tar(df_dict, tar_loc, gzip=True)
        df_dict_loaded = load_frames_from_tar(saved_loc, gzip=True)
