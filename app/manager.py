# coding: UTF-8

'''
硬件设备访问 入口文件
'''

import web


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
        return 'hello findbake'
