# coding: UTF-8

""" 设备位置信息页 """

import web
import config


class Location:
    def GET(self):
        data = web.input()
        if 'yesterday' in data.keys():
            return config.render.location_history(data)
        return config.render.location(data)
