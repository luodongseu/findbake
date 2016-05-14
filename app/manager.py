# coding: UTF-8

'''
硬件设备访问 入口文件
'''

import web
import time
import urllib2
import json

from api.apiManager import ApiManager
from const import errors


class Manager:
    def GET(self):
        '''
        设备访问GET请求
        :return:
        '''
        return '{201:S_O}'
        input = web.input(data=None, lat=None, lon=None, ccid=None)
        data = input.data  # 数据类型 -1/0/1...
        # return '{'+data+'}'
        ccid = input.ccid  # 设备号
        # return '{'+ccid+'}'
        if not ccid:
            return '{401}'  # 参数不全
        if data != 1:
            '''数据不可用,单独处理'''
            d = {
                'gps': '-1,-1',
                'power': '100'
            }
        else:
            '''处理数据:格式化坐标数据记录数据'''
            lat = input.lat  # 经度
            latd = int(lat[0:2])
            latf = float(lat[3:])
            lat = str(latd) + '.' + str(latf / 60)
            lon = input.lon  # 纬度
            lond = int(lon[0:1])
            lonf = float(lon[2:])
            lon = str(lond) + '.' + str(lonf / 60)
            if not lat:
                lat = '-1'
            if not lon:
                lon = '-1'
            gps = lat + ',' + lon
            d = {
                'gps': gps,
                'power': '100'
            }
        r, m = ApiManager.refreshDeviceInfo(ccid, d)
        if r == 'success':  # 执行成功
            if not m:
                return '{200}'
            else:
                return '{201:' + m + '}'  # 返回格式:{201:order,order...}
        else:  # 执行失败
            if m == errors.NO_DEVICE:  # 错误原因:没有设备
                '''插入设备,并在线生成二维码'''
                t = time.time()  # 当前时间
                code = 'FB_D_N' + str(t)  # 设备编号
                '''二维码 基于百度API'''
                url = 'http://apis.baidu.com/3023/qr/qrcode?size=12&qr=' + code
                req = urllib2.Request(url)
                req.add_header("apikey", "af9772bd7a226ec2da6055f47ad0d2c1")
                resp = urllib2.urlopen(req)
                content = resp.read()
                if content:
                    qrurl = json.loads(content)['url']  # 解析json
                    if not qrurl:
                        return '{402}'  # 生成二维码失败
                ApiManager.registerDevice(ccid, code, qrurl)
            else:
                return '{403}'  # 刷新失败,未知错误原因
        return '{200}'

    def POST(self):
        '''
        设备访问POST请求
        :return:
        '''
        input = web.input(ccid=None, gps=None, power=None)
        ccid = input.ccid
        gps = input.gps
        power = input.power
        if not ccid or not gps:
            return '{-fail}'  # POST请求失败
        if not power or power not in [0, 100]:
            power = 100
        d = {
            'gps': gps,
            'power': power
        }
        r, m = ApiManager.refreshDeviceInfo(ccid, d)
        if r == 'success':
            return '{-' + m + '}'  # POST请求成功,并返回指令数据
        else:
            return '{-success}'  # POST请求成功
