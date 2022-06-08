import pickle
from lz4 import frame


def encode(obj):
    return pickle.dumps(obj)


def decode(obj):
    return pickle.loads(obj)


def encode_lz4(obj):
    #  序列化、压缩
    msg = pickle.dumps(obj)
    return frame.compress(msg)


def decode_lz4(obj):
    uncompress_obj = frame.decompress(obj)
    return pickle.loads(uncompress_obj)