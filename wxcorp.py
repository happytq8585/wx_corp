import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import os.path
from tornado.options import define, options

from tables import query_user

define("port", default=8000, help="run on the given port", type=int)

class StaticHandler(tornado.web.RequestHandler):
    def get(self, htmlfile):
        self.render(htmlfile + ".html")

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
            self.render("success_log.html")

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
               (r'/login', LoginHandler),]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
