from tsdl.api import req, url
from tsdl.config.config import CONFIG
from tsdl.common.util import to_dict


def manual(protocol: str, operation: str, mode: str = None, security: str = None):
    u = url.get(CONFIG.get('API', 'pro') + ':manual')
    return req.get(url.get(CONFIG.get('API', 'pro') + ':manual'),
                   params=to_dict(protocol=protocol, operation=operation, mode=mode, security=security))


def encode(parse: dict):
    return req.post(url.get(CONFIG.get('API', 'pro') + ':encode'), jsons=parse)


def decode(frame: str, session: dict = None):
    return req.post(url.get(CONFIG.get('API', 'pro') + ':decode'), jsons=to_dict(frame=frame, session=session))
