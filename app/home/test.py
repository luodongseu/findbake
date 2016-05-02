import web

from home import config


class Test:

    def GET(self):
        """ Show page """
        test = web.input()
        return config.render.test(test)


    def POST(self):
        """ Show page """
        test = web.input()
        return config.render.test(test)

