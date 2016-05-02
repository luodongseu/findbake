# coding:utf-8

import web
import json
from .lib import WeixinHelper

#session = web.config.get('_session')


class JSHelper(object):
    """微信JS SDK逻辑帮组类"""

    @classmethod
    def access_token(self):
        #token = session.ACCESS_TOKEN
        token = None
        if not token:
            data = json.loads(WeixinHelper.getAccessToken())
            token, expire = data["access_token"], data["expires_in"]
            #session.ACCESS_TOKEN = token
        return token

    @classmethod
    def jsapi_ticket(self):
        #ticket = session.JSAPI_TICKET
        ticket = None
        if not ticket:
            tk = self.access_token()
            data = json.loads(WeixinHelper.getJsapiTicket(tk))
            ticket, expire = data["ticket"], data["expires_in"]
            #session.JSAPI_TICKET = ticket
        return ticket

    @classmethod
    def js_data(self, url):
        """jsapi_ticket 签名"""
        sign = WeixinHelper.jsapiSign(self.jsapi_ticket(), url)
        return sign
