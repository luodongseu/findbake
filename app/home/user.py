# coding: UTF-8

""" 账号信息页 """

import web
import config
# Templates


class User:

    def GET(self):
        data = web.input()
        return config.render.user(data)
