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
        if 'name' and 'number_of_parts' in request_dict.keys():
            widget = Widget(name=request_dict['name'],
            number_of_parts=request_dict['number_of_parts'])
            self.session.add(widget)
        else:
            raise tornado.web.HTTPError(400, log_message="You have supplied a payload without a required field")
        self.write({'message': f"added {request_dict} to repo"})
