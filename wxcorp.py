#-*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import os.path
import json
import time
from tornado.options import define, options

from tables import query_user, write_dish, query_menu_list, regist_user

define("port", default=8000, help="run on the given port", type=int)

class MenuList(tornado.web.RequestHandler):
    def get(self):
        d = self.get_argument("d")
        if not d:
            timestamp = time.strftime("%Y%m%d", time.localtime())
        else:
            a = d.split('-')
            timestamp = "%4d%02d%02d"%(int(a[0]), int(a[1]), int(a[2]))
        data = query_menu_list(timestamp)
        res = {"list": data}
        res = str(res)
        line = "menu_list_display(%s);"%res
        self.write(line)
class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("up.html");
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
class StaticHandler(tornado.web.RequestHandler):
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
            self.set_cookie("username", uname)
            self.render("success_log.html")
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("username");
        self.redirect("/")
class RegistHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("regist.html")
    def post(self):
        uname = self.get_argument("username")
        upass = self.get_argument("password")
        ret = regist_user(uname + '\3' + upass)
        self.render("regist_stat.html", ret=ret)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login" }
    handler = [(r'/menu/(today)', StaticHandler),
               (r'/menu/(order)', StaticHandler),
               (r'/', IndexHandler),
               (r'/login', LoginHandler),
               (r'/up', UploadFileHandler),
               (r'/menu_list', MenuList),
               (r'/regist', RegistHandler),
               (r'/logout', LogoutHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
