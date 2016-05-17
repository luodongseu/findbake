# coding: UTF-8

'''
设备绑定
用户未绑定设备时调用
'''

import web


class Api:
    def GET(self):
        '''
        GET请求解析
        :return:
        '''
        return web.input()

    def POST(self):
        '''
        POST请求解析
        :return:
        '''
        r = dict()
        r['code'] = 200
        r['username'] = 'admin'
        return r
