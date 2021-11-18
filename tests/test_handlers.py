from widgets import handlers
from widgets.models import Widget
from widgets.models import Base
from tornado.web import Application
from tornado.httputil import HTTPServerRequest
from tornado.testing import AsyncHTTPTestCase
from unittest.mock import Mock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
import datetime

class TestWidget():

    eng = create_engine('sqlite://')

    Base.metadata.bind = eng
    Base.metadata.create_all()

    Session = sessionmaker(bind=eng)
    session = Session()
    def test_list_all_widgets(self, monkeypatch):
        """
        This tests if all widgets are retrieved from the db when the get method is called
        """
        widget1 = Widget("test_widget_1", 1)
        widget2 = Widget("test_widget_2", 2)
        self.session.add(widget1)
        self.session.add(widget2)
        self.session.commit()
        expected_list_of_widgets = [widget1, widget2]
        monkeypatch.setattr(handlers.WidgetHandler, 'initialize', self.Session)
        setattr(handlers.WidgetHandler, "session", self.session)
        handler = handlers.WidgetHandler(Mock(ui_methods={}), Mock())
        handler.get()
        results_dict = json.loads(handler._write_buffer[0])
        assert json.loads(results_dict['results'][0])['name'] == 'test_widget_1'
        assert json.loads(results_dict['results'][1])['name'] == 'test_widget_2'
    def test_create_widget(self, monkeypatch):
        """
        This tests if a widget can be created and is added to the database
        """
        payload = {'name': 'test_create_name', 'number_of_parts': '1'}
        monkeypatch.setattr(handlers.WidgetHandler, 'initialize', self.Session)
        setattr(handlers.WidgetHandler, "session", self.session)
        class FakeRequest:
            body = None
        handler = handlers.WidgetHandler(Mock(ui_methods={}), Mock(body=json.dumps(payload, default=str)))
        handler.post()
        expected_widget = self.session.query(Widget).filter_by(name = "test_create_name")
