# coding: UTF-8

""" 主页 """
import web
import config

# Templates
import sys

sys.path.append("..")
from weixin.jshelper import JSHelper
#from sae import channel


class Home:
    def GET(self):
        """ Show home page """
        input = web.input()
        data = JSHelper.js_data(web.ctx.homedomain + web.ctx.homepath + web.ctx.fullpath)
	#        url = channel.create_channel('ld')
        #data['url'] = url

        return config.render.home(data)
