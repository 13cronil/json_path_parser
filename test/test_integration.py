import pytest
import json
from pathlib import Path
from lark import Lark

from json_path_parser.parser import create_parser


class TestJSONPathIntegration:
    """Integration tests using the complex test data."""

    @pytest.fixture
    def complex_data(self):
        """Load the complex test data."""
        test_data_path = Path(__file__).parent.parent / "test_data.json"
        with open(test_data_path) as f:
            return json.load(f)

    @pytest.mark.parametrize("json_path,description", [
        ("$", "Root selector"),
        ("$.store", "Store object"),
        ("$.store.book", "Book array"),
        ("$.store.book[0]", "First book"),
        ("$.store.book[0].title", "First book title"),
        ("$.store.book[0].metadata.publisher", "First book publisher"),
        ("$.store.book[*]", "All books (wildcard)"),
        ("$.store.book[*].author", "All book authors"),
        ("$.users[0].name", "First user name"),
        ("$.users[1].preferences.categories[0]", "Second user first category"),
        ('$.config["special-key"]', "Config key with special characters"),
        ("$.config.shipping.free_threshold", "Nested shipping config"),
        ("$.store.electronics[0].specs.cpu", "First electronic device CPU"),
    ])
    def test_valid_json_paths_parse_successfully(self, parser: Lark, json_path: str, description: str):
        """Test that various JSON paths parse without errors."""
        tree = parser.parse(json_path)
        assert tree is not None
        assert tree.data == "root"

    @pytest.mark.parametrize("json_path,expected_field", [
        ("$.store.book[0].title", "title"),
        ("$.users[0].name", "name"),
        ("$.config.store_name", "store_name"),
        ("$.store.bicycle.color", "color"),
    ])
    def test_field_access_extraction(self, parser: Lark, json_path: str, expected_field: str):
        """Test that field names are correctly extracted from paths."""
        tree = parser.parse(json_path)
        # Find the last field node in the tree
        field_nodes = [child for child in tree.children if hasattr(child, 'data') and child.data == "field"]
        assert len(field_nodes) > 0
        last_field = field_nodes[-1]
        assert last_field.children[0].value == expected_field

    @pytest.mark.parametrize("json_path,expected_index", [
        ("$.store.book[0]", "0"),
        ("$.store.book[1]", "1"),
        ("$.store.book[3]", "3"),
        ("$.users[0]", "0"),
        ("$.store.electronics[1]", "1"),
    ])
    def test_array_index_extraction(self, parser: Lark, json_path: str, expected_index: str):
        """Test that array indices are correctly extracted."""
        tree = parser.parse(json_path)
        # Find index nodes in the tree
        index_nodes = [child for child in tree.children if hasattr(child, 'data') and child.data == "index"]
        assert len(index_nodes) > 0
        # Check the last index node
        last_index = index_nodes[-1]
        assert last_index.children[0].value == expected_index

    @pytest.mark.parametrize("json_path", [
        "$.store.book[*].title",
        "$.users[*].email",
        "$.store.electronics[*].brand",
    ])
    def test_wildcard_paths_parse(self, parser: Lark, json_path: str):
        """Test that wildcard paths parse correctly."""
        tree = parser.parse(json_path)
        # Should contain a wildcard_index node
        wildcard_nodes = [child for child in tree.children if hasattr(child, 'data') and child.data == "wildcard_index"]
        assert len(wildcard_nodes) == 1

    @pytest.mark.parametrize("json_path,field_name,comparator,value_type", [
        ('$.store.book[?(price < 10)]', "price", "<", "number"),
        ('$.store.book[?(category == "fiction")]', "category", "==", "string"),
        ('$.store.book[?(available == true)]', "available", "==", "boolean"),
        ('$.users[?(age > 30)]', "age", ">", "number"),
        ('$.store.electronics[?(in_stock != false)]', "in_stock", "!=", "boolean"),
    ])
    def test_filter_expressions_parse(self, parser: Lark, json_path: str, field_name: str, comparator: str, value_type: str):
        """Test that filter expressions parse correctly with various data types."""
        tree = parser.parse(json_path)
        # Find the filter node
        filter_nodes = [child for child in tree.children if hasattr(child, 'data') and child.data == "filter"]
        assert len(filter_nodes) == 1

        filter_node = filter_nodes[0]
        condition = filter_node.children[0]
        assert condition.data == "condition"

        # Check field name
        assert condition.children[0].value == field_name

        # Check comparator
        assert condition.children[1].children[0] == comparator

        # Check value type
        value_node = condition.children[2]
        if value_type == "number":
            assert value_node.data == "value"
            assert value_node.children[0].data == "number"
        elif value_type == "string":
            assert value_node.data == "value"
            assert value_node.children[0].data == "string"
        elif value_type == "boolean":
            assert value_node.data == "value"
            # Should be either true or false node
            bool_node = value_node.children[0]
            assert bool_node.data in ["true", "false"]

    def test_complex_nested_paths_from_test_data(self, parser: Lark):
        """Test complex paths that would be useful with the test data."""
        complex_paths = [
            "$.store.book[0].metadata.publisher",
            "$.users[0].purchase_history[0].item",
            "$.config.api_endpoints.books",
            "$.store.electronics[1].specs.storage",
            "$.users[1].preferences.categories[0]",
        ]

        for path in complex_paths:
            tree = parser.parse(path)
            assert tree is not None
            assert tree.data == "root"

    def test_paths_with_special_characters_in_keys(self, parser: Lark):
        """Test paths that access keys with special characters."""
        special_paths = [
            '$.config["special-key"]',
            '$.config["store_name"]',  # underscore
        ]

        for path in special_paths:
            tree = parser.parse(path)
            assert tree is not None
            key_nodes = [child for child in tree.children if hasattr(child, 'data') and child.data == "key"]
            assert len(key_nodes) >= 1

    def test_realistic_query_scenarios(self, parser: Lark):
        """Test realistic query scenarios that might be used with the test data."""
        scenarios = [
            # Find all book titles
            "$.store.book[*].title",
            # Get user emails
            "$.users[*].email",
            # Access shipping configuration
            "$.config.shipping.free_threshold",
            # Get first user's purchase history
            "$.users[0].purchase_history[*].item",
            # Access electronics specifications
            "$.store.electronics[*].specs.cpu",
            # Filter books by price (syntax test only)
            '$.store.book[?(price < 15)]',
            # Filter users by age
            '$.users[?(age > 25)]',
        ]

        for scenario in scenarios:
            tree = parser.parse(scenario)
            assert tree is not None
            assert tree.data == "root"

    @pytest.mark.parametrize("invalid_path", [
        "store.book[0]",  # Missing $
        "$.",  # Empty field
        "$[]",  # Empty brackets
        "$[",  # Unclosed bracket
        "$[0",  # Unclosed bracket
        "$.store..book",  # Double dot
        "$[?(price)]",  # Incomplete filter
        "$[?(price === 10)]",  # Invalid operator
    ])
    def test_invalid_paths_raise_errors(self, parser: Lark, invalid_path: str):
        """Test that invalid paths raise parsing errors."""
        with pytest.raises(Exception):  # Could be LarkError or subclass
            parser.parse(invalid_path)

    def test_path_structure_validation(self, parser: Lark):
        """Test that parsed paths have the expected structure."""
        test_cases = [
            ("$.store", ["$", "field"]),
            ("$.store[0]", ["$", "field", "index"]),
            ("$.store[*]", ["$", "field", "wildcard_index"]),
            ('$.store["key"]', ["$", "field", "key"]),
            ('$.store[?(x == 1)]', ["$", "field", "filter"]),
        ]

        for path, expected_types in test_cases:
            tree = parser.parse(path)
            actual_types = []
            for child in tree.children:
                if isinstance(child, str):
                    actual_types.append(child)
                else:
                    actual_types.append(child.data)

            assert actual_types == expected_types, f"Path {path} has structure {actual_types}, expected {expected_types}"