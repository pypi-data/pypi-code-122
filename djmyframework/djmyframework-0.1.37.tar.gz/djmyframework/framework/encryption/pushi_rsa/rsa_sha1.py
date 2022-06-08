import base64

from Crypto.Hash import SHA
from Crypto.IO import PKCS8
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import oid, _import_keyDER
from Crypto.Signature import PKCS1_v1_5


def import_pkcs8(encoded, passphrase=None):
    k = PKCS8.unwrap(encoded, passphrase)
    if k[0] != oid:
        raise ValueError("No PKCS#8 encoded RSA key")
    return _import_keyDER(k[1], passphrase)


def rsa_pkcs8_hex_sign(hex_key, data):
    """
    16进制-pkcs#8-RSA
    pkcs#8 获取秘钥

    对应的的java的rsa加密
    byte[] keyBytes =  hexStrToBytes(hexKey);
    PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(keyBytes);
    KeyFactory keyFactory = KeyFactory.getInstance(KEY_ALGORITHM);
    PrivateKey privateKey = keyFactory.generatePrivate(keySpec);

    :param hex_key: 16进制的秘钥
    :param data: 原始报文
    :return: 16进制密文

    案例
    hex_key: 30820153020100300d06092a864886f70d01010105000482013d308201390201000241008a49c20f28f4c99aa65316a62c5d153f2fcbb2a06ec1fbcbcd609d1758615d0cecfc6d9571d1f743a40cb5766e2841b7adc1374210798a48d99fdf97ddbe06df020301000102405d4f49872b2e88fe35ee68a0f5dc5522cea056c65415c64e0d257cba2ce37d81e44078f89d2069d47c930ec315569e0e7f3bdb709e5b555e18660a48d22b2c81022100d5e7f5956102d595965436c072e0d6984d4beb07aed6b84eb5bbb97ef15a379f022100a5805be7bd413ab1f8714c717903a799c62eaab29c567b1beebc1ff1c06ee8c1022056a8100fa22b79c78e0d33d92730fafedc61a3278ba725278dec2d2bc62f1c5502207b00bf4da8b7062ca77d6d57189dc2bee33063e5839432c33bd7cdd61b33530102204d652a63834ef72a642df776b8e084722ad6770d6de82544190b381dc5da673f
    """

    key_bytes = bytes.fromhex(hex_key)
    private_key = import_pkcs8(key_bytes)
    cipher = PKCS1_v1_5.new(private_key)
    h = SHA.new(data.encode())
    signature = cipher.sign(h)
    return base64.b64encode(signature).hex()


def rsa_sign(pem, data):
    private_key = RSA.importKey(pem)
    cipher = PKCS1_v1_5.new(private_key)
    h = SHA.new(data.encode())
    signature = cipher.sign(h)
    return base64.b64encode(signature).decode()


if __name__ == '__main__':
    pem = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDDGt89VqLTsDqW
