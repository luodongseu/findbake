# coding: UTF-8

""" 设备声音控制页 """

import web
import config
import sys

sys.path.append("..")
from api.common import Common
from api.apiManager import ApiManager
from const import errors
from const import orders


class Sound:
    def GET(self):
        '''
        声音控制器
        静态指令执行
        :return:
        '''
        username = Common.getLoginUsername()  # 获得登录用户名
        if not username:  # 不存在则返回重定向
            return web.redirect('/404')

        input = web.input(op=None)
        op = input.op  # 操作码
        if op:
            r, d = ApiManager.getDeviceInfo(username)  # 获取设备信息
            if r == 'fail':
                if d == errors.NOT_BIND:  # 设备未绑定
                    url = '/bind?username=' + username
                    return web.redirect(url)
                else:
                    return web.redirect('/404')
            if op == 'open':  # 打开声音
                ApiManager.sendOrder(d['id'], orders.OPEN_SOUND)
            elif op == 'close':  # 关闭声音
                ApiManager.sendOrder(d['id'], orders.CLOSE_SOUND)
            else:
                '''指令错误'''
                return web.redirect('/404')
        status = ApiManager.getSoundStatus(username)
        return config.render.sound(status)
