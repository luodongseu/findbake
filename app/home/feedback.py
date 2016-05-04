# coding: UTF-8

""" 用户反馈页 """

import web
import config
import sys

sys.path.append("..")
from api.common import Common
from api.apiManager import ApiManager


class Feedback:
    def GET(self):
        '''
        静态展示反馈界面,无限制
        :return:
        '''
        return config.render.feedback()

    def POST(self):
        '''
        提交反馈信息
        :return:
        '''
        input = web.input(content=None)
        content = input.content
        ''' 处理得到的反馈内容 '''
        if not content:
            return '无反馈内容'
        ''' 保存到数据库中 '''
        username = Common.getLoginUsername()  # 获得登录用户名
        if not username:
            return '用户未登录'
        ApiManager.sendFeedback(username, content)
        return 'success'
