import os

import requests
from framework.shortcut import APIError


def download_file(url, dir_path='', file_name=''):
    """
    下载文件到指定路径

    :param url: 文件url
    :param dir_path: 文件储存路径（文件夹）
    :param file_name: 保存的文件名字
    """
    try:
        content = requests.get(url, verify=False, timeout=3000).content
    except Exception:
        raise APIError('下载文件失败', 1)

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception:
        raise APIError(f'无法创建此路径：{dir_path}', 1)

    full_path = os.path.join(dir_path, file_name)
    with open(full_path, 'wb') as f:
        f.write(content)

    return {'code': 0}


def write_file(mch_cert_content, dir_path='', file_name=''):
    """
    写入证书内容并指定路径

    :param url: 文件url
    :param dir_path: 文件储存路径（文件夹）
    :param file_name: 保存的文件名字
    """
    # try:
    #     content = requests.get(url, verify=False, timeout=3000).content
    # except Exception:
    #     raise APIError('下载文件失败', 1)

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception:
        raise APIError(f'无法创建此路径：{dir_path}', 1)

    full_path = os.path.join(dir_path, file_name)
    with open(full_path, 'w') as f:
        f.write(mch_cert_content)

    return {'code': 0}
