#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import handlers
import os
from repo import Session

define("port", default=8000, type=int)

urls = [
tornado.web.url(r"/widget/\w*", handlers.WidgetHandler, dict(session=Session))
]

settings = dict({
    "cookie_secret": str(os.urandom(45)),
    "xsrf_cookies": True,
    "debug": False,
    "gzip": True,
})

application = tornado.web.Application(urls, **settings)


if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
