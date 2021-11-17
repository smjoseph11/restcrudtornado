import pytest
from widgets.models import Widget

def test_widget():
    widget = Widget(name="test_name", number_of_parts=0)
    assert widget.name == "test_name"
