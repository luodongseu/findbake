# coding: UTF-8

""" 设备信息页 """

import web
import config
# Templates
import sys

sys.path.append("..")


class Device:
    def GET(self):
        data = web.input()
        return config.render.device(data)
