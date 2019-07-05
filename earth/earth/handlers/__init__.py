# -*- coding: utf-8 -*-

import tornado.web
import binascii,os

import motor.motor_tornado
from pymongo import MongoClient

class BaseHandler(tornado.web.RequestHandler):
    __TOKEN_LIST = {}
    __tempdb = MongoClient('127.0.0.1',27017).earth
    for i in __tempdb.user_token_list.find({}):
        __TOKEN_LIST[i["token"]] = i["userid"]
    print ("Init Finished")
    
    def __init__(self,application,request,**kwargs):
        super(BaseHandler,self).__init__(application,request,**kwargs)

    @property
    def db(self):
        #use motor db
        self._db = motor.motor_tornado.MotorClient('mongodb://127.0.0.1:27017').earth
        return self._db

    def new_token(self):
        while True:
            new_token = binascii.hexlify(os.urandom(16)).decode("utf-8")
            if new_token not in self.__TOKEN_LIST:
                return new_token

    def on_login_success(self,new_token,user_id):
        self.set_secure_cookie('_token',new_token,expires_days=365)
        exist_token = [k for k, v in self.__TOKEN_LIST.items() if user_id == v]
        if exist_token:
            exist_token = exist_token[0]
            self.__tempdb.user_token_list.remove({"token":exist_token})
            del self.__TOKEN_LIST[exist_token]
        self.__TOKEN_LIST[new_token] = user_id
        self.__tempdb.user_token_list.insert({"userid":user_id,"token":new_token})

    def logout(self,utoken):
        utoken = utoken.decode("utf-8")
        #print (utoken)
        #print (self.__TOKEN_LIST)
        if utoken in self.__TOKEN_LIST:
            del self.__TOKEN_LIST[utoken]
            self.__tempdb.user_token_list.remove({"token":utoken})
        return 1

    def get_current_user(self):
        token = self.get_secure_cookie('_token')
        if token:
            token = token.decode("utf-8")

        #print (token)
        #print (self.__TOKEN_LIST)

        if token and token in self.__TOKEN_LIST:
            user_id = self.__TOKEN_LIST[token]
            return user_id
        return None

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://earth.fireapex.com")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Max-Age', 86400)
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with,content-type')
        self.set_header('Content-type', 'application/json')
            
