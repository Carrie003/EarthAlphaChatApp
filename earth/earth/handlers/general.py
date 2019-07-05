# -*- coding: utf-8 -*-

from handlers import BaseHandler
import tornado.web
import json

from libs.verify import verPhone,verKey

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write(json.dumps({"flag":"HOME"}))
        self.finish()
        return

class HomeHandler(BaseHandler):
    def get(self):
        flag = self.get_current_user()
        if flag ==None:
            self.write(json.dumps({"flag":False}))
        else:
            self.write(json.dumps({"flag":True}))
        self.finish()
        return

