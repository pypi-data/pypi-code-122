#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : wechat
# @Time         : 2021/6/7 11:17 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from wechatpy.enterprise import WeChatClient as _WeChatClient


class WeChatClient(_WeChatClient):
    API_BASE_URL = 'https://qywxlocal.nesc.cn:7443/cgi-bin/'

    def __init__(self, secret, corp_id='ww3c6024bb94ecef59', access_token=None,
                 session=None, timeout=None, auto_retry=True):
        self.corp_id = corp_id
        self.secret = secret
        super().__init__(
            corp_id, access_token, session, timeout, auto_retry
        )

    def fetch_access_token(self):
        """ Fetch access token"""
        return self._fetch_access_token(
            url=f'{self.API_BASE_URL}gettoken',
            params={
                'corpid': self.corp_id,
                'corpsecret': self.secret
            }
        )
