#-*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import os.path
import json
import time
import re
from tornado.options import define, options

from tables import query_user, write_dish, query_menu_list, regist_user
from hostip import get_ip_address

define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class MenuHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        d = self.get_argument("day", None)
        t = time.localtime();
        timestamp = time.strftime("%Y%m%d", t)
        cur = "%4d-%02d-%02d" % (t.tm_year, t.tm_mon, t.tm_mday);
        today = {"flag":True, "date":timestamp}
        if d:
            d = str(d)
            reg = "20[0-9]{2}-[0-9]{2}-[0-9]{2}"
            if re.match(reg, d):
                timestamp = d
                today = {"flag":False, "date":d}
        if cur == d:
            today['flag'] = True 
        data = query_menu_list(timestamp)
        ip = get_ip_address("eth0")
        hostip = "http://" + str(ip)+":"+str(options.port)
        uname = self.get_secure_cookie("username")
        res = {}
        res['time']      = today
        res['serverip']  = hostip
        res['username']  = uname
        res['data']      = data
        print res
        #self.render("menu.html", today=today, data=data, host_ip=hostip, username=uname)
class UploadFileHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("up.html");
    #@tornado.web.authenticated
    def post(self):
        if not os.path.exists("static/files"):
            os.makedirs("static/files");
        timestamp = time.strftime("%Y%m%d", time.localtime());
        todaydir = "static/files/" + timestamp
        if not os.path.exists(todaydir):
            os.makedirs(todaydir)
        upload_path = os.path.join(os.path.dirname(__file__), todaydir)
        file_metas  = self.request.files['file']
        names = {}
        for meta in file_metas:
            filename = meta['filename']
            names[filename] = todaydir + '/' +  filename + '\3' + timestamp
            filepath = os.path.join(upload_path, filename)
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
        write_dish(**names)
        self.write('上传成功!')
class StaticHandler(BaseHandler):
    def get(self, htmlfile):
        uname = self.get_cookie("username")
        self.render(htmlfile + ".html", username=uname)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        uname = self.get_argument("username")
        upass = self.get_argument("password")
        ret = query_user(uname + '\3' + upass)
        if not ret:
            self.render("failed_log.html")
        else:
            self.set_secure_cookie("username", uname)
            self.set_secure_cookie("role", ret)
            self.redirect("/welcome")
class WelcomeHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        uname = self.get_secure_cookie("username")
        role  = self.get_secure_cookie("role")
        self.render("success_log.html", username=uname, role=role)
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("username");
        self.clear_cookie("role");
        self.redirect("/")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login" }
    handler = [(r'/menu', MenuHandler),
               (r'/', IndexHandler),
               (r'/welcome', WelcomeHandler),
               (r'/login', LoginHandler),
               (r'/up', UploadFileHandler),
               (r'/menu', MenuHandler),
               (r'/logout', LogoutHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
