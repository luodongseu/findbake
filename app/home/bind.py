# coding: UTF-8

'''
设备绑定
用户未绑定设备时调用
'''

import web
import config

import sys

sys.path.append("..")
from weixin.jshelper import JSHelper


class Bind:
    def GET(self):
        '''
        解析步骤:
        1.获取参数username
        2.从数据库中判断username是否绑定了设备
        3.如果未绑定进入4,绑定了进入5
        4.获取参数result
        5.如果参数result存在进入6,否则显示绑定页
        6.如果result=success,显示绑定成功页;否则显示绑定失败页
        5.跳转到主页
        :return:
        '''
        input = web.input(username=None, result=None)
        username = input.username
        if not username:  # 检查用户名,如果用户名为空,提示失败
            return config.render.bindFail()
        result = input.result
        if result == None:  # 如果结果为空,表示进入绑定
            fullurl = web.ctx.homedomain + web.ctx.homepath + web.ctx.fullpath
            data = JSHelper.js_data(fullurl)  # request for js ticket from weixin
            return config.render.bindDevice(data)
        else:  # 如果结果不为空,表示展示绑定结果
            if result == 'success':
                ''' 绑定成功 '''
                return config.render.bindSuccess()
            else:
                ''' 绑定失败 '''
                return config.render.bindFail()
