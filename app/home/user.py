# coding: UTF-8

""" 账号信息页 """

import web
import config
import sys

sys.path.append("..")
from api.common import Common
from api.apiManager import ApiManager
from const import errors


class User:
    def GET(self):
        '''
        静态查看用户基本信息
        :return:
        '''

        r, username = Common.getLoginUsername()  # 获得登录用户名
        if r == 'n':  # 不存在则返回重定向
            return username
        return username
        # r, data = ApiManager.getUserInfo(username)  # 获取设备信息
        # if r == 'fail':  # 获取设备信息失败
        #     if data == errors.NOT_BIND:  # 如果未绑定 则进入绑定页
        #         return web.redirect('/bind?username=' + username)
        #     else:  # 否则进入404
        #         return web.redirect('/404')
        # return config.render.user(data)
