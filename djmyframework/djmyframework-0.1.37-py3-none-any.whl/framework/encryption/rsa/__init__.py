# -*- coding: UTF-8 -*-

import base64

import M2Crypto
from M2Crypto import BIO


# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Crypto.PublicKey import RSA


def private_encrypt(msg, file_name):
    """私钥加密
    """
    # print(type(msg), "原文: ", msg)

    rsa_pri = M2Crypto.RSA.load_key(file_name)
    ctxt_pri = rsa_pri.private_encrypt(msg.encode(), M2Crypto.RSA.pkcs1_padding)  # 这里的方法选择加密填充方式，所以在解密的时候 要对应。
    ctxt64_pri = base64.b64encode(ctxt_pri).decode()  # 密文是base64  方便保存 encode成str
    return ctxt64_pri


def private_encrypt_str(msg, context):
    """私钥加密
    """
    # print(type(msg), "原文: ", msg)

    rsa_pri = M2Crypto.RSA.load_key_string(context.strip('\n').encode('utf-8'))
    ctxt_pri = rsa_pri.private_encrypt(msg.encode(), M2Crypto.RSA.pkcs1_padding)  # 这里的方法选择加密填充方式，所以在解密的时候 要对应。
    ctxt64_pri = base64.b64encode(ctxt_pri).decode()  # 密文是base64  方便保存 encode成str
    return ctxt64_pri


def get_m2c_pub(pub_string):
    """将公钥字符串转为m2c的对象
    """
    return M2Crypto.RSA.load_pub_key_bio(BIO.MemoryBuffer(pub_string))


def get_m2c_private(private_string):
    """将私钥字符串转为m2c的对象
    """
    # rsa_pri = M2Crypto.RSA.load_key_bio(private_string)
    return M2Crypto.RSA.load_key_bio(BIO.MemoryBuffer(private_string))


def read_key(file_path, key_type):
    """
    读取RSA密钥
    :param file_path: 文件路径
    :param key_type: 密钥类型，private：私钥|public：公钥
    :return:
    """
    with open(file_path, "rb") as file_handler:
        rea_key = BIO.MemoryBuffer(file_handler.read())
    if key_type == "private":
        return M2Crypto.RSA.load_key_bio(rea_key)
    else:
        return M2Crypto.RSA.load_pub_key_bio(rea_key)


def public_decrypt(data, m2c_pub):
    """公钥解密数据
    """
    data = base64.b64decode(data)
    _maxlength = 128
    l_dstr = [m2c_pub.public_decrypt(data[i * _maxlength:_maxlength * (i + 1)], M2Crypto.RSA.pkcs1_padding) for i in
              range(int(len(data) / _maxlength))]
    return b''.join(l_dstr)


def private_decrypt(data, m2c_pri):
    """私钥解密数据
    """
    data = base64.b64decode(data)
    _maxlength = 128
    l_dstr = [m2c_pri.private_decrypt(data[i * _maxlength:_maxlength * (i + 1)], M2Crypto.RSA.pkcs1_padding) for i in
              range(int(len(data) / _maxlength))]
    return b''.join(l_dstr)


def read_str_key(context):
    # print(M2Crypto.RSA.load_key_string(file.strip('\n').encode('utf-8')))
    return M2Crypto.RSA.load_key_string(context.strip('\n').encode('utf-8'))


# TODO: 注意密钥的格式，很重要
public_key = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDVGGIfySLp79NL2xubk36CQYle
zwHFQ7IR6IQI/0wS0hUCGEPEFBIz5Ajz+PRWAv7x7uqAgKsyaoh8MMHq/+Ns4O34
TOrggOi9vqA4OPh7T1hPO3GK4g7c0B3qicrHkWs0U9GnfwwXfHDjsZ0u7SOZuF0f
c9as0GPx0zOdgTZ3zwIDAQAB
-----END PUBLIC KEY-----"""

if __name__ == "__main__":
    private_key_file = r'/Users/treehs/Desktop/v3/test/private.pem'
    pubkey_file = r'/home/lipeng/Desktop/work/code/packer-buffet/demos/朴食/public.pem'

    # 1. 私钥加密
    msg = 'LNoDjeXqtsVgCPhgJT5NLRNXVCb1i8zN'
    cipher_text = private_encrypt(msg, private_key_file)
    print("密文:", cipher_text)

    # 2. 公钥解密
    m2c_key = get_m2c_pub(public_key)
    # m2c_key = read_key(pubkey_file, key_type="public")
    plain_text = public_decrypt(cipher_text, m2c_key)
    print("明文: ", plain_text)

    # 3. 私钥解密
    m2c_pri_key = read_key(private_key_file, key_type="private")
    b_cipher_text = b'u5KctOktZ0BW+lCnxfp+CYQUs6e41A9v7h6++w4meL5ikEa2922IWg+IB05nzNsck14nZ6/82m//uecC/j4xgPGe5C6YiyoJ78Ll975ubAWKRQ7XDrZdvtDNnnL1gcKO5E8GzWCVSH6OUbjczoNa9RYeNEkWov+OJgzybk1m7bo='
    b_plain_text = private_decrypt(b_cipher_text, m2c_pri_key)

    print("明文: ", b_plain_text)
