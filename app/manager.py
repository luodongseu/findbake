# coding: UTF-8

'''
硬件设备访问 入口文件
'''

import web
from api.apiManager import ApiManager


class Manager:
    def GET(self):
        '''
        设备访问GET请求
        :return:
        '''
        input = web.input(data=None)
        return 'hello world:' + input.data

    def POST(self):
        '''
        设备访问POST请求
        :return:
        '''
        input = web.input(ccid=None, gps=None, power=None)
        ccid = input.ccid
        gps = input.gps
        power = input.power
        if not ccid or not gps:
            return 'fail'
        if not power or power not in [0, 100]:
            power = 100
        d = {
            'gps': gps,
            'power': power
        }
        r, m = ApiManager.refreshDeviceInfo(ccid, d)
        if r == 'success':
            return m
        else:
            return 'success'
