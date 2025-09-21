import pytest
from pathlib import Path

from json_path_parser.parser import create_parser


@pytest.fixture
def parser():
    return create_parser()


@pytest.fixture
def sample_json():
    return r"""
    {
        "name": "John",
        "age": 30,
        "is_student": false,
        "courses": ["Math", "Science"],
        "address": {
            "city": "New York",
            "zip": "10001"
        },
        "scores": [95, 88, 76]
    }
    """


@pytest.fixture
def sample_nested_json():
    return Path(__file__).parent / "data" / "nested.json"


@pytest.fixture
def sample_json_path_complex():
    return "$.store.book[?(@.price < 10)].title"
