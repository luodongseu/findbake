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
from const import orders
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
        # if comes from weixin return echostr
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
               "\n\nThank for your attention and use!"

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
            return '================\n常用指令:\n\n201.查看设备信息\n202.查看帐号信息\n203.查看设备当前位置\n204.打开声音\n205.关闭声音\n' \
                   '================'

        '''201命令 查看设备信息'''
        if content == '201' or "设备" in content:
            status, deviceinfo = ApiManager.getDeviceInfo(username)
            if 'fail' == status:
                if deviceinfo == errors.NOT_BIND:
                    return '================\n错误: ' + deviceinfo + \
                           '\n提示: <a href="http://luodongseu.top/bind?username=' + \
                           username + '">点我去绑定</a>\n================'
                else:
                    return deviceinfo
            else:
                '''格式化数据后返回'''
                result = '================\n===设备信息如下====\n'
                result += '1.设备ID:' + str(deviceinfo['id']) + '\n'
                result += '2.生产日期:' + str(deviceinfo['ct']) + '\n'
                result += '3.绑定状态:' + str(deviceinfo['bs']) + '\n'
                result += '4.信息上传次数:' + str(deviceinfo['count']) + '\n'
                result += '5.最后一次上传时间:' + deviceinfo['last'] + '\n================'
                return result

        '''202命令 查看用户信息'''
        if content == '202' or "我" in content or "用户" in content:
            status, userinfo = ApiManager.getUserInfo(username)
            if 'fail' == status:
                if userinfo == errors.NOT_BIND:
                    return '================\n错误: ' + userinfo + \
                           '\n提示: <a href="http://luodongseu.top/bind?username="' + \
                           username + '>点我去绑定</a>\n================'
                else:
                    return userinfo
            else:
                '''格式化数据后返回'''
                result = '================\n===用户信息如下===\n'
                result += '1.用户ID:' + str(userinfo['id']) + '\n'
                result += '2.绑定时间:' + str(userinfo['bt']) + '\n'
                result += '3.绑定状态:' + str(userinfo['bs']) + '\n'
                result += '4.登录次数:' + str(userinfo['count']) + '\n'
                result += '5.最后一次登录时间:' + userinfo['last'] + '\n================'
                return result

        '''203命令 查看位置信息'''
        if content == '203' or '位置' in content:
            status, location = ApiManager.getDeviceLocationInfo(username)
            if 'fail' == status:
                if location == errors.NOT_BIND:
                    return '================\n错误: ' + location + \
                           '\n提示: <a href="http://luodongseu.top/bind?username="' + \
                           username + '>点我去绑定</a>\n================'
                else:
                    return location
            else:
                '''格式化数据后返回'''
                result = '================\n===设备坐标如下===\n'
                result += '1.设备ID:' + str(location['id']) + '\n'
                result += '2.经度:' + str(location['lat']) + '\n'
                result += '3.纬度:' + str(location['lon']) + '\n'
                result += '4.更新时间:' + location['last'] + '\n================'
                return result

        '''204 打开声音'''
        if content == '204' or '打开声音' in content:
            status, deviceinfo = ApiManager.getDeviceInfo(username)
            if 'fail' == status:
                if deviceinfo == errors.NOT_BIND:
                    return '================\n错误: ' + deviceinfo + \
                           '\n提示: <a href="http://luodongseu.top/bind?username="' + \
                           username + '>点我去绑定</a>\n================'
                else:
                    return deviceinfo
            else:
                r, status, time = ApiManager.getSoundStatus(username)
                if str(status) == '1':
                    '''关闭状态'''
                    ApiManager.sendOrder(deviceinfo['id'], orders.OPEN_SOUND)
                    return '================\n指令发送成功,已进入等待执行队列!\n================'
                else:
                    if str(status) == '2':
                        return '================\n声音已打开,请勿重复操作!\n================'
                    else:
                        return '================\n操作正在等待执行,请稍后!\n已等待时间:'+str(time)+'\n================'

        '''205 关闭声音'''
        if content == '205' or '关闭声音' in content:
            status, deviceinfo = ApiManager.getDeviceInfo(username)
            if 'fail' == status:
                if deviceinfo == errors.NOT_BIND:
                    return '================\n错误: ' + deviceinfo + \
                           '\n提示: <a href="http://luodongseu.top/bind?username="' + \
                           username + '>点我去绑定</a>\n================'
                else:
                    return deviceinfo
            else:
                r, status, time = ApiManager.getSoundStatus(username)
                if str(status) == '2':
                    '''打开状态'''
                    ApiManager.sendOrder(deviceinfo['id'], orders.CLOSE_SOUND)
                    return '================\n指令发送成功,已进入等待执行队列!\n================'
                else:
                    if str(status) == '1':
                        '''关闭状态'''
                        return '================\n声音已关闭,请勿重复操作!\n================'
                    else:
                        return '================\n操作正在等待执行,请稍后!\n已等待时间:'+str(time)+'\n================'

        ''' 其他数据 机器人聊天 '''
        msg = urllib2.urlopen(urllib2.Request('http://www.xiaodoubi.com/simsimiapi.php?msg=' + content)).read().encode(
            'utf-8')
        return msg + '\n\n================\n回复\"菜单\"获取功能列表\n================'
