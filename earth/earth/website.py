# -*- coding: utf-8 -*-

import os.path as path
import tornado.httpserver
import tornado.ioloop
import tornado.web

from handlers import user
from handlers import general

from tornado.options import define,options
define("port",default=8000,help="running port",type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/", general.MainHandler),
                (r"/home", general.HomeHandler),

                (r"/request", user.RequestHandler),
                (r"/info", user.InfoHandler),
                (r"/login", user.LoginHandler),
                (r"/logout", user.LogoutHandler),
                (r"/setpass", user.SetpassHandler),
                (r"/login_with_pass", user.LoginwithpassHandler),
                (r"/update_info", user.UpdateInfoHandler),
                (r"/view_user", user.UserInfoHandler),

                (r".*",tornado.web.RedirectHandler,{"url":"/"})
                ]
        settings = dict(
                cookie_secret = 'HswodAdW',
                login_url = '/home',
                debug = True
                )
        tornado.web.Application.__init__(self,handlers,**settings)

if __name__=='__main__':
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

