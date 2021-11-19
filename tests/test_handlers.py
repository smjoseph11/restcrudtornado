import json
from unittest.mock import Mock

from widgets import handlers
from widgets.models import Widget


class TestWidget:
    def test_list_all_widgets(self, monkeypatch, session):
        """
        This tests if all widgets are retrieved from the db
        when the get method is called
        """
        session_inst = session()
        widget1 = Widget("test_widget_1", 1)
        widget2 = Widget("test_widget_2", 2)
        session_inst.add(widget1)
        session_inst.add(widget2)
        session_inst.commit()
        monkeypatch.setattr(handlers.WidgetGetPostHandler, "initialize", session)
        setattr(handlers.WidgetGetPostHandler, "session", session_inst)
        handler = handlers.WidgetGetPostHandler(Mock(ui_methods={}), Mock())
        handler.get()
        results_dict = json.loads(handler._write_buffer[0])
        assert json.loads(results_dict["results"][0])["name"] == "test_widget_1"
        assert json.loads(results_dict["results"][1])["name"] == "test_widget_2"

    def test_create_widget(self, monkeypatch, session):
        """
        This tests if a widget can be created and is added to the database
        """
        session_inst = session()
        payload = {"name": "test_create_name", "number_of_parts": "1"}
        monkeypatch.setattr(handlers.WidgetGetPostHandler, "initialize", session)
        setattr(handlers.WidgetGetPostHandler, "session", session())

        class FakeRequest:
            body = None

        handler = handlers.WidgetGetPostHandler(
            Mock(ui_methods={}), Mock(body=json.dumps(payload, default=str))
        )
        handler.post()
        query = session_inst.query(Widget).filter_by(name="test_create_name")
        assert query.all()[0].name == "test_create_name"

    def test_delete_widget(self, monkeypatch, session):
        """
        This tests if a widget can be deleted from the database
        """
        session_inst = session()
        widget1 = Widget("test_widget_1", 1)
        widget2 = Widget("test_widget_2", 2)
        session_inst.add(widget1)
        session_inst.add(widget2)
        session_inst.commit()
        monkeypatch.setattr(handlers.WidgetDeleteHandler, "initialize", session)
        setattr(handlers.WidgetDeleteHandler, "session", session_inst)
        handler = handlers.WidgetDeleteHandler(Mock(ui_methods={}), Mock())
        handler.delete("test_widget_1")
        query_1 = session_inst.query(Widget).filter_by(name="test_widget_1")
        assert query_1.all() == []
        query_2 = session_inst.query(Widget).filter_by(name="test_widget_2")
        assert query_2.all()[0].name == "test_widget_2"

    def test_update_widget(self, monkeypatch, session):
        """
        This tests if a widget can be updated from the database
        """
        payload = {"number_of_parts": "2"}
        session_inst = session()
        widget1 = Widget("test_widget_1", 1)
        widget2 = Widget("test_widget_2", 2)
        session_inst.add(widget1)
        session_inst.add(widget2)
        session_inst.commit()
        monkeypatch.setattr(handlers.WidgetDeleteHandler, "initialize", session)
        setattr(handlers.WidgetDeleteHandler, "session", session_inst)
        handler = handlers.WidgetDeleteHandler(
            Mock(ui_methods={}), Mock(body=json.dumps(payload, default=str))
        )
        handler.put(name="test_widget_1")
        query = session_inst.query(Widget).filter_by(name="test_widget_1")
        assert query.all()[0].number_of_parts == 2
