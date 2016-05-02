# coding: UTF-8

""" 设备电量信息页 """

import web
import config

class Power:
    def GET(self):
        data = web.input()
        return config.render.power(data)
