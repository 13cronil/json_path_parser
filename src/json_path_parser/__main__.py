from lark import Lark

grammar = r"""
    value: dict
         | list
         | STRING
         | NUMBER
         | "true" | "false" | "null"

    dict : "{" [pair ("," pair)*] "}"
    pair : STRING ":" value
    list : "[" [value ("," value)*] "]"

    %import common.ESCAPED_STRING -> STRING
    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS
    %ignore WS
"""

json_path_parser = Lark(grammar, start="value", parser="lalr")

print("test")
