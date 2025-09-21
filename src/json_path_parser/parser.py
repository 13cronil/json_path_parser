from lark import Lark


def create_parser() -> Lark:
    """Create and return a JSON parser using Lark.

    This parser is designed to parse JSONPath expressions.

    Returns:
        Lark: A Lark parser instance configured for JSONPath.

    """
    grammar = r"""
        ?start: root

        root : "$" segment*

        ?segment: dot_selector
                | bracket_selector
                | recursive_selector

        dot_selector: "." (CNAME | "*")          -> field

        bracket_selector: "[" bracketed_content "]"

        ?bracketed_content: integer                   -> index
                        | slice
                        | "*"                         -> wildcard_index
                        | int_index_list              -> index_list
                        | string                      -> name

        recursive_selector: ".." (CNAME | "*" | bracket_selector)?

        ?slice: integer? ":" integer? (":" integer?)?
        int_index_list: integer ("," integer)*

        string : ESCAPED_STRING | SINGLE_QUOTED_STRING
        ?integer : SIGNED_INT


        SINGLE_QUOTED_STRING : /'([^'\\]*(\\.[^'\\]*)*)'/

        %import common.SIGNED_INT
        %import common.ESCAPED_STRING
        %import common.CNAME
        %import common.SIGNED_NUMBER
        %import common.WS
        %ignore WS
    """

    return Lark(grammar, start="root", parser="earley")
