# coding: UTF-8

""" 设备声音控制页 """

import web
import config


class Sound:
    def GET(self):
        data = web.input()
        status = 1
        return config.render.sound(data, status)
