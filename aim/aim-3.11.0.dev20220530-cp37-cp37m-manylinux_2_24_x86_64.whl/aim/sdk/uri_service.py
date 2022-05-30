from cryptography.fernet import Fernet
from typing import Iterator, List, Optional, Dict
from typing import TYPE_CHECKING

from aim.storage.encoding import encode_path, decode_path
from aim.storage.types import BLOB
from aim.sdk.repo import ContainerConfig

if TYPE_CHECKING:
    from aim.storage.types import AimObjectPath
    from aim.storage.prefixview import PrefixView
    from aim.sdk.repo import Repo


def generate_resource_path(prefix_view: 'PrefixView', additional_path: 'AimObjectPath') -> str:
    prefix_path = decode_path(prefix_view.prefix)
    encoded_path = encode_path((*prefix_path, *additional_path))
    return encoded_path.hex()


class URIService:
    SEPARATOR = '__'

    def __init__(self, repo: 'Repo'):
        self.repo = repo
        self.container_persistent_pool = dict()

    @classmethod
    def generate_uri(cls, repo: 'Repo', run_name: str, sub_name: str, resource_path: str = None) -> str:
        encryptor = Fernet(key=repo.encryption_key)
        to_be_encrypted = f'{run_name}{URIService.SEPARATOR}{sub_name}'
        if resource_path:
            to_be_encrypted = f'{to_be_encrypted}{URIService.SEPARATOR}{resource_path}'

        return encryptor.encrypt(to_be_encrypted.encode()).decode()

    @classmethod
    def decode_uri(cls, repo: 'Repo', uri: str) -> List[Optional[str]]:
        decryptor = Fernet(key=repo.encryption_key)
        decrypted_uri = decryptor.decrypt(uri.encode()).decode()
        result = decrypted_uri.split(URIService.SEPARATOR, maxsplit=2)
        assert len(result) <= 3
        # extend result length to 3, fill with [None]s
        result.extend([None] * (3 - len(result)))

        return result

    def request_batch(self, uri_batch: List[str]) -> Iterator[Dict[str, bytes]]:
        for uri in uri_batch:
            run_name, sub_name, resource_path = self.decode_uri(self.repo, uri)
            container = self._get_container(run_name, sub_name)
            resource_path = decode_path(bytes.fromhex(resource_path))

            # TODO: [MV] change to some other implementation of view when available
            #  which won't collect in case of custom objects
            data = container.tree().subtree(resource_path).collect()
            if isinstance(data, BLOB):
                data = data.load()
            yield {uri: data}

        # clear container pool
        self.container_persistent_pool.clear()

    def _get_container(self, run_name: str, sub_name: str):
        config = ContainerConfig(run_name, sub_name, read_only=True)
        container = self.container_persistent_pool.get(config)

        if not container:
            if sub_name == 'meta':
                container = self.repo.request(sub_name, run_name, from_union=True, read_only=True)
            else:
                container = self.repo.request(sub_name, run_name, read_only=True)

            self.container_persistent_pool[config] = container

        return container
