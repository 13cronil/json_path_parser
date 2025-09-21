import pytest
from lark import Lark, Tree


class TestParser:
    def test_parse_simple(self, parser: Lark, sample_json_path: str):
        sample_json_path = "$.store.book[1].title"
        tree = parser.parse(sample_json_path)
        assert tree is not None

    def test_parse_invalid_json_path(self, parser: Lark):
        invalid_json_path = "^"
        with pytest.raises(Exception):
            parser.parse(invalid_json_path)

    def test_root_only(self, parser: Lark) -> None:
        """Test parsing just the root selector."""
        tree = parser.parse("$")
        assert tree.data == "root"
        assert len(tree.children) == 0
        assert isinstance(tree, Tree)
