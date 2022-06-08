import rsa
import base64
import json


#rsa加密，通常对加密结果进行base64编码
def handle_pub_key(key):
    """
    处理公钥
    公钥格式pem，处理成以-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾的格式
    :param key:pem格式的公钥，无-----BEGIN PUBLIC KEY-----开头，-----END PUBLIC KEY-----结尾
    :return:
    """
    start = '-----BEGIN PUBLIC KEY-----\n'
    end = '-----END PUBLIC KEY-----'
    result = ''
    # 分割key，每64位长度换一行
    divide = int(len(key) / 64)
    divide = divide if (divide > 0) else divide + 1
    line = divide if (len(key) % 64 == 0) else divide + 1
    for i in range(line):
        result += key[i * 64:(i + 1) * 64] + '\n'
    result = start + result + end
    return result


def get_param(message, public_key):
    """
    处理长消息 不经过 这个处理回报下面error
    OverflowError: 458 bytes needed for message, but there is only space for 117
    :param message 消息
    :param public_key 公钥
    :return:
    """
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    crypto = b''
    divide = int(len(message) / 117)
    divide = divide if (divide > 0) else divide + 1
    line = divide if (len(message) % 117 == 0) else divide + 1
    for i in range(line):
        crypto += rsa.encrypt(message[i * 117:(i + 1) * 117].encode(), pubkey)

    crypto1 = base64.b64encode(crypto)
    return crypto1.decode()



if __name__ == '__main__':
    b = {
    "companyId ": "1000001056",
    "paramValue ": "147852369"
}
    message = json.dumps(b)
    public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBgqqTw4oBp4EKI35K6VSUMqCogsropY1voAkHrBf6AZl4kb2TdG2TfKhTzBsPBtp/3wrTAlUHO6g1qHr/FaUVQc3U1gkf/XdWWcXr+2UEfq6OJt0KdNXcBGSA1zY7Q6ndWTOGjMtSdvbkC0VoFP4T6+AZRHwehpK52rr+aEVKNQIDAQAB"
    public_key = handle_pub_key(public_key)
    param = get_param(message, public_key)
    print(param)