# coding: UTF-8
'''
硬件设备访问 入口文件
'''

import web
import config

import sys

sys.path.append("..")

from weixin.jshelper import JSHelper
from api.common import Common
from api.apiManager import ApiManager
from const import errors


class Manager:
    def GET(self):
        '''
        设备访问GET请求
        :return:
        '''
        return 'hello world'

    def POST(self):
        '''
        设备访问POST请求
        :return:
        '''
        return 'hello findbake'
