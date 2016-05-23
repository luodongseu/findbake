# coding: UTF-8

'''
接口控制中心
'''

import time
import web
from common import Common

import sys

sys.path.append("..")
from home import config
from const import errors
from const import orders

Db = config.db  # 数据库操作对象


class ApiManager:
    @classmethod
    def getusernamebyimei(self, imei):
        '''
        通过imei号获取用户名
        :param imei:
        :return:
        '''
        if not imei:
            return 'fail', errors.ERROR_PARAM
        r = Db.select('t_user', where="imei=$imei", vars=locals(), limit=1)  # 查询当前设备信息
        if not r:  # 无设备
            return 'fail', errors.NO_DEVICE
        else:
            d = r[0]
            return 'success', d['wx_name']

    @classmethod
    def binddevicebyimei(cls, devicecode, imei):
        '''
        通过imei号绑定设备
        :param dqr:设备二维码
        :param imei:手机imei号
        :return:
        '''
        if not imei or not devicecode:
            return 'fail', errors.ERROR_PARAM
        t = time.time()  # 当前绑定时间
        r = Db.select('t_device', where="code=$devicecode", vars=locals(), limit=1)  # 检查devicecode是否存在
        if not r:  # 不存在设备code
            return 'fail', errors.NO_DEVICE

        d = r[0]  # 取出第一个设备为当前设备
        r1 = Db.select('t_user', where="imei=$imei", vars=locals(), limit=1)  # 查询当前用户是否存在
        if r1:  # 用户已经存在了,则更新绑定
            Db.update('t_user', where="imei=$imei", vars=locals(), device_id=d['id'], bind_time=t)
            return 'success', ''
        else:  # 没有用户信息,则新建用户信息
            name = 'Mobile_A_' + int(t)  # '''随机生成用户名'''
            Db.insert('t_user', imei=imei, wx_name=name, device_id=d['id'], bind_time=t)
            return 'success', ''

    @classmethod
    def registerDevice(self, ccid, code, qrcodeurl):
        '''
        注册设备信息
        :param code:    设备CCID号
        :return:
        '''
        if not code:
            return 'fail', errors.ERROR_PARAM
        t = time.time()  # 当前时间
        Db.insert('t_device', ccid=ccid, code=code, qr=qrcodeurl, create_time=t)
        return 'success', ''

    @classmethod
    def refreshDeviceInfo(self, ccid, data):
        '''
        (1)更新设备信息

        :param code:
            设备CCID号
        :param data:
            gps:latitude longitude
            power: \d
        :调用者: 设备
        :return:
        '''
        if not ccid or not data:
            return 'fail', errors.ERROR_PARAM
        t = time.time()  # 当前时间
        ds = Db.select('t_device', where="ccid=$ccid", vars=locals(), limit=1)  # 查询当前设备信息
        if not ds:
            return 'fail', errors.NO_DEVICE  # 如果没有设备信息 则跳出
        d = ds[0]  # 第一个数据就是当前设备
        Db.insert('t_device_attribute', device_id=d['id'], gps=data['gps'], power=data['power'], time=t)
        '''
        (2)查询待执行指令
        '''
        os = Db.select('t_order_quene', what="code", where="status=1 and device_id=$d['id']",
                       vars=locals())  # 查询当前设备未执行的指令
        if not os:
            return 'success', None  # 如果没有指令未执行,则返回空字符串
        r = ''  # 返回的指令字符串
        codes = []  # 存储不同的指令
        for o in os:

            code = o.code
            if code in codes:  # 如果指令已存在,则跳过
                continue
            else:  # 否则加入codes中待判断
                codes.append(code)

            if code == orders.OPEN_SOUND:  # 打开声音
                Db.update('t_device', where="id=$d['id']", vars=locals(), sound=2)
            elif code == orders.CLOSE_SOUND:  # 关闭声音
                Db.update('t_device', where="id=$d['id']", vars=locals(), sound=1)
            elif code == orders.REFRESH_RATE_REST:  # 重置频率
                Db.update('t_device', where="id=$d['id']", vars=locals(), delay=30)
            elif code == orders.REFRESH_RATE_HIGH:  # 提高频率
                Db.update('t_device', where="id=$d['id']", vars=locals(), delay=15)
            r = r + code + ','  # 拼接指令,以逗号隔开
        Db.update('t_order_quene', where="device_id=$d['id']", vars=locals(), status=2)  # 将队列中所有当前设备的指令全部更新为完成
        return 'success', r

    @classmethod
    def sendOrder(self, deviceid, order):
        '''
        向设备发送指令
        :param deviceid:
            设备ID
        :param order:
            指令编码 example:C1 S1
        :调用者 用户
        :return 'success/fail d':
        '''
        if not deviceid or not order:
            return 'fail', errors.ERROR_SYSTEM
        t = time.time()  # 当前指令创建时间
        Db.insert('t_order_quene', device_id=deviceid, code=order, status=1, time=t)  # 将指令压入指令队列中
        return 'success', ''

    @classmethod
    def bindDevice(self, username, devicecode):
        '''
        用户与设备绑定
        :param username:
            微信用户提供的用户名
        :param devicecode:
            用户扫描的二维码提供的code
        :return 'success/fail d':
        '''
        if not username or not devicecode:
            return 'fail', errors.NOT_BIND
        t = time.time()  # 当前绑定时间
        r = Db.select('t_device', where="code=$devicecode", vars=locals(), limit=1)  # 检查devicecode是否存在
        if not r:  # 不存在设备code
            return 'fail', errors.NO_DEVICE
        d = r[0]  # 取出第一个设备为当前设备
        r1 = Db.select('t_user', where="wx_name=$username", vars=locals(), limit=1)  # 查询当前用户是否存在
        if r1:  # 用户已经存在了,则更新绑定
            Db.update('t_user', where="wx_name=$username", vars=locals(), device_id=d['id'], bind_time=t)
            return 'success', ''
        else:  # 没有用户信息,则新建用户信息
            Db.insert('t_user', wx_name=username, device_id=d['id'], bind_time=t)
            return 'success', ''

    @classmethod
    def login(self, username):
        '''
        用户进入首页时登录
        :param username:
            微信用户提供的用户名
        :return 'success/fail d':
        '''
        if not username:
            return 'fail', errors.NOT_BIND
        t = time.time()  # 当前登录时间
        r = Db.select('t_user', where="wx_name=$username", vars=locals(), limit=1)  # 查询当前用户是否存在
        if not r:  # 用户不存在,即未绑定,则跳转绑定
            return 'fail', errors.NOT_BIND
        u = r[0]  # 取出第一个用户为当前用户
        ip = web.ctx.ip  # 这个得到客户端ip
        if not ip:
            ip = '0.0.0.0'
        Db.insert('t_user_attribute', user_id=u['id'], ip=ip, time=t)  # 返回ID
        return 'success', username

    @classmethod
    def getDeviceInfo(self, username):
        '''
        用户查看设备信息
        :param username:
            微信用户提供的用户名
        :return 'res[]/fail d':
        '''
        if not username:
            return 'fail', errors.NOT_BIND
        r = Db.select('t_user', where='wx_name = $username', vars=locals(), limit=1)  # 查看用户是否已绑定
        if not r:  # 用户还未绑定设备
            return 'fail', errors.NOT_BIND
        u = r[0]  # 取出第一个用户为当前用户
        r1 = Db.select('t_device', where="id=$u['device_id']", vars=locals(), limit=1)  # 获取设备基本信息
        if not r1:  # 如果设备不存在,则为系统错误
            return 'fail', errors.ERROR_SYSTEM
        d = r1[0]  # 取出第一个设备作为当前设备
        res = dict()  # 返回结果的字典
        res['id'] = d['id']  # 设备ID
        res['ct'] = Common.secToStr(d['create_time'])  # 生产日期
        res['bs'] = '已绑定'  # 绑定状态
        res['rf'] = d['delay']  # 收集数据频率

        r2 = Db.select('t_device_attribute', what='count(*)', where="device_id=$d['id']", vars=locals())  # 获取上传次数
        if not r2:
            res['count'] = 0  # 上传次数
            res['last'] = 0  # 最后一次上传时间
        else:
            res['count'] = r2[0]['count(*)']  # 上传次数
            r3 = Db.select('t_device_attribute', where="device_id=$d['id']", vars=locals(), order="time desc",
                           limit=1)  # 获取最后一个记录
            res['last'] = Common.secToLast(r3[0].time)  # 最后一次上传时间
        return 'success', res

    @classmethod
    def getSoundStatus(self, username):
        '''
        用户获取声音状态
        :param username:
        :return:
        '''
        if not username:
            return 'fail', errors.NOT_BIND, ''
        r = Db.select('t_user', where="wx_name=$username", vars=locals(), limit=1)  # 查看用户是否已绑定
        if not r:  # 用户还未绑定设备
            return 'fail', errors.NOT_BIND, ''
        u = r[0]  # 取出第一个用户为当前用户
        r1 = Db.select('t_device', where="id=$u['device_id']", vars=locals(), limit=1)  # 获取设备基本信息
        if not r1:  # 如果设备不存在,则为系统错误
            return 'fail', errors.ERROR_SYSTEM, ''
        d = r1[0]  # 取出第一个设备作为当前设备
        s = d['sound']  # 返回的指令状态
        t = 0
        '''查看指令队列是否有未执行的指令'''
        r2 = Db.select('t_order_quene', what="code,time", where="device_id=$d['id'] and status=1", vars=locals(),
                       order="time desc", limit=1)
        if r2:
            order = r2[0]  # 取出最后的一个指令码
            t = Common.secToLast(order['time'])
            if order['code'] == orders.OPEN_SOUND:
                s = 3  # 等待打开
            elif order['code'] == orders.CLOSE_SOUND:
                s = 4  # 等待关闭
        return 'success', s, t

    @classmethod
    def getUserInfo(self, username):
        '''
        用户查看自己的基本信息
        :param username:
            微信用户提供的用户名
        :return 'res[]/fail d':
        '''
        if not username:
            return 'fail', errors.NOT_BIND
        r = Db.select('t_user', where="wx_name=$username", vars=locals(), limit=1)  # 查看用户是否已绑定
        if not r:  # 用户还未绑定设备,即用户未注册账号
            return 'fail', errors.NOT_BIND
        u = r[0]  # 取出第一个用户为当前用户
        res = dict()  # 返回结果的字典
        res['id'] = u['id']  # 用户ID
        res['bt'] = Common.secToStr(u['bind_time'])  # 绑定时间
        res['bs'] = '已绑定'  # 绑定状态

        r2 = Db.select('t_user_attribute', what='count(*)', where="user_id=$u['id']", vars=locals())  # 获取登录次数
        if not r2:
            res['count'] = 0  # 登录次数
            res['last'] = Common.secToLast(0)  # 最后一次登录时间
        else:
            res['count'] = r2[0]['count(*)']  # 登录次数
            r3 = Db.select('t_user_attribute', where="user_id=$u['id']", vars=locals(), order="time desc",
                           limit=1)  # 获取最后一个记录
            res['last'] = Common.secToLast(r3[0].time)  # 最后一次登录时间
        return 'success', res

    @classmethod
    def getDeviceLocationInfo(self, username):
        '''
        读取设备当前坐标信息
        :param username:
            微信用户提供的用户名
        :return 'res[]/fail d':
        '''
        if not username:
            return 'fail', errors.NOT_BIND
        r = Db.select('t_user', where="wx_name=$username", vars=locals(), limit=1)  # 查看用户是否已绑定
        if not r:  # 用户还未绑定设备
            return 'fail', errors.NOT_BIND
        u = r[0]  # 取出第一个用户为当前用户
        r1 = Db.select('t_device', where="id=$u['device_id']", vars=locals(), limit=1)  # 获取设备基本信息
        if not r1:  # 如果设备不存在,则为系统错误
            return 'fail', errors.ERROR_SYSTEM
        d = r1[0]  # 取出第一个设备作为当前设备
        res = dict()  # 返回结果的字典
        res['id'] = d['id']  # 设备ID

        r3 = Db.select('t_device_attribute', where="device_id=$d['id'] and gps!='-1,-1'", vars=locals(),
                       order="time desc",
                       limit=1)  # 获取最后一个记录
        if not r3:  # 返回默认坐标:北京
            res['lat'] = 0  # 经度
            res['lon'] = 0  # 纬度
            res['last'] = 0  # 最后一次上传时间
        else:
            l = r3[0]
            gps = l['gps']
            g = gps.split(',')  # 解析坐标值
            res['lat'] = g[0]  # 经度
            res['lon'] = g[1]  # 纬度
            res['last'] = Common.secToLast(l['time'])  # 最后一次上传时间
        return 'success', res

    @classmethod
    def getYesterdayLocationInfos(self, username):
        '''
        获取昨天的坐标数据集
        :param username:
            微信用户提供的用户名
        :return 'res[]/fail d':
        '''
        if not username:
            return 'fail', errors.NOT_BIND
        r = Db.select('t_user', where="wx_name=$username", vars=locals(), limit=1)  # 查看用户是否已绑定
        if not r:  # 用户还未绑定设备
            return 'fail', errors.NOT_BIND
        u = r[0]  # 取出第一个用户为当前用户

        res = []  # 返回结果的字典
        t = time.time()  # 当前时间戳
        t1 = int(t - t % 86400) + time.timezone  # 当天0点时间戳
        t2 = int(t1 + 86400)  # 昨天0点时间戳
        r1_e = Db.select('t_device_attribute',
                         what='gps', where="device_id=$u['device_id'] and time<$t2 and time>$t1",
                         vars=locals(), order='time asc')  # 获取设备昨日坐标信息
        if not r1_e:  # 返回默认坐标:0,0
            res_d = dict()
            res_d['lat'] = 0  # 经度
            res_d['lon'] = 0  # 纬度
            res.append(res_d)
        else:  # 返回坐标集合
            for g in r1_e:  # 遍历结果集
                if g['gps'] == '-1,-1':
                    continue
                g1 = g['gps'].split(',')  # 解析坐标值
                res_d = dict()
                res_d['lat'] = g1[0]  # 经度
                res_d['lon'] = g1[1]  # 纬度
                res.append(res_d)
        return 'success', res

    @classmethod
    def sendFeedback(self, username, content):
        '''
        用户发送用户反馈
        :param username:
            微信用户提供的用户名
        :param content:
            反馈内容
        :return:
        '''
        if not username or not content:
            return 'fail', errors.ERROR_PARAM
        t = time.time()  # 当前时间戳
        r = Db.select('t_user', where="wx_name=$username", vars=locals(), limit=1)  # 查看用户是否已绑定
        if not r:  # 用户还未绑定设备 此处允许匿名反馈
            # return 'fail', errors.NOT_BIND
            Db.insert('t_feedback', user_id=-1, content=content, time=t)
        else:  # 已登录的用户
            u = r[0]  # 取出第一个用户为当前用户
            Db.insert('t_feedback', user_id=u['id'], content=content, time=t)
        return 'success', ''
