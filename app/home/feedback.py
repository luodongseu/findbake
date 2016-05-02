# coding: UTF-8

""" 用户反馈页 """

import web
import config
# Templates
import sys

sys.path.append("..")


class Feedback:
    def GET(self):
        return config.render.feedback()

    def POST(self):
        input = web.input()
        ''' 处理得到的反馈内容 '''
        ''' 保存到数据库中 '''
        return input
