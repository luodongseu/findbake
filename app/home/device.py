# coding: UTF-8

""" 设备信息页 """

import web
import config
import sys

sys.path.append("..")
from api.common import Common
from api.apiManager import ApiManager
from const import errors


class Device:
    def GET(self):
        '''
        静态查看设备信息
        :return:
        '''
        username = Common.getLoginUsername()  # 获得登录用户名
        r, data = ApiManager.getDeviceInfo(username)  # 获取设备信息
        if r == 'fail':  # 获取设备信息失败
            if data == errors.NOT_BIND:  # 如果未绑定 则进入绑定页
                url = '/bind?username=' + username
                return web.redirect(url)
            else:  # 否则进入404
                return web.redirect('/404')
        return config.render.device(data)
