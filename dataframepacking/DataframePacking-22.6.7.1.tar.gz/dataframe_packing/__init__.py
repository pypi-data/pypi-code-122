# gist tags: tar tar.gz pandas dataframe
import os
from pathlib import Path
import re
import tarfile
import pandas as pd
from tempfile import TemporaryDirectory


def save_frames_to_tar(
    names_to_dfs_dict:dict[str, pd.DataFrame], 
    out_directory:str, gzip=True) -> str:
    """
    Saves a dictionary of {table_name (str): table_df (pd.DataFrame)} entries to a tar file as tarred CSVs.

    Args:
        out_directory (str): The name of the file to write out to (with or without the extension)
        names_to_dfs_dict (dict[str, pd.DataFrame]): A dictionary of dataframe names and dataframes
        gzip (bool, optional): If true, gzips the end tar and saves as .tar.gz. otherwise, saves as a .tar. Defaults to True.
    
    Returns:
        str: The path to the tarfile that was written out
    """
    if gzip:
        mode = 'w:gz'
        ext = '.tar.gz'
    else:
        mode = 'w'
        ext = '.tar'

    out_directory = out_directory.strip()
    if out_directory.endswith(".tar.gz"):
        out_directory = out_directory[0:-len(".tar.gz")]
    elif out_directory.endswith(".tar"):
        out_directory = out_directory[0:-len(".tar")]


    # Make sure the data_path de-references all relative paths
    out_directory = os.path.realpath(os.path.expanduser(out_directory))
    out_directory_dir = os.path.dirname(out_directory)
    
    # Make sure the directory exists
    if not os.path.exists(out_directory_dir):
        os.makedirs(out_directory_dir)

    # Create a tarfile into which frames can be added
    with tarfile.open(f"{out_directory}{ext}", mode=mode) as tfo:
    
        # Loop over all dataframes to be saved
        for file_name, df in names_to_dfs_dict.items():
            file_name:str = file_name.strip()
            file_name = file_name + ".csv"

            # Create a temporary directory for packaging into a tar_file
            #temp_dir = TemporaryDirectory()
            with TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                file_loc = temp_dir_path/file_name
                df.to_csv(file_loc, index=False)

                # Add the temp file to the tarfile
                tfo.add(file_loc)
        filename = tfo.name
    return filename

        
def load_frames_from_tar(in_tar_file:str, gzip=True) -> dict[str, pd.DataFrame]:
    """Loads a dictionary of {table_name (str): table_df (pd.DataFrame)} files from a (possibly gzipped) tar file of Pandas dataframes as CSVs.

    Args:
        in_tar_file (str): The tarred dataframe csvs to read in.
        gzip (bool, optional): True if the provided dataframes are gzipped (.tar.gz). Defaults to True.

    Returns:
        dict[str, pd.DataFrame]: A dictionary from the name of the dataframe (minus the last .csv extension) to the contents of the dataframe.
    """

    if gzip:
        mode = 'r:gz'
    else:
        mode = 'r'

    # Make sure the data_path de-references all relative paths
    in_tar_file = os.path.realpath(os.path.expanduser(in_tar_file))

    dataframe_dict = dict()
    print(in_tar_file)
    
    # Create a tarfile into which frames can be added
    with tarfile.open(in_tar_file, mode=mode) as tfo:
        # Loop over all dataframes to be saved
        for member in tfo.getmembers():
            f = tfo.extractfile(member)
            df = pd.read_csv(f)
            df_name = os.path.basename(member.name)
            if df_name.endswith(".csv"):
                df_name = df_name[0:-4]

            dataframe_dict[df_name] = df

    return dataframe_dict