0JU+tkXwElmyO6mN/mxmFEsdCjpD83rukcoiqYLaqDOTEXFRyRlUqqKMS3wgt6RZ
T8IwgGqioHvVjxXHdrt8/WdFScfeP0cytvd5X4nbcm5cEHllslI7rw+3+mtAh97T
l5sDZILGrfrtd1rDeLieObCRmwOkfIjmPQ8iVwXzGUzpkI5Vdwo40NKL4+NHHH63
X3adxQK41v+LPpzF2ju9kl18aaw4nCM0p2YIuOh2d5KD2YS5CRzOp90OZbiunRls
7oj3eyGIL0PRMtUE6elCY4e4cmYM7tuFlOFdV4I13/Fsk+RECEQvrqetm8Nh9s4d
IsIQsoBLAgMBAAECggEAQmS8n0UCOAN6jKQChcrFVgMInwyKkJWKEdrKDOHUHheX
N+RI4y7IJtyiYGPJKknC4vsGQbPWU9Pqi7IGpTauExWFzpDYmn4fI1OgdwW6jDkA
Y5O794O5iAIS6CV7Ck56iXDzamo/YUBbZanryGXF0xKVl4XMT0SfnsiG+6XCwZA/
ajd/FX5uqMfncED76Olz8QDfPbOqKzuNlWy43BKwC0y8EOigW/CfV8JK9gfI17dK
4NXXrl3dbIyn6QwiJ5Mpi2XCLeC+OQzzKAQSvFyzIqOjty92a2Ymy7cUZwdCDii0
GuwA2nTfFKMB4+kRNvs75TyY5bh02cq76PUQuEd18QKBgQDkN490+Glvo3q9+u8d
wctxORfDuYcHfhpsGHyLtnQ0eWUDreroe+zZkO+9ti98fJVqdcwiB5ptToklS+Ib
fyrJ33U1tzL9sdpAgfGxzhbaByNIN3iRoQop5DaoDN4vCL86meQIl3/AH2/F6i17
v7lhbQgC2zz1BiWIYZZjiw5kNwKBgQDa2123xIetO1GCmiRRrVgdNNZfNmyno2JB
cWGGgD3FwPCl6lvis9egwJned7/tZI5qx7W5XHMVCTCzLHy2QIizyTYIhjRnuPoU
thor8GT/LB4pQO/ljXdy8ZB8PV0O8GkuIxYRv4469wf7fpndwrmDgQJzHW0UQvtt
Ch71BDoijQKBgAMbLnytFOJMG1OSosaI6Lf1yvkDAW98q+dkve044oQEUvel2lin
tyWO73RpkmPjXjVAvTKJX/S06PD1A3LUXES7IeFFSRBi51GRczS0VWNKTZSiDKYO
xxCi5ouLAUsql0+44H2tcjOvOdo7wbq5dVB6J23ChiXfm4srqNxZ/CwpAoGANGwr
LKOEpDf7ND9bx7yvyH8pgjD1Icp+9JIF/EOniEDI49UZIVpWogjAUot4i5J0kps3
qii84CMNaT2UucsHc5kUukH7N4UVUfS0nCW+62hT6SnGzMNwAzZdl4TTT4rChuyc
kq/Bj9owLUuL65SC/z7dqVk5EYth0iKEe8gBbNkCgYEA0eqwMBoS6Ogfle0Qk7ec
HSsOnYTC1QNc5B48Y0J1T0frptLit5LuI63mYED7rfLpk1XCEb1/KrNespamQ6Q3
+L3GFlMx9HwOY1zHs7/1+Hn/zzU3AQxmwr3E1QPMC4F/BUb5dKDgNOCyMM0daAjV
EHhVik0cCJKY5Uhao+Mg8HE=
-----END PRIVATE KEY-----
    """

    plain_text = 'a123access_token123app_key123c123method123timestamp123v123'
    print(rsa_sign(pem, plain_text))

    print('##### 建行瓦片支付测试')
    plain_text = 'FT_CORPID=FTC_GJH&FT_TILEID=06CNY0001&FT_SCENARIO=GJH&SYS_TIME=20210824 10:18:58'
    pkcs8_privatekey_hex = '30820153020100300d06092a864886f70d01010105000482013d308201390201000241008a49c20f28f4c99aa65316a62c5d153f2fcbb2a06ec1fbcbcd609d1758615d0cecfc6d9571d1f743a40cb5766e2841b7adc1374210798a48d99fdf97ddbe06df020301000102405d4f49872b2e88fe35ee68a0f5dc5522cea056c65415c64e0d257cba2ce37d81e44078f89d2069d47c930ec315569e0e7f3bdb709e5b555e18660a48d22b2c81022100d5e7f5956102d595965436c072e0d6984d4beb07aed6b84eb5bbb97ef15a379f022100a5805be7bd413ab1f8714c717903a799c62eaab29c567b1beebc1ff1c06ee8c1022056a8100fa22b79c78e0d33d92730fafedc61a3278ba725278dec2d2bc62f1c5502207b00bf4da8b7062ca77d6d57189dc2bee33063e5839432c33bd7cdd61b33530102204d652a63834ef72a642df776b8e084722ad6770d6de82544190b381dc5da673f'
    print(rsa_pkcs8_hex_sign(pkcs8_privatekey_hex, plain_text))
    print('##### 建行瓦片支付测试')
