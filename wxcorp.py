#-*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import os.path
import json
import time
import datetime
import re
from tornado.web import StaticFileHandler
from tornado.options import define, options

from tables import query_user, write_dish, query_dish_by_day, regist_user, dish_delete
from hostip import get_ip_address

define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class MenuHandler(BaseHandler):
    @tornado.web.authenticated
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
        self.render("menu.html", today=today, data=data, host_ip=hostip, username=uname)

class UploadFileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("up.html");
    @tornado.web.authenticated
    def post(self):
        if not os.path.exists("static/files"):
            os.makedirs("static/files");
        timestamp = time.strftime("%Y%m%d", time.localtime());
        todaydir = "static/files/" + timestamp
        if not os.path.exists(todaydir):
            os.makedirs(todaydir)
        upload_path = os.path.join(os.path.dirname(__file__), todaydir)
        file_metas  = self.request.files['file']
        meta = file_metas[0]
        filename = meta['filename']
        filename = todaydir + '/' +  filename
        with open(filename, 'wb') as up:
            up.write(meta['body'])
        filename = filename + '\3' + timestamp
        dish_name     = self.get_argument('dish_name')
        dish_material = self.get_argument('dish_material')
        dish_order    = self.get_argument('dish_order')
        write_dish(filename, dish_name, dish_material, dish_order)
        self.write('上传成功!')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        uname = self.get_argument("username")
        upass = self.get_argument("password")
        ret = query_user(uname + '\3' + upass)
        if not ret:
            self.render("failed_log.html")
        else:
            print(ret)
            self.set_secure_cookie("username", uname, expires_days=None)
            self.set_secure_cookie("role", "%d"%ret,  expires_days=None)
            self.redirect("/welcome")

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        uname = self.get_secure_cookie("username")
        self.render("begin.html", username=uname)
'''
@brief:  用户查看某一天的菜谱
@param:  day= 空则取当天的菜谱 否则去具体的日期的菜谱
@return: 返回具体某一天的菜谱列表
         dish_name:       菜的名字
         average_score:   菜的平均得分
         material:        菜的食材
         order:           菜是否可以预定 0=不可以 1=可以
         pic_land:        点击菜图片的landing url, 显示该菜的详细情况
         pic_src:         菜的图片的存放位置
'''
class CanteenIndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        d = self.get_argument("day", None)
        if not d:
            now = datetime.datetime.now()
            d = now.strftime('%Y-%m-%d')
        r = query_dish_by_day(d)
        a = []
        for i in r:
            e = {}
            e['dish_name']        = i[0]
            e['average_score']    = 4.6
            e['material']         = i[3]
            e['order']            = i[4]
            e['pic_land']         = ''
            e['pic_src']          = i[1]
            e['id']               = i[-1]
            a.append(e)
        uname = self.get_secure_cookie("username")
        role  = int(self.get_secure_cookie("role"))
        '''
        e['dish_name']     = '凉拌三丝'
        e['average_score'] = 4.6
        e['material']      = '土豆、海带、细粉、蒜、葱、芥末'
        e['order']         = 1
        e['pic_land']      = ''
        e['pic_src']       = 'img/97.jpg'
        a.append(e)
        e = {}
        e['dish_name']     = '凉拌三丝111'
        e['average_score'] = 4.9
        e['material']      = '细粉、蒜、葱、芥末'
        e['order']         = 0
        e['pic_land']      = ''
        e['pic_src']       = 'img/97.jpg'
        a.append(e)
        '''
        self.render("canteen.html", username=uname, role=role, arr=a)

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("username");
        self.clear_cookie("role");
        self.redirect("/")
class DeleteHandler(tornado.web.RequestHandler):
    #@tornado.web.authenticated
    def get(self):
        imgid = self.get_argument("id")
        if not imgid:
            self.write("id is invalid")
        dish_delete(imgid)
        self.write("OK!!!")
if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True,
        "login_url": "/login",
        "debug":True}
    handler = [
               (r"/static/(.*)", StaticFileHandler, {"path": "static"}),  
               (r"/css/(.*)", StaticFileHandler, {"path": "static/css"}),  
               (r"/js/(.*)", StaticFileHandler, {"path": "static/js"}),  
               (r"/img/(.*)", StaticFileHandler, {"path": "static/img"}), 
               (r'/canteen', CanteenIndexHandler),
               (r'/', IndexHandler),
               (r'/welcome', WelcomeHandler),
               (r'/login', LoginHandler),
               (r'/up', UploadFileHandler),
               (r'/delete', DeleteHandler),
               (r'/menu', MenuHandler),
               (r'/logout', LogoutHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
