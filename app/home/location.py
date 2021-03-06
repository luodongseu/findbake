# coding: UTF-8

""" 设备位置信息页 """

import web
import config
import sys

sys.path.append("..")
from api.common import Common
from api.apiManager import ApiManager
from const import errors


class Location:
    def GET(self):
        '''
        静态查看定位信息
        :return:
        '''
        username = Common.getLoginUsername()  # 获得登录用户名
        if not username:  # 不存在则返回重定向
            return web.redirect('/404')

        input = web.input()
        if 'yesterday' in input.keys():
            r, data = ApiManager.getYesterdayLocationInfos(username)
            if r == 'success':
                return config.render.location_history(data)
            else:
                return web.seeother('/404')
        r, data = ApiManager.getDeviceLocationInfo(username)  # 获取设备定位信息
        if r == 'fail':  # 获取设备信息失败
            if data == errors.NOT_BIND:  # 如果未绑定 则进入绑定页
                url = '/bind?username=' + username
                return web.seeother(url)
            else:  # 否则进入404
                return web.seeother('/404')
        return config.render.location(data)
