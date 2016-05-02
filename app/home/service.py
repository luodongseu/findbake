# coding: UTF-8

""" 客服服务页 """

import web
import config
# Templates
import sys

sys.path.append("..")

class Service:
    def GET(self):
        return config.render.service()
