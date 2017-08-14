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
from tables import query_comments_by_id, write_comment, write_order, update_user_password
from tables import query_order_list_by_uid, query_all_users, update_user
from tables import add_user, delete_user
from hostip import get_ip_address

define("port", default=8000, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")
    def get_role(self):
        return int(self.get_secure_cookie("role"))
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
        role = self.get_role()
        self.render("menu.html", today=today, data=data, host_ip=hostip, username=uname, role=role)

class UploadFileHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        if not os.path.exists("static/files"):
            os.makedirs("static/files");
        day = self.get_argument("day", None)
        if not day:
            timestamp = time.strftime("%Y%m%d", time.localtime())
        else:
            arr = [int(e) for e in day.split('-')]
            timestamp = "%4d%02d%02d"%(arr[0], arr[1], arr[2])
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
            self.write("用户名或密码错误")
        else:
            print(ret)
            self.set_secure_cookie("username", uname, expires_days=None)
            self.set_secure_cookie("role", "%d"%ret[0],  expires_days=None)
            self.set_secure_cookie("userid", "%d"%int(ret[1]), expires_days=None)
            self.redirect("/welcome")

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        uname = self.get_secure_cookie("username")
        role  = self.get_role()
        self.render("begin.html", username=uname, role=role)
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
        json = self.get_argument("json", None)
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
        role  = self.get_role()
        if json:
            ret = {}
            ret['data'] = a
            ret['username'] = uname
            ret['role'] = role
            self.write(ret)
        else:
            t = time.localtime();
            timestamp = time.strftime("%Y.%m.%d", t)
            self.render("canteen.html", username=uname, role=role, arr=a, today=timestamp)
'''
dish图片的landing page处理
'''
class CanteenItemHandler(BaseHandler):
    def get(self):
        r                 = {}
        r['dish_name']    = self.get_argument('dish_name', '')
        r['pic_src']      = self.get_argument('pic_src',   '')
        r['order']        = int(self.get_argument('order', 0))
        r['material']     = self.get_argument('material', '')
        r['average_score']= self.get_argument('average_score', 0)
        r['id']           = int(self.get_argument('id', 0))
        res               = query_comments_by_id(r['id'])#根据菜的id查询它的评论
        c                 = [{'id':e.id, 'user_id':e.user_id, 'stars':e.stars,
                              'time':e.time, 'content':e.content} for e in res] 
        s = 0
        for e in res:
            s = s + e.stars
        r['average_score'] = 1 if s == 0 else (int(s/len(res)))
        userid = int(self.get_secure_cookie("userid"))
        user_comment = None
        for e in res:
            if e.user_id == userid:
                user_comment = e
                break
        t = time.localtime();
        timestamp = time.strftime("%Y.%m.%d", t)
        role = self.get_role()
        self.render("canteenList.html", R=r, C=c, user_comment=user_comment, today=timestamp, role=role)
    def post(self):
        pass
class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("username");
        self.clear_cookie("role");
        self.redirect("/")
class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        imgid = self.get_argument("id")
        if not imgid:
            self.write("id is invalid")
        dish_delete(imgid)
        self.write("OK!!!")
'''
评论提交处理类
dish_id:  菜的id
star:     对该菜的星级评价
words:    对该菜的评论内容
'''
class CommentHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        dish_id        = self.get_argument("id", None)
        star           = self.get_argument("star", None)
        words          = self.get_argument("words", None)
        userid         = self.get_secure_cookie("userid")
        if not dish_id:
            self.write({"code":-1, "reason": "dish id is invalid"})
            return -1
        if not star:
            self.write({"code":-1, "reason": "star number is invalid"})
            return -1
        if not words:
            self.write({"code":-1, "reason": "comments is null"})
            return -1
        ret = write_comment(userid, dish_id, star, words)
        if not ret:
            self.write({"code":-1, "reason": "write failed!"})
            return -1
        self.write("success")
"""
订单信息提交
"""
class OrderHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        dish_id      = self.get_argument("dish_id", None)
        dish_name    = self.get_argument("dish_name", None)
        num          = self.get_argument("num", None)
        img_url      = self.get_argument("img_url", "")
        userid       = self.get_secure_cookie("userid")
        username     = self.get_secure_cookie("username")
        if not dish_id:
            self.write("dish_id is null!")
            return 1
        if not dish_name:
            self.write("dish_name is null!")
            return 1
        if not num:
            self.write("num is null")
            return 1
        ret = write_order(userid, username, dish_id, dish_name, img_url, num)
        if not ret:
            self.write("order to db error!")
            return 1
        self.write("order success!")

class PersonalCenterHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        role = self.get_role()
        self.render("PersonalCenter.html", role=role)
    def post(self):
        t     = self.get_argument("type", None)
        if not t:
            self.write("type is missing")
            return 1
        t = int(t)
        if t == 1:#rewrite password
            old       = self.get_argument("old", None)
            passwd    = self.get_argument("passwd", None)
            userid    = self.get_secure_cookie("userid")
            if not old:
                self.write("old password is null")
                return 1
            if not passwd:
                self.write("new passwd is null")
                return 1
            ret = update_user_password(userid, old, passwd)
            if not ret:
                self.write("update password failed")
                return 1
            self.write("update password success")

class OrderListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        uid         = self.get_secure_cookie("userid")
        olist       = query_order_list_by_uid(uid)
        print(olist)
        role        = self.get_role()
        self.render("OrderList.html", olist=olist, role=role)
class EmployeeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        users       = query_all_users()
        role        = self.get_role()
        self.render("Employeelists.html", userlists=users, role=role)
    @tornado.web.authenticated
    def post(self):
        action      = str(self.get_argument("action", ""))
        name        = str(self.get_argument("name", ""))
        passwd      = str(self.get_argument("passwd", ""))
        role        = int(self.get_argument("role", -1))
        uid         = int(self.get_argument("uid", -1))
            
        print(action, name, passwd, role, uid)
        if action == "update":
            update_user(name, passwd, role, uid)
        elif action == "delete":
            delete_user(uid)
        elif action == "add":
            add_user(name, passwd, role)

class ConstructHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write("Constructing!")
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
               (r'/canteenItem', CanteenItemHandler),
               (r'/comment', CommentHandler),
               (r'/order',   OrderHandler),
               (r'/personalcenter', PersonalCenterHandler),
               (r'/orderlist', OrderListHandler),
               (r'/employee', EmployeeHandler),
               (r'/', IndexHandler),
               (r'/welcome', WelcomeHandler),
               (r'/login', LoginHandler),
               (r'/up', UploadFileHandler),
               (r'/delete', DeleteHandler),
               (r'/logout', LogoutHandler),
               (r'/meeting', ConstructHandler),
               (r'/property',ConstructHandler),
               (r'/notice',  ConstructHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
