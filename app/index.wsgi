# coding: UTF-8
import os
import sys 
#import sae
import web

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
 
from conversation import Conversation
from home.test import Test
from home.home import Home
from home.bind import Bind
from home.device import Device
from home.user import User
from home.power import Power
from home.flow import Flow
from home.location import Location
from home.sound import Sound
from home.feedback import Feedback
from home.service import Service

urls = (
    '/wx','Conversation',
    '/bind','Bind',
    '/home','Home',
    '/device','Device',
    '/user','User',
    '/power','Power',
    '/flow','Flow',
    '/location','Location',
    '/sound','Sound',
    '/feedback','Feedback',
    '/service','Service',
    '/test','Test',
    '/','hello'
)
 
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class hello:

    def GET(self):
        """ Show page """
        return 'hello'

app = web.application(urls, globals())

#增加session管理,将session放入全局的web.config
#if web.config.get('_session') is None:
#    m_session = web.session.Session(app, DiskStore('sessions'),
#                        initializer={'userid':0})
#    web.config._session = m_session
#else:
#    m_session = web.config._session
#def session_hook():
#    web.ctx.session = m_session
#app.add_processor(web.loadhook(session_hook))

#application = sae.create_wsgi_app(app)

if __name__ == "__main__":
    app.run()
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
