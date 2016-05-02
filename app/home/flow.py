# coding: UTF-8

""" 设备流量信息页 """

import web
import config
# Templates
import sys

sys.path.append("..")
from weixin.jshelper import JSHelper


class Flow:
    def GET(self):
        input = web.input()
        data = JSHelper.js_data(web.ctx.homedomain + web.ctx.homepath + web.ctx.fullpath)
        return config.render.home(data)
