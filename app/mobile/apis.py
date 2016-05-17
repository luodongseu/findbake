# coding: UTF-8

'''
移动端的API接口
'''

import web
import sys

sys.path.append("..")
from api.apiManager import ApiManager


class Apis:
    def GET(self):
        '''
        GET请求解析
        :return:
        '''
        return web.input()

    def POST(self):
        '''
        POST请求解析

        req:api方式
        :return:
        '''
        fail = dict()  # 失败码
        fail['code'] = 400

        input = web.input()
        if 'req' not in input:
            return fail
        if input.req == 'login':
            '''登录接口'''
            if 'imei' not in input:
                return fail
            else:
                return self.login(input.imei)
        if input.req == 'bind':
            '''绑定设备接口'''
            if 'imei' not in input or 'qr' not in input:
                return fail
            else:
                return self.bind(input.imei, input.qr)

        r['username'] = 'admin'
        return r

    def login(self, imei):
        '''
        登录接口
        :param imei:手机识别码
        :return:
        '''
        res = dict()
        r, m = ApiManager.getusernamebyimei(imei)
        if r == 'success':  # 执行成功
            if m:
                res['code'] = 201
                res['username'] = m
                return res
        else:
            res['code'] = 400
            res['username'] = 'null'
            return res

    def bind(self, imei, devicecode):
        '''
        绑定接口
        :param imei:手机识别码
        :param devicecode:设备二维码
        :return:
        '''
        res = dict()
        r, m = ApiManager.binddevicebyimei(devicecode, imei)
        if r == 'success':
            r, m = ApiManager.getusernamebyimei(imei)
            if r == 'success':  # 执行成功
                if m:
                    res['code'] = 201
                    res['data'] = m
                    return res
            else:
                res['code'] = 400
                res['data'] = 'null'
            return res
        else:
            res['code'] = 401
            res['data'] = m.encode("UTF-8")
            return res
