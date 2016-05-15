# coding: UTF-8

'''
公共函数库
'''

import web
import time


class Common:
    @classmethod
    def islogin(self, name):
        '''
        判断用户是否登录
        :return: 登录后返回用户名 未登录直接跳转到绑定界面
        '''

        try:
            session = web.config._session  # web.ctx.session
            username = session.username
            if not username:
                return 'n', web.redirect('/home?username=' + name)
            else:
                return 'y', username
        except Exception as e:
            return 'n', web.redirect('/home?username=' + name)

    @classmethod
    def getLoginUsername(self):
        '''
        获取登录的用户名
        :return 登录用户名:
        '''
        r, d = self.islogin('')
        if r == 'y':
            return d
        else:
            return None

    @classmethod
    def addsession(self, username):
        '''
        将用户名 加入session 中
        :param 用户名:
        :return:
        '''
        try:
            session = web.ctx.session
            session.username = username
        except Exception as e:
            return 'fail'

    @classmethod
    def secToStr(self, sec):
        '''
        秒数转字符串
        :param sec:
        :return:
        '''
        return time.strftime("%Y年%m月%d日% H:%M:%S", time.localtime(sec))

    @classmethod
    def secToLast(self, sec):
        '''
        计算多少时间前
        :param sec:
        :return:
        '''
        if sec == 0 or sec == None:  # 时间参数错误
            return '未知时间'
        n = time.time()  # 当前秒数
        d = n - sec  # 时间差
        if d <= 3:
            '''3秒内 即为刚刚'''
            return '刚刚'
        elif d < 60:
            '''1分钟内 即为多少秒前 '''
            return d + '秒前'
        elif d < 60 * 60:
            '''1小时内 即为几分钟前'''
            return d / 60 + '分钟前'
        elif d < 60 * 60 * 24:
            '''1天内 即为多少小时前'''
            return d / 60 / 60 + '小时前'
        else:
            '''1天以上 即多少天前'''
            return d / 60 / 60 / 24 + '天前'
