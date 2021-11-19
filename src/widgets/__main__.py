#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from widgets import handlers
from widgets.repo import Session

define("port", default=8000, type=int)

urls = [
    tornado.web.url(r"/widget", handlers.WidgetGetPostHandler, dict(session=Session)),
    tornado.web.url(
        r"/widget/(\w+)", handlers.WidgetDeleteHandler, dict(session=Session)
    ),
]

settings = dict(
    {
        "debug": True,
    }
)

application = tornado.web.Application(urls, **settings)


if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
