# coding: UTF-8

'''
公共函数库
'''

import web


class Common:
    def islogin(self):
        '''
        判断用户是否登录
        :return: 登录后返回用户名 未登录直接跳转到绑定界面
        '''

        try:
            session = web.ctx.session
            username = session.username
            if not username:
                return web.redirect('/bind')
            else:
                return username
        except Exception as e:
            return web.redirect('/bind')

    def getLoginUsername(self):
        '''
        获取登录的用户名
        :return:
        '''
        return self.islogin()
