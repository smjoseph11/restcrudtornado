# coding: utf-8

import json

import tornado.web
from tornado.web import RequestHandler

from widgets.models import Widget
from widgets.repo import Session


class WidgetGetPostHandler(RequestHandler):
    def initialize(self, session: Session):
        self.session = session()

    # LIST
    def get(self):
        results = self.session.query(Widget).all()
        modded_results = []
        for res in results:
            res.__dict__.pop("_sa_instance_state")
            stringified_res = json.dumps(res.__dict__, default=str)
            modded_results.append(stringified_res)
        self.write({"results": modded_results})

    # CREATE
    def post(self):
        acceptable_keys = ["name", "number_of_parts"]
        request_dict = json.loads(self.request.body)
        for k in request_dict:
            if k not in acceptable_keys:
                raise tornado.web.HTTPError(
                    400,
                    log_message="You have supplied a payload with unexpected fields",
                )
        if "name" and "number_of_parts" in request_dict.keys():
            widget = Widget(
                name=request_dict["name"],
                number_of_parts=request_dict["number_of_parts"],
            )
            self.session.add(widget)
            self.session.commit()
        else:
            raise tornado.web.HTTPError(
                400, log_message="You have supplied a payload without a required field"
            )
        self.write({"message": f"added {request_dict} to repo"})


class WidgetDeleteHandler(RequestHandler):
    def initialize(self, session: Session):
        self.session = session()

    # DELETE
    def delete(self, name):
        query = self.session.query(Widget).filter_by(name=name)
        if query.all() == []:
            raise tornado.web.HTTPError(
                400,
                log_message="this name does not exist in the database of widgets and"
                "therefore cannot be deleted",
            )
        else:
            query.delete()
            self.write({"message": f"Widget {name} deleted from the database"})
        self.session.commit()

    # READ
    def get(self, name):
        result = self.session.query(Widget).filter_by(name=name).all()
        if result == []:
            raise tornado.web.HTTPError(
                400,
                log_message="this name does not exist in the database of widgets and"
                "therefore cannot be retrieved",
            )
        else:
            widget = result[0]
        widget.__dict__.pop("_sa_instance_state")
        stringified_res = json.dumps(widget.__dict__, default=str)
        self.write({"result": stringified_res})

    # UPDATE
    def put(self, name):
        query = self.session.query(Widget).filter_by(name=name).all()
        if query == []:
            raise tornado.web.HTTPError(
                400,
                log_message="this name does not exist in the database of widgets and"
                "therefore cannot be retrieved",
            )
        else:
            widget = query[0]
        acceptable_keys = ["number_of_parts"]
        request_dict = json.loads(self.request.body)
        for k in request_dict:
            if k not in acceptable_keys:
                raise tornado.web.HTTPError(
                    400,
                    log_message="You have supplied a payload with unexpected fields",
                )
        if "number_of_parts" in request_dict.keys():
            widget.number_of_parts = request_dict["number_of_parts"]
            self.session.commit()
        else:
            raise tornado.web.HTTPError(
                400, log_message="You have supplied a payload without a required field"
            )
        self.write({"message": f"updated {name} with {request_dict}"})
