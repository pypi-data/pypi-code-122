# -*- coding: utf-8 -*-
# @Time    : 2022/5/6 10:33
# @Author  : xuyiqing
# @FileName: loadbalanced.py
import re
import random
import time

import requests

from nacos_app.service import NacosServerInstance


class LoadBalanced(NacosServerInstance):
    """
    url = "http://service-name/api/test"
    """

    def __init__(self, **kwargs):
        super(LoadBalanced, self).__init__(**kwargs)
        self.instance_map = {}
        # 在内存中缓存服务实例信息
        self.cache = self.instance_info_cache is None or self.instance_info_cache is True
        self.expire = int(kwargs.get("expire") or 0) or 1800

    def service_url(self, url):
        instance_names = re.findall("http[s]?://(.+?)/.+", url)
        if instance_names:
            instance_name = instance_names[0]
        else:
            raise Exception("{} url错误, 无法解析出服务名称".format(url))

        instance = None
        if self.cache:
            instance_cache = self.instance_map.get(instance_name)
            if instance_cache:
                create_at = instance_cache.get("create_at")
                if (time.time() - create_at) <= self.expire:
                    instance = instance_cache.get("instance")
        if not instance:
            instances = self.get_instances(instance_name)
            if not instances:
                raise Exception("{} 服务无法发现".format(instance_name))
            instance = random.sample(instances, 1)[0]
            if self.cache:
                self.instance_map.update({
                    instance_name: {"create_at": time.time(), "instance": instance}
                })
        url = url.replace(instance_name, instance.host, 1)
        return url

    def request(self, method, url, params=None, body=None):
        url = self.service_url(url)
        return requests.request(method, url, params=params, json=body).json()

    def get(self, url, params=None):
        url = self.service_url(url)
        return requests.get(url, params=params).json()

    def post(self, url, body, params=None):
        url = self.service_url(url)
        return requests.post(url, json=body, params=params).json()

    def formpost(self, url, form, params=None):
        url = self.service_url(url)
        return requests.post(url, data=form, params=params).json()
