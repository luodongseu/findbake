# -*- coding: utf-8 -*-

'''
out of date

no use at all and will not update
@author luodong 16/4/14
'''


import hashlib
import home
import lxml
import time
import os
import urllib2,json
from lxml import etree

class WeiXin:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = home.template.render(self.templates_root)

    def wx_token(self):
        APPID=u'wx0967ed045660afe4'
    	SECRET=u'3c6d8e04e4cf66599d5dbc6a8b96b2d2'
        url = r'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+APPID+'&secret='+SECRET
        resp = urllib2.urlopen(url)
        token = json.loads(resp.read())
        return token['access_token']

    def GET(self):
        #获取输入参数
        data = home.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="luodongseu" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = home.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType == "![CDATA[text]]":
            return self.render.reply_text(fromUser,toUser,int(time.time()),content)
