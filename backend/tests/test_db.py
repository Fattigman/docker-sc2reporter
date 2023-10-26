from unittest.mock import patch, Mock
from db import parse_json, db  # replace `your_module_name` with the module's name
import importlib


def test_parse_json():
    data = {"key": "value"}
    parsed = parse_json(data)
    assert isinstance(parsed, dict)
