# coding: UTF-8

""" 主页 """
import web
import config

# Templates
import sys

sys.path.append("..")

from weixin.jshelper import JSHelper
from api.common import Common
from api.apiManager import ApiManager
from const import errors


class Home:
    def GET(self):
        '''
        检测是否登录
        :return:
        '''
        input = web.input(username=None)
        username = input.username
        if not username:  # 如果没有用户名参数,则进入404
            return web.redirect('/404')  # 进入404页面
        self.login(username)
        data = JSHelper.js_data(web.ctx.homedomain + web.ctx.homepath + web.ctx.fullpath)
        return config.render.home(data)

    def login(self, username):
        '''
        用户登录
        :param username:用户名
        :return:
        '''
        r, msg = ApiManager.login(username)
        if r == 'success':  # 登录成功,则将返回来的用户ID加入session
            Common.addsession(msg)
        else:
            if msg == errors.NOT_BIND:  # 未绑定
                return web.redirect('/bind?username=' + username)
            else:
                return web.redirect('/404')  # 进入404页面
