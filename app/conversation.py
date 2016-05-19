# coding: UTF-8
'''
app 入口文件
'''

import urllib2
import hashlib
import web
from weixin import handler as HD
from api.apiManager import ApiManager
from api.common import Common
from const import errors
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Conversation:
    def GET(self):
        # get wexin input params
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # self token
        token = "luodongseu"
        # sort by list
        l = [token, timestamp, nonce]
        l.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, l)
        hashcode = sha1.hexdigest()
        # sha1 password
        # ...
        #if comes from weixin return echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        """公众平台对接"""
        # get input data
        data = web.data()
        handler = HD.MessageHandle(data)
        response = handler.start()
        return response

    @HD.subscribe
    def subscribe(xml):
        return "Welcom to FINDBAKE!We are created for your lovely bike remote controlling and locating!回复'菜单'获取操作指南" \
               "\n\nWe are trying best to build a better world with little lost accident!" \
               "\n\nThank for your attention and use!" \
               "\n\nPlease click url <a href='http://www.baidu.com'>Manage Page</a> to jump to management page!"

    @HD.unsubscribe
    def subscribe(xml):
        print("leave")
        return "Thanks for your time and use! May you happy a lot!"

    @HD.text
    def text(xml):
        content = xml.Content
        username = xml.FromUserName

        if content == "菜单":
            return '================\n请回复序号:\n\n101:进入控制台\n102:获取操作命令词\n103+内容:发送反馈信息\n================'

        '''101命令 子菜单1'''
        if content == "101" or "控制" in content or "controll" in content:
            return {"Title": "欢迎使用FINDBAKE控制台",
                    "Description": "FINDBAKE专注于增加每一位用户的财产安全,随时随地监控您的爱车",
                    "PicUrl": "http://luodongseu.top/static/images/console.jpg",
                    "Url": "http://luodongseu.top/home?username=" + username}

        ''' 103 反馈'''
        if content.startswith('103'):
            r, msg = ApiManager.sendFeedback(username, content[3:])
            if r == 'fail':
                return '================\nSorry:' + msg + '!\n\n感谢您的支持!\n================'
            return '================\n反馈成功!\n\n感谢您的支持!\n================'

        '''102命令 子菜单2'''
        if content == "102":
            return '================\n常用指令:\n\n201.查看设备信息\n202.查看帐号信息\n203.查看设备当前位置\n================'

        '''301命令 查看设备信息'''
        if content == '201' or "设备" in content:
            status, deviceinfo = ApiManager.getDeviceInfo(username)
            if 'fail' == status:
                if deviceinfo == errors.NOT_BIND:
                    return '================\n错误: ' + deviceinfo + \
                           '\n提示: <a href="http://120.27.125.31/bind?username=' + \
                           username + '">点我去绑定</a>\n================'
                else:
                    return deviceinfo
            else:
                '''格式化数据后返回'''
                result = '================\n======设备信息如下=======\n'
                result += '1.设备ID:' + deviceinfo['id'] + '\n'
                result += '2.生产日期:' + deviceinfo['ct'] + '\n'
                result += '3.绑定状态:' + deviceinfo['bs'] + '\n'
                result += '4.信息上传次数:' + deviceinfo['count'] + '\n'
                result += '5.最后一次上传时间:' + Common.secToLast(deviceinfo['last']) + '\n================'

        '''302命令 查看用户信息'''
        if content == '202' or "我" in content or "用户" in content:
            status, userinfo = ApiManager.getUserInfo(username)
            if 'fail' == status:
                if userinfo == errors.NOT_BIND:
                    return '================\n错误: ' + userinfo + \
                           '\n提示: <a href="http://120.27.125.31/bind?username="' + \
                           username + '>点我去绑定</a>\n================'
                else:
                    return userinfo
            else:
                '''格式化数据后返回'''
                result = '======用户信息如下=======\n'
                result += '1.用户ID:' + userinfo['id'] + '\n'
                result += '2.绑定时间:' + userinfo['bt'] + '\n'
                result += '3.绑定状态:' + userinfo['bs'] + '\n'
                result += '4.登录次数:' + userinfo['count'] + '\n'
                result += '5.最后一次登录时间:' + Common.secToLast(userinfo['last']) + '\n'
                return result
        ''' 其他数据 机器人聊天 '''
        msg = urllib2.urlopen(urllib2.Request('http://www.xiaodoubi.com/simsimiapi.php?msg=' + content)).read().encode(
            'utf-8')
        return msg + '\n\n================\n回复\"菜单\"获取功能列表\n================'
