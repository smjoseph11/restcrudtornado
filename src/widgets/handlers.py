#coding: utf-8

from tornado.web import RequestHandler
import tornado.web
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from widgets.models import Base, Widget
from widgets.repo import Session

import json

class WidgetHandler(RequestHandler):

    def initialize(self, session:Session):
        self.session = session()

    def get(self):
        results = self.session.query(Widget).all()
        modded_results = []
        for res in results:
            breakpoint()
            res.__dict__.pop('_sa_instance_state')
            stringified_res = json.dumps(res.__dict__, default=str)
            modded_results.append(stringified_res)
        self.write({"results":modded_results})

    def post(self):
        acceptable_keys = ['name', 'number_of_parts']
        request_dict = json.loads(self.request.body)
        for k in request_dict:
            if k not in acceptable_keys:
                raise tornado.web.HTTPError(400, log_message="You have supplied a payload with unexpected fields")
            
        self.write({'message': json.loads(self.request.body)})
