# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/API_Prediction.ipynb (unless otherwise specified).

__all__ = ["Prediction"]

# Cell

from typing import *

# Internal Cell

import os
import requests

from pathlib import Path
import pandas as pd
from fastcore.foundation import patch
from tqdm import tqdm

from ..logger import get_logger, set_level
from ..helper import (
    get_data,
    post_data,
    delete_data,
    add_ready_column,
    generate_df,
    get_attributes_from_instances,
)

from .client import Client
from .progress_status import ProgressStatus
from ..constant import CLIENT_DB_USERNAME, CLIENT_DB_PASSWORD

# Internal Cell

logger = get_logger(__name__)

# Cell


class Prediction(ProgressStatus):
    """A class to manage and download the predictions.

    The `Prediction` class is automatically instantiated by calling the `Model.predict` method of a `Model` instance.
    Currently, it is the only way to instantiate this class.
    """

    BASIC_PRED_COLS = ["id", "created", "total_steps", "completed_steps"]
    ALL_PRED_COLS = BASIC_PRED_COLS + ["model_id", "datasource_id", "error"]

    def __init__(
        self,
        id: int,
        datasource_id: Optional[int] = None,
        model_id: Optional[int] = None,
        created: Optional[pd.Timestamp] = None,
        total_steps: Optional[int] = None,
        completed_steps: Optional[int] = None,
        error: Optional[str] = None,
        disabled: Optional[bool] = None,
    ):
        """Constructs a new `Prediction` instance

        Warning:
            Do not construct this object directly by calling the constructor, instead please use
            `Model.predict` method of the Model instance.

        Args:
            id: Prediction ID in the server.
            datasource_id: DataSource ID in the server.
            model_id: Model ID in the server.
            created: Prediction creation date.
            total_steps: No of steps needed to complete the model prediction.
            completed_steps: No of steps completed so far in the model prediction.
            error: Error message while making the prediction.
            disabled: Flag to indicate the status of the prediction.
        """
        self.id = id
        self.datasource_id = datasource_id
        self.model_id = model_id
        self.created = created
        self.total_steps = total_steps
        self.completed_steps = completed_steps
        self.error = error
        self.disabled = disabled
        ProgressStatus.__init__(self, relative_url=f"/prediction/{self.id}")

    @staticmethod
    def _download_prediction_file_to_local(
        file_name: str, url: str, path: Union[str, Path]
    ) -> None:
        """Download the file to local directory.

        Args:
            file_name: Name of the file
            url: Url of the file
            path: Local directory path

        Raises:
            HTTPError: If the **url** is invalid or not reachable.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(e)

        else:
            with open(Path(path) / file_name, "wb") as f:
                f.write(response.content)

    @staticmethod
    def ls(
        offset: int = 0,
        limit: int = 100,
        disabled: bool = False,
        completed: bool = False,
    ) -> List["Prediction"]:
        """Return the list of Prediction instances available in the server.

        Args:
            offset: The number of predictions to offset at the beginning. If None, then the default value **0** will be used.
            limit: The maximum number of predictions to return from the server. If None,
                then the default value **100** will be used.
            disabled: If set to **True**, then only the deleted predictions will be returned. Else, the default value
                **False** will be used to return only the list of active predictions.
            completed: If set to **True**, then only the predictions that are successfully processed in server will be returned.
                Else, the default value **False** will be used to return all the predictions.

        Returns:
            A list of Prediction instances available in the server.

        Raises:
            ConnectionError: If the server address is invalid or not reachable.

        An example to list the available predictions:

        ```python
        Prediction.ls()
        ```
        """
        lists = Client._get_data(
            relative_url=f"/prediction/?disabled={disabled}&completed={completed}&offset={offset}&limit={limit}"
        )

        predx = [
            Prediction(
                id=pred["id"],
                model_id=pred["model_id"],
                datasource_id=pred["datasource_id"],
                created=pred["created"],
                total_steps=pred["total_steps"],
                completed_steps=pred["completed_steps"],
                error=pred["error"],
                disabled=pred["disabled"],
            )
            for pred in lists
        ]

        return predx

    @staticmethod
    def as_df(predx: List["Prediction"]) -> pd.DataFrame:
        """Return the details of prediction instances as a pandas dataframe.

        Args:
            predx: List of prediction instances.

        Returns:
            Details of all the prediction in a dataframe.

        Raises:
            ConnectionError: If the server address is invalid or not reachable.

        An example get the details of available prediction:

        ```python
        predictionx = Prediction.ls()
        Prediction.as_df(predictionx)
        ```
        """
        lists = get_attributes_from_instances(predx, Prediction.BASIC_PRED_COLS)  # type: ignore

        df = generate_df(lists, Prediction.BASIC_PRED_COLS)

        return add_ready_column(df)

    def details(self) -> pd.DataFrame:
        raise NotImplementedError()

    def to_pandas(self) -> pd.DataFrame:
        raise NotImplementedError()

    def delete(self) -> pd.DataFrame:
        raise NotImplementedError()

    def to_s3(
        self,
        uri: str,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> ProgressStatus:
        raise NotImplementedError()

    def to_local(
        self,
        path: Union[str, Path],
        show_progress: Optional[bool] = True,
    ) -> None:
        raise NotImplementedError()

    def to_mysql(
        self,
        *,
        host: str,
        database: str,
        table: str,
        port: int = 3306,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> ProgressStatus:
        raise NotImplementedError()

    def to_clickhouse(
        self,
        *,
        host: str,
        database: str,
        table: str,
        port: int = 0,
        protocol: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> ProgressStatus:
        raise NotImplementedError()


# Cell


@patch
def details(self: Prediction) -> pd.DataFrame:
    """Return the details of a prediction.

    Returns:
        A pandas DataFrame encapsulating the details of the prediction.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.

    An example to get details of a prediction:

    ```python
    prediction.details()
    ```
    """
    details = Client._get_data(relative_url=f"/prediction/{self.id}")

    details_df = pd.DataFrame(details, index=[0])[Prediction.ALL_PRED_COLS]

    return add_ready_column(details_df)


# Cell


@patch
def delete(self: Prediction) -> pd.DataFrame:
    """Delete a prediction from the server.

    Returns:
        A pandas DataFrame encapsulating the details of the deleted prediction.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.

    An example to delete a prediction:

    ```python
    prediction.delete()
    ```
    """
    predictions = Client._delete_data(relative_url=f"/prediction/{self.id}")

    predictions_df = pd.DataFrame(predictions, index=[0])[Prediction.BASIC_PRED_COLS]

    return add_ready_column(predictions_df)


# Cell


@patch
def to_pandas(self: Prediction) -> pd.DataFrame:
    """Return the prediction results as a pandas DataFrame

    Returns:
        A pandas DataFrame encapsulating the results of the prediction.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.

    An example to convert the prediction results into a pandas DataFrame:

    ```python
    predictions.to_pandas()
    ```
    """
    response = Client._get_data(relative_url=f"/prediction/{self.id}/pandas")
    keys = list(response.keys())
    keys.remove("Score")
    index_name = keys[0]
    return (
        pd.DataFrame(response)
        .set_index(index_name)
        .sort_values("Score", ascending=False)
    )


# Cell


@patch
def to_s3(
    self: Prediction,
    uri: str,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
) -> ProgressStatus:
    """Push the prediction results to the target AWS S3 bucket.

    Args:
        uri: Target S3 bucket uri.
        access_key: Access key for the target S3 bucket. If **None** (default value), then the value
            from **AWS_ACCESS_KEY_ID** environment variable is used.
        secret_key: Secret key for the target S3 bucket. If **None** (default value), then the value
            from **AWS_SECRET_ACCESS_KEY** environment variable is used.

    Returns:
        An instance of `ProgressStatus` class.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.

    An example to push the prediction resluts to an AWS s3 bucket:

    ```python
        status = prediction.to_s3(
            uri="s3://target-bucket/"
        )
        status.progress_bar()
    ```
    """
    access_key = (
        access_key if access_key is not None else os.environ["AWS_ACCESS_KEY_ID"]
    )
    secret_key = (
        secret_key if secret_key is not None else os.environ["AWS_SECRET_ACCESS_KEY"]
    )

    response = Client._post_data(
        relative_url=f"/prediction/{self.id}/to_s3",
        data=dict(uri=uri, access_key=access_key, secret_key=secret_key),
    )

    return ProgressStatus(relative_url=f"/prediction/push/{response['id']}")


# Cell


@patch
def to_local(
    self: Prediction,
    path: Union[str, Path],
    show_progress: Optional[bool] = True,
) -> None:
    """Download the prediction results to a local directory.

    Args:
        path: Local directory path.
        show_progress: Flag to set the progressbar visibility. If not passed, then the default value **True** will be used.

    Raises:
        FileNotFoundError: If the **path** is invalid.
        HTTPError: If the presigned AWS s3 uri to download the prediction results are invalid or not reachable.

    An example to download the predictions to local:

    ```python
        prediction.to_local(
            path=Path('path-to-local-directory')
        )
    ```
    """
    response = Client._get_data(relative_url=f"/prediction/{self.id}/to_local")

    # Initiate progress bar
    t = tqdm(total=len(response), disable=not show_progress)

    for file_name, url in response.items():
        Prediction._download_prediction_file_to_local(file_name, url, Path(path))
        t.update()

    t.close()


# Cell


@patch
def to_mysql(
    self: Prediction,
    *,
    host: str,
    database: str,
    table: str,
    port: int = 3306,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> ProgressStatus:
    """Push the prediction results to a mysql database.

    If the database requires authentication, pass the username/password as parameters or store it in
    the **AIRT_CLIENT_DB_USERNAME** and **AIRT_CLIENT_DB_PASSWORD** environment variables.

    Args:
        host: Database host name.
        database: Database name.
        table: Table name.
        port: Host port number. If not passed, then the default value **3306** will be used.
        username: Database username. If not passed, then the value set in the environment variable
            **AIRT_CLIENT_DB_USERNAME** will be used else the default value "root" will be used.
        password: Database password. If not passed, then the value set in the environment variable
            **AIRT_CLIENT_DB_PASSWORD** will be used else the default value "" will be used.

    Returns:
        An instance of `ProgressStatus` class.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.

    An example to push the prediction resluts to a mysql database:

    ```python
        status = prediction.to_mysql(
            host="host_name",
            database="database_name",
            table="table_name"
        )
        status.progress_bar()
    ```
    """
    username = (
        username if username is not None else os.environ.get(CLIENT_DB_USERNAME, "root")
    )

    password = (
        password if password is not None else os.environ.get(CLIENT_DB_PASSWORD, "")
    )

    _body = dict(
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
        table=table,
    )

    response = Client._post_data(
        relative_url=f"/prediction/{self.id}/to_mysql", data=_body
    )

    return ProgressStatus(relative_url=f"/prediction/push/{response['id']}")


# Cell


@patch
def to_clickhouse(
    self: Prediction,
    *,
    host: str,
    database: str,
    table: str,
    protocol: str,
    port: int = 0,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> ProgressStatus:
    """Push the prediction results to a clickhouse database.

    If the database requires authentication, pass the username/password as parameters or store it in
    the **CLICKHOUSE_USERNAME** and **CLICKHOUSE_PASSWORD** environment variables.

    Args:
        host: Remote database host name.
        database: Database name.
        table: Table name.
        protocol: Protocol to use (native/http).
        port: Host port number. If not passed, then the default value **0** will be used.
        username: Database username. If not passed, then the value set in the environment variable
            **CLICKHOUSE_USERNAME** will be used else the default value "root" will be used.
        password: Database password. If not passed, then the value set in the environment variable
            **CLICKHOUSE_PASSWORD** will be used else the default value "" will be used.

    Returns:
        An instance of `ProgressStatus` class.

    Raises:
        ConnectionError: If the server address is invalid or not reachable.

    An example to push the prediction resluts to a clickhouse database:

    ```python
        status = prediction.to_clickhouse(
            host="host_name",
            database="database_name",
            table="table_name",
            protocol="native",
        )
        status.progress_bar()
    ```
    """
    username = (
        username
        if username is not None
        else os.environ.get("CLICKHOUSE_USERNAME", "root")
    )

    password = (
        password if password is not None else os.environ.get("CLICKHOUSE_PASSWORD", "")
    )

    _body = dict(
        host=host,
        database=database,
        table=table,
        protocol=protocol,
        port=port,
        username=username,
        password=password,
    )

    response = Client._post_data(
        relative_url=f"/prediction/{self.id}/to_clickhouse", data=_body
    )

    return ProgressStatus(relative_url=f"/prediction/push/{response['id']}")
