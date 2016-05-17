# coding: UTF-8
import os
import sys
import web

abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)
 
from conversation import Conversation
from manager import Manager
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
from mobile.api import Api

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
    '/404','Wrong',
    '/','Manager'
    '/mobile/api','Api'
)
web.config.debug=False

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Wrong:
    def GET(self):
        """ Show 404 page """
        return render.f()



#在应用处理器中加入session
#if web.config.get("_session") is None:
#    from web import utils
#    store = web.session.DiskStore(os.path.join(abspath,'sessions'))
#    session = web.session.Session(app, store,initializer={"username": "ld"})
#    web.config._session = session
#else:
#    session = web.config._session
# session = web.session.Session(app, web.session.DiskStore(os.path.join(abspath,'sessions')), initializer={'username': None})
#

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore(os.path.join(abspath,'sessions')), initializer={'username': 'LD'})
# web.config._session = session

def session_hook():
    web.ctx.session = session
app.add_processor(web.loadhook(session_hook))

#application = sae.create_wsgi_app(app)

application = app.wsgifunc()
