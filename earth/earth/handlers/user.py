# -*- coding: utf-8 -*-

from handlers import BaseHandler
import tornado.web
import json,random,time,hashlib
from uuid import uuid4

from libs.verify import verID,verUrl,verPhone,verKey,verPassword,secure,md5

class RequestHandler(BaseHandler):
   async def post(self):
        phone = self.get_argument('phone')
        ip = self.request.remote_ip
        key = str(random.randint(100000,999999))

        if not verPhone(phone):
            '''invalid user input'''
            self.write(json.dumps({"flag":1})) #invalid input
            self.finish()
            return

        exist_user = await self.db.user.find_one({"phone":phone})

        if exist_user:
            Time = exist_user["keytime"]
            if (time.time()-Time)<=60:
                self.write(json.dumps({"flag":2}))
                self.finish()
                return

            await self.db.user.update_one({"phone":phone},{"$set":{"key":key,"keycount":0,"keytime":int(time.time())}})
            # TODO : send message and remove "directly return key"
            self.write(json.dumps({"flag":"success","key":key})) # key to be removed
            self.finish()
            return

        name = 'EarthMan'
        
        picnum = hashlib.md5()
        picnum.update(phone.encode("utf-8"))

        await self.db.user.insert_one({
            "_id" : str(uuid4()),
            "phone":phone,
            "vip" : False,
            "profile" : "http://www.gravatar.com/avatar/" + picnum.hexdigest() + "?f=y&d=retro",
            "nickname" : name,
            "signature" : "Nothing yet!",
            "register_time" : int(time.time()),
            "active" : 1,
            "key" : key,
            "keytime" : int(time.time()),
            "keycount" : 0,
            "money" : 0,
            "last_login" : 0,
            "ip" : ip,
            "password" : "",
            "permission" : 0,
            "level" : 0,
            "isbiz" : 0,
            "isadmin" : 0,
            "block" : 0
            })

        # TODO : send short message

        self.write(json.dumps({"flag":"success","key":key})) # key to be deleted
        self.finish()
        return  

class LoginHandler(BaseHandler):
    async def post(self):
        phone = self.get_argument('phone')
        key = self.get_argument('key')
        if self.get_current_user():
            self.write(json.dumps({'flag':7}))
            self.finish()
            return
        ip = self.request.remote_ip
        first_login  = 0

        if not(verPhone(phone)&verKey(key)&(key!="")):
            self.write(json.dumps({'flag':1}))
            self.finish()
            return

        userinfo = await self.db.user.find_one({"phone":phone})

        if not userinfo:
            self.write(json.dumps({'flag':3}))
            self.finish()
            return
        if userinfo["active"]!=1:
            self.write(json.dumps({'flag':4}))
            self.finish()
            return
        keycount = userinfo["keycount"]
        if keycount>=3:
            self.write(json.dumps({"flag":5}))
            self.finish()
            return
        await self.db.user.update_one({"phone":phone},{"$set":{"keycount":keycount+1}})
        if userinfo["key"]!=key:
            self.write(json.dumps({"flag":6}))
            self.finish()
            return

        if userinfo["last_login"] == 0:
            first_login = 1

        await self.db.user.update_one({"phone":phone},{"$set":{"key":"","keycount":0,"ip":ip,"last_login":int(time.time())}})

        new_token = self.new_token()
        self.on_login_success(new_token,userinfo["_id"])
        self.write(json.dumps({'flag':'success','first_login':first_login}))
        self.finish()
        return

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        utoken = self.get_secure_cookie('_token')
        if utoken:
            self.logout(utoken)
        self.write(json.dumps({'flag':'success'}))
        self.finish()
        return

class SetpassHandler(BaseHandler):
    @tornado.web.authenticated
    async def post(self):
        user = self.get_current_user()
        password = self.get_argument("password")
        
        if not(verPassword(password)):
            self.write(json.dumps({'flag':1})) # invalid input
            self.finish()
            return

        await self.db.user.update_one({"_id":user},{"$set":{"password":md5(password)}}) # set password

        self.write(json.dumps({'flag':'success'}))
        self.finish()
        return

class LoginwithpassHandler(BaseHandler):
    async def post(self):
        phone = self.get_argument("phone")
        password = self.get_argument("password")
        ip = self.request.remote_ip
        if self.get_current_user():
            self.write(json.dumps({'flag':7}))
            self.finish()
            return

        if not(verPhone(phone)&verPassword(password)&(password!="")):
            self.write(json.dumps({'flag':1})) # invalid input
            self.finish()
            return

        password = md5(password)
        userinfo = await self.db.user.find_one({"phone":phone})

        if not userinfo:
            self.write(json.dumps({'flag':3})) # no such user
            self.finish()
            return
        if userinfo["active"]!=1:
            self.write(json.dumps({'flag':4})) # user not activated
            self.finish()
            return

        keycount = userinfo["keycount"]
        if keycount>=3:
            self.write(json.dumps({'flag':5}))
            self.finish()
            return
        await self.db.user.update_one({"phone":phone},{"$set":{"keycount":keycount+1}})
        if userinfo["password"] != password:
            self.write(json.dumps({'flag':6}))
            self.finish()
            return

        if userinfo["last_login"] == 0:
            first_login = 1
        else:
            first_login = 0

        await self.db.user.update_one({"phone":phone},{"$set":{"key":"","keycount":0,"ip":ip,"last_login":int(time.time())}})

        new_token = self.new_token()
        self.on_login_success(new_token,userinfo["_id"])
        self.write(json.dumps({'flag':'success','first_login':first_login}))
        self.finish()
        return

class InfoHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        info = await self.db.user.find_one({"_id" : self.current_user},{
            "key" : 0,
            "keytime" : 0,
            "keycount" : 0,
            "ip" : 0,
            "password" : 0,
            "location" : 0})
        info["flag"] = "success"

        self.write(json.dumps(info))
        self.finish()
        return

# view other people
class UserInfoHandler(BaseHandler):
    @tornado.web.authenticated
    async def get(self):
        uid = self.get_argument("user")
        if not verID(uid):
            self.write(json.dumps({"flag" : 1}))
            self.finish()
            return

        info = await self.db.user.find_one({"_id" : uid},{
            "phone" : 0,
            "coin" : 0,
            "register_time" : 0,
            "last_login" : 0,
            "key" : 0,
            "keytime" : 0,
            "keycount" : 0,
            "ip" : 0,
            "password" : 0,
            "location" : 0})
        if not info:
            self.write(json.dumps({"flag" : 3}))
            self.finish()
            return

        info["flag"] = "success"
        self.write(json.dumps(info))
        self.finish()
        return

class UpdateInfoHandler(BaseHandler):
    @tornado.web.authenticated
    async def post(self):
        nickname = self.get_argument('nickname')
        profile = self.get_argument('profile')
        signature = self.get_argument("signature")
        permission = self.get_argument("permission")

        signature = secure(signature)
        nickname = secure(nickname)
        if not (verUrl(profile) & (len(nickname)<=30) & (len(signature)<=100) & (permission in ["0","1","2"])):
            self.write(json.dumps({"flag" : 1})) #invalid input
            self.finish()
            return

        permission = int(permission)

        await self.db.share.update_many({"uid" : self.current_user},{"$set" : {"permission" : permission}})
        await self.db.content.update_many({"owner" : [self.current_user]},{"$set" : {"permission" : permission}})

        await self.db.user.update_one({"_id":self.current_user},{"$set":{
            "nickname" : nickname,
            "profile" : profile,
            "signature" : signature,
            "permission" : permission}})
        self.write({"flag":"success"})
        self.finish()
        return
