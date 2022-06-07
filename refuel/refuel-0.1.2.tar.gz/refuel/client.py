import os
import concurrent.futures as pyfutures
from datetime import datetime
import math
from typing import Dict, List
import sys

from loguru import logger
from requests_futures.sessions import FuturesSession

from refuel.types import Event, EventBatch

class RefuelClient:
    # Default config settings
    API_BASE_URL = 'https://api.refuel.ai'
    API_KEY_ENV_VARIABLE = 'REFUEL_API_KEY'
    TIMEOUT_SECS = 3
    MAX_RETRIES = 3
    MAX_WORKERS = os.cpu_count()
    DT_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
    MAX_BYTES_PER_BATCH = 3000000   # 3 MB
    
    def __init__(
        self,
        api_key: str = None,
        api_base_url: str = API_BASE_URL,
        timeout: int = TIMEOUT_SECS,
        max_retries: int = MAX_RETRIES,
        max_workers: int = MAX_WORKERS
    ) -> None:
        """
        Args:
            api_key (str, optional): Refuel API Key. Defaults to None.
            api_base_url (str, optional): Base URL of the Refuel API endpoints. Defaults to API_BASE_URL.
            timeout (int, optional): Timeout (secs) for a given API call. Defaults to TIMEOUT_SECS.
            max_retries (int, optional): Max num retries. Defaults to MAX_RETRIES.
            max_workers (int, optional): Max number of concurrent tasks in the ThreadPoolExecutor
        """
        # initialize variables
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV_VARIABLE)
        self._api_base_url = api_base_url
        self._timeout = timeout
        self._max_retries = max_retries
        self._header = {
            'Content-Type': 'application/json',
            'x-api-key': self._api_key
        }
        # initialize request session
        # TODO: customize adapters to take into account max_retries parameters
        self._session = FuturesSession(max_workers=max_workers)

        # Get initialization context from Refuel
        if not self._api_key or not isinstance(self._api_key, str):
            logger.error(f"API Key is absent or invalid: {self._api_key}. logged")
            self._init_context = {}
        else:
            init_response = self._get(url=self._api_base_url + "/init").result()
            self._init_context = init_response.json()

    def _get(self, url: str, params: Dict = None) -> pyfutures.Future:
        return self._session.get(url, headers=self._header, params=params)
    
    def _post(self, url: str, body: str) -> pyfutures.Future:
        return self._session.post(url, headers=self._header, timeout=self._timeout, data=body)

    def _chunkify_events(self, events: List) -> List:
        # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
        nbytes = sum([sys.getsizeof(e) for e in events])
        nchunks = math.floor(nbytes / self.MAX_BYTES_PER_BATCH) + 1
        width = math.floor(len(events) / nchunks) + 1
        return [events[i:i + width] for i in range(0, len(events), width)]

    def log(
        self,
        model_name: str,
        x: Dict,
        y_pred: Dict,
        y_true: Dict = None,
        metadata: Dict = None
    ) -> pyfutures.Future:
        """
        Log individual events to the Refuel platform.

        Args:
            model_name (str): _description_
            x (dict): _description_
            y_pred (dict): _description_
            y_true (dict, optional): _description_. Defaults to None.
            metadata (dict, optional): _description_. Defaults to None.

        Returns:
            pyfutures.Future: _description_
        """
        if not self._api_key:
            logger.error(f"API Key is absent or invalid: {self._api_key}. No event was logged")
            return None
        if model_name not in self._init_context.get('models', []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)
        event = Event(
            model_name,
            client_timestamp,
            x,
            y_pred,
            y_true,
            metadata
        )
        return self._post(
            url=self._api_base_url + "/log",
            body=event.serialize()
        )
    
    def log_batch(
        self,
        model_name: str,
        events: List
    ) -> List[pyfutures.Future]:
        """_summary_

        Args:
            model_name (str): _description_
            events (List): _description_

        Returns:
            List[pyfutures.Future]: _description_
        """
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged")
            return None
        if model_name not in self._init_context.get('models', []):
            logger.error(
                f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)
        chunks = self._chunkify_events(events)
        futures = []
        for chunk in chunks:
            batch = EventBatch(
                model_name,
                client_timestamp,
                chunk
            )
            futures.append(
                self._post(
                    url=self._api_base_url + "/log",
                    body=batch.serialize()
                )
            )
        return futures


