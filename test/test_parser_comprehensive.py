import pytest
from lark import Lark
from lark.exceptions import LarkError


class TestJSONPathParser:
    """Comprehensive test suite for JSON Path parser."""

    def test_root_only(self, parser: Lark):
        """Test parsing just the root selector."""
        tree = parser.parse("$")
        assert tree.data == "root"
        assert len(tree.children) == 1
        assert tree.children[0] == "$"

    def test_simple_field_access(self, parser: Lark):
        """Test basic field access with dot notation."""
        tree = parser.parse("$.name")
        assert tree.data == "root"
        field_node = tree.children[1]
        assert field_node.data == "field"
        assert field_node.children[0].value == "name"

    def test_nested_field_access(self, parser: Lark):
        """Test accessing nested fields."""
        tree = parser.parse("$.user.profile.name")
        assert tree.data == "root"
        # Should have 4 children: $, field(user), field(profile), field(name)
        assert len(tree.children) == 4
        assert tree.children[1].data == "field"
        assert tree.children[1].children[0].value == "user"
        assert tree.children[2].data == "field"
        assert tree.children[2].children[0].value == "profile"
        assert tree.children[3].data == "field"
        assert tree.children[3].children[0].value == "name"

    def test_array_index_access(self, parser: Lark):
        """Test array index access."""
        tree = parser.parse("$[0]")
        assert tree.data == "root"
        index_node = tree.children[1]
        assert index_node.data == "index"
        assert index_node.children[0].value == "0"

    def test_negative_array_index(self, parser: Lark):
        """Test negative array index."""
        tree = parser.parse("$[-1]")
        assert tree.data == "root"
        index_node = tree.children[1]
        assert index_node.data == "index"
        assert index_node.children[0].value == "-1"

    def test_wildcard_access(self, parser: Lark):
        """Test wildcard selector."""
        tree = parser.parse("$[*]")
        assert tree.data == "root"
        wildcard_node = tree.children[1]
        assert wildcard_node.data == "wildcard_index"

    def test_string_key_access_double_quotes(self, parser: Lark):
        """Test key access with double quotes."""
        tree = parser.parse('$["key-with-hyphens"]')
        assert tree.data == "root"
        key_node = tree.children[1]
        assert key_node.data == "key"
        # The string should include the quotes
        assert '"key-with-hyphens"' in str(key_node.children[0])

    def test_string_key_access_single_quotes(self, parser: Lark):
        """Test key access with single quotes."""
        tree = parser.parse("$['special key']")
        assert tree.data == "root"
        key_node = tree.children[1]
        assert key_node.data == "key"
        assert "'special key'" in str(key_node.children[0])

    def test_mixed_access_patterns(self, parser: Lark):
        """Test combining different access patterns."""
        tree = parser.parse("$.store.book[0].title")
        assert tree.data == "root"
        assert (
            len(tree.children) == 5
        )  # $, field(store), field(book), index(0), field(title)

        # Verify each part
        assert tree.children[1].data == "field"
        assert tree.children[1].children[0].value == "store"
        assert tree.children[2].data == "field"
        assert tree.children[2].children[0].value == "book"
        assert tree.children[3].data == "index"
        assert tree.children[3].children[0].value == "0"
        assert tree.children[4].data == "field"
        assert tree.children[4].children[0].value == "title"

    def test_filter_expression_string_comparison(self, parser: Lark):
        """Test filter with string comparison."""
        tree = parser.parse('$[?(category == "fiction")]')
        assert tree.data == "root"
        filter_node = tree.children[1]
        assert filter_node.data == "filter"
        condition = filter_node.children[0]
        assert condition.data == "condition"
        assert condition.children[0].value == "category"  # field name
        assert condition.children[1].children[0] == "=="  # comparator
        # value should be a string

    def test_filter_expression_number_comparison(self, parser: Lark):
        """Test filter with number comparison."""
        tree = parser.parse("$[?(price < 10)]")
        assert tree.data == "root"
        filter_node = tree.children[1]
        assert filter_node.data == "filter"
        condition = filter_node.children[0]
        assert condition.children[0].value == "price"
        assert condition.children[1].children[0] == "<"

    def test_filter_expression_boolean_comparison(self, parser: Lark):
        """Test filter with boolean comparison."""
        tree = parser.parse("$[?(available == true)]")
        assert tree.data == "root"
        filter_node = tree.children[1]
        assert filter_node.data == "filter"
        condition = filter_node.children[0]
        assert condition.children[0].value == "available"
        assert condition.children[1].children[0] == "=="

    def test_filter_expression_null_comparison(self, parser: Lark):
        """Test filter with null comparison."""
        tree = parser.parse("$[?(deleted != null)]")
        assert tree.data == "root"
        filter_node = tree.children[1]
        assert filter_node.data == "filter"
        condition = filter_node.children[0]
        assert condition.children[0].value == "deleted"
        assert condition.children[1].children[0] == "!="

    @pytest.mark.parametrize("comparator", ["==", "!=", "<", "<=", ">", ">="])
    def test_all_comparators(self, parser: Lark, comparator: str):
        """Test all supported comparison operators."""
        tree = parser.parse(f"$[?(value {comparator} 5)]")
        assert tree.data == "root"
        filter_node = tree.children[1]
        condition = filter_node.children[0]
        assert condition.children[1].children[0] == comparator

    def test_complex_nested_path(self, parser: Lark):
        """Test a complex nested path with multiple types of access."""
        tree = parser.parse('$.users[0].preferences["max_price"]')
        assert tree.data == "root"
        assert len(tree.children) == 5
        assert tree.children[1].data == "field"  # users
        assert tree.children[2].data == "index"  # [0]
        assert tree.children[3].data == "field"  # preferences
        assert tree.children[4].data == "key"  # ["max_price"]

    def test_wildcard_with_field_access(self, parser: Lark):
        """Test wildcard followed by field access."""
        tree = parser.parse("$.store.book[*].title")
        assert tree.data == "root"
        assert len(tree.children) == 5
        assert tree.children[3].data == "wildcard_index"
        assert tree.children[4].data == "field"

    # Error cases
    def test_invalid_syntax_no_dollar(self, parser: Lark):
        """Test that paths must start with $."""
        with pytest.raises(LarkError):
            parser.parse("store.book")

    def test_invalid_syntax_empty_brackets(self, parser: Lark):
        """Test invalid empty brackets."""
        with pytest.raises(LarkError):
            parser.parse("$[]")

    def test_invalid_syntax_unclosed_brackets(self, parser: Lark):
        """Test unclosed brackets."""
        with pytest.raises(LarkError):
            parser.parse("$[0")

    def test_invalid_syntax_malformed_filter(self, parser: Lark):
        """Test malformed filter expression."""
        with pytest.raises(LarkError):
            parser.parse("$[?(price)]")  # Missing comparison

    def test_invalid_syntax_bad_comparator(self, parser: Lark):
        """Test invalid comparator in filter."""
        with pytest.raises(LarkError):
            parser.parse("$[?(price === 10)]")  # Invalid === operator

    def test_empty_field_name(self, parser: Lark):
        """Test that field names cannot be empty."""
        with pytest.raises(LarkError):
            parser.parse("$.")

    def test_whitespace_handling(self, parser: Lark):
        """Test that whitespace is properly ignored."""
        tree1 = parser.parse("$[ 0 ]")
        tree2 = parser.parse("$[0]")
        # Both should parse to equivalent structures
        assert tree1.data == tree2.data
        assert len(tree1.children) == len(tree2.children)

    def test_filter_with_whitespace(self, parser: Lark):
        """Test filter expressions with whitespace."""
        tree = parser.parse("$[ ?( price < 10 ) ]")
        assert tree.data == "root"
        filter_node = tree.children[1]
        assert filter_node.data == "filter"

    @pytest.mark.parametrize(
        "path,expected_elements",
        [
            ("$", 1),
            ("$.name", 2),
            ("$.user.name", 3),
            ("$[0]", 2),
            ("$.users[0].name", 4),
            ("$.store.book[*].title", 5),
            ('$["special-key"]', 2),
        ],
    )
    def test_path_element_counts(self, parser: Lark, path: str, expected_elements: int):
        """Test that paths have the expected number of elements."""
        tree = parser.parse(path)
        assert len(tree.children) == expected_elements
