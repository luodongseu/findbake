# coding: UTF-8

""" 设备信息页 """

import web
import config
import sys

sys.path.append("..")
from api.common import Common
from api.apiManager import ApiManager
from const import errors
from const import orders


class Device:
    def GET(self):
        '''
        静态查看设备信息
        :return:
        '''
        username = Common.getLoginUsername()  # 获得登录用户名
        if not username:  # 不存在则返回重定向
            return web.redirect('/404')

        r, data = ApiManager.getDeviceInfo(username)  # 获取设备信息
        if r == 'fail':  # 获取设备信息失败
            if data == errors.NOT_BIND:  # 如果未绑定 则进入绑定页
                url = '/bind?username=' + username
                return web.redirect(url)
            else:  # 否则进入404
                return web.redirect('/404')
        return config.render.device(data)

    def POST(self):
        '''
        接收指令
        :return:
        '''
        input = web.input(delay=None)
        delay = input.delay
        if not delay:
            return 'failed'
        if isinstance(delay, (int)):
            username = Common.getLoginUsername()  # 获得登录用户名
            if not username:  # 不存在则返回重定向
                return web.redirect('/404')

            r, data = ApiManager.getDeviceInfo(username)  # 获取设备信息
            if r == 'fail':  # 获取设备信息失败
                if data == errors.NOT_BIND:  # 如果未绑定 则进入绑定页
                    url = '/bind?username=' + username
                    return web.redirect(url)
                else:  # 否则进入404
                    return web.redirect('/404')
            else:  # 成功获取信息
                if delay > 15:
                    ApiManager.sendOrder(data['id'], orders.REFRESH_RATE_REST)  # 发送S_X指令'F_' + str(delay)
                else:
                    ApiManager.sendOrder(data['id'], orders.REFRESH_RATE_HIGH)  # 发送S_X指令'F_' + str(delay)
                return 'success'
        return 'fail'
