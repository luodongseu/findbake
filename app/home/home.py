# coding: UTF-8

""" 主页 """
import web
import config

# Templates
import sys

sys.path.append("..")

from weixin.jshelper import JSHelper


class Home:
    def GET(self):
        """ Show home page """
        # input = web.input()
        data = JSHelper.js_data(web.ctx.homedomain + web.ctx.homepath + web.ctx.fullpath)
        return config.render.home(data)
