# coding: utf-8
import json
import os
import time
import uuid

from simplepy import IS_WINDOWS

if IS_WINDOWS:
    import winreg

import requests

import nacos
from simplepy import IS_WINDOWS, logger, IS_LINUX
from simplepy.multi_download import StreamDown
from simplepy.utils import unzip_file, get_cmd_print
from simplepy.utils import request_post
from multiprocessing import freeze_support


def get_base_chrome_driver(version):
    data = [
        {
            "name": "chromedriver_linux64.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_linux64.zip",
        },
        {
            "name": "chromedriver_mac64.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_mac64.zip",
        },
        {
            "name": "chromedriver_mac64_m1.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_mac64_m1.zip",
        },
        {
            "name": "chromedriver_win32.zip",
            "url": f"https://registry.npmmirror.com/-/binary/chromedriver/{version}chromedriver_win32.zip",
        }
    ]
    return data


def get_chrome_driver():
    html = requests.get('https://registry.npmmirror.com/-/binary/chromedriver/').json()
    main_version = get_chrome_version()[1]
    result = list(filter(lambda x: str(x.get('name')).startswith(main_version), html))[0].get('name')
    if IS_WINDOWS:
        plat_name = "chromedriver_win32.zip"
    elif IS_LINUX:
        plat_name = 'chromedriver_linux64.zip'
    else:
        plat_name = 'chromedriver_mac64_m1.zip'
    download_info = list(
        filter(lambda x: x.get("name") == plat_name, get_base_chrome_driver(result))
    )[0]
    download_url = download_info.get('url')
    download_name = download_info.get('name')
    return download_url, download_name


def download_chrome_driver(path):
    download_url, download_name = get_chrome_driver()
    sd = StreamDown(download_url, download_name, path, 20)
    sd.multi_down()
    file_name = os.path.join(path, download_name)
    unzip_file(file_name, path)
    if not IS_WINDOWS:
        logger.info('可执行文件')
        os.system(f'chmod 777 {file_name}')


def get_chrome_version():
    """
    https://blog.csdn.net/sinat_41870148/article/details/109263847
    :return:
    """
    try:
        if IS_WINDOWS:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
            chrome_version = winreg.QueryValueEx(key, 'version')[0]
            return chrome_version, chrome_version.split('.')[0]
        elif IS_LINUX:
            # linux Google Chrome 102.0.5005.61
            chrome_version = get_cmd_print('google-chrome --version').split()[-1]
            return chrome_version, chrome_version.split('.')[0]
        else:
            # mac os
            # https://superuser.com/questions/1144651/get-chrome-version-from-commandline-in-mac
            chrome_version = get_cmd_print(
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version'
            ).split()[-1]
            return chrome_version, chrome_version.split('.')[0]
    except Exception as e:
        logger.error("该操作系统未安装Chrome Browser", e)


def email_fetch():
    """
    临时邮箱获取
    :return:
    """
    url = 'http://24mail.chacuo.net/'
    cookie = 'Hm_lvt_ef483ae9c0f4f800aefdf407e35a21b3=1653793645; Hm_lpvt_ef483ae9c0f4f800aefdf407e35a21b3=1653793645; mail_ck=2; sid=5d7c5b0d20a2d81f6a185be60ffbb737da235054'
    data = {"data": "uawbjk62879", "type": "refresh", "arg": ""}
    result = request_post(url, data, cookie=cookie)
    print(result)


def config_callback(x):
    print(x)


def nacos_clent():
    SERVER_ADDRESSES = "192.168.12.126:8848"
    NAMESPACE = "e8d634f2-9096-4a96-8b22-ce3d0cb6a359"
    # auth mode
    client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username="nacos", password="nacos")

    # get config
    data_id = "user-api.yaml"
    group = "home"
    print(client.get_config(data_id, group))

    client.add_config_watcher(data_id, group, config_callback)


def consul_register(ip: str, port: int, method='http'):
    """
    文档
    https://www.consul.io/api-docs/agent/service
    https://www.consul.io/api-docs/agent/servicehttps://www.consul.io/api-docs/agent/check
    :param ip:
    :param port:
    :param method:
    :return:
    """
    headers = {
        'Content-Type': 'application/json'
    }
    grpc = {
        "GRPC": f'{ip}:{port}',
        "GRPCUseTLS": False,
        "Timeout": "5s",
        "Interval": "5s",
        "DeregisterCriticalServiceAfter": "5s",
    }
    http = {
        "HTTP": "http://192.168.12.56:32226/actuator/health",
        "DeregisterCriticalServiceAfter": "5s",
        # "Args": ["/usr/local/bin/check_redis.py"],
        "Interval": "5s",
        "Timeout": "5s"
    }
    body = {
        "ID": f"{ip}:{port}",
        "Name": "all-api",
        "Tags": ["primary", "v1"],
        "Address": ip,
        "Port": port,
        "EnableTagOverride": False,
        "Check": None,
        "Weights": {
            "Passing": 10,
            "Warning": 1
        }
    }
    url = 'http://192.168.12.126:8500/v1/agent/service/register'

    if method == 'http':
        body.update({'Check': http})
    else:
        body.update({'Check': grpc})
    code = requests.put(url, json=body, headers=headers).status_code
    if code == 200:
        print('success')
    else:
        print('fail')


def consul_deregister(ip, port):
    """
    取消的是name
    :param ip:
    :param port
    :return:
    """
    url = f'http://192.168.12.126:8500/v1/agent/service/deregister/{ip}:{port}'
    code = requests.put(url).status_code
    if code == 200:
        print('success')
    else:
        print('fail')


if __name__ == '__main__':
    # get_chrome_driver()
    # email_fetch()
    # freeze_support()
    # nacos_clent()
    # http://192.168.12.56:32226/actuator/health
    consul_register('192.168.12.126', 32226, 'http')
    # consul_deregister('192.168.12.126', 32226)
