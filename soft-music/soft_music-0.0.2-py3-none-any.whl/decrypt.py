import base64
import binascii
import hashlib
import gzip
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from Cryptodome import Random
from pyDes import des, CBC, PAD_PKCS5
from Cryptodome.Cipher import DES3, AES, ARC4
from Cryptodome.Hash import SHA1
from Cryptodome.Protocol.KDF import PBKDF2


def gzip_compress(text, encoding='utf-8'):
    s_in = text.encode(encoding)
    s_out = gzip.compress(s_in)
    return [i for i in s_out]


def gzip_decompress(compressed_data, encoding='utf-8'):
    res = gzip.decompress(compressed_data)
    return res.decode(encoding)


def byte_list_2_str(byte_list, encoding='utf-8'):
    # byte_list 既可以是python的字节数组， 也可以是java的字节数组
    # eg. byte_list = [-26, -83, -90, -26, -78, -101, -23, -67, -112]
    # eg. byte_list = [229, 188, 160, 228, 184, 137, 230, 135, 181, 233, 128, 188, 228, 186, 134]
    bs = bytearray()
    for item in byte_list:
        if item < 0:
            item = item + 256
        bs.append(item)

    str_data = bs.decode(encoding)
    return str_data


def str_2_byte_list(str_, encoding='utf-8'):
    data_bytes = str_.encode(encoding)
    data_list = []
    for item in data_bytes:
        data_list.append(item)
    return data_list


def b64encode(text, encoding='utf-8'):
    return base64.b64encode(text.encode(encoding))


def b64decode(encoded_str, encoding='utf-8'):
    data = base64.b64decode(encoded_str)
    return data.decode(encoding)


def md5(text, salt='', encoding='utf-8', hex_format=True):
    encrypt = hashlib.md5()
    if salt != '':
        text += salt
    encrypt.update(text.encode(encoding))
    if hex_format:
        return encrypt.hexdigest()
    return encrypt.digest()


def sha(text, mode="sha256", encoding='utf-8', hex_format=True):
    encrypt = hashlib.new(mode, text.encode(encoding))
    if hex_format:
        return encrypt.hexdigest()
    return encrypt.digest()


def aes_encrypt(text, key, iv, mode=AES.MODE_CBC, encoding='utf-8', base=16):
    aes = AES.new(
        key=key.encode(encoding),
        mode=mode,
        iv=iv.encode(encoding)
    )
    raw = pad(text.encode(encoding), base)
    return aes.encrypt(raw)


# 需要补位，str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


# 加密模式 CBC，填充方式 PAD_PKCS5
def des_encrypt(text, key, iv):
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(text, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_decrypt(key, text, iv):
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(text), padmode=PAD_PKCS5)
    return de


def rc4_encrypt(key, text, encoding='utf8', need_base64=True):
    enc = ARC4.new(key.encode(encoding))
    res = enc.encrypt(text.encode(encoding))
    if need_base64:
        return base64.b64encode(res)
    return res


def rc4_decrypt(key, encrypted_str, encoding='utf8', need_base64=True):
    if need_base64:
        data = base64.b64decode(encrypted_str)
    else:
        data = encrypted_str
    enc = ARC4.new(key.encode(encoding))
    res = enc.decrypt(data)
    return res


iv = Random.new().read(DES3.block_size)  # DES3.block_size == 8


def _3des_encrypt(key, text, iv):
    # 加密模式 OFB
    cipher_encrypt = DES3.new(add_to_16(key), DES3.MODE_OFB, iv)
    encrypted_text = cipher_encrypt.encrypt(text.encode("utf-8"))
    return encrypted_text


def _3des_decrypt(key, text, iv):
    # 加密模式 OFB
    cipher_decrypt = DES3.new(add_to_16(key), DES3.MODE_OFB, iv)
    decrypted_text = cipher_decrypt.decrypt(text)
    return decrypted_text


def pbkdf2(text, salt):
    result = PBKDF2(text, salt, count=10, hmac_hash_module=SHA1)
    result = binascii.hexlify(result)
    return result
