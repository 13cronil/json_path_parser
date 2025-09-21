from lark import Token, Transformer

from .parsed_dataclasses import (
    BracketSelector,
    Field,
    Index,
    IndexList,
    JSONPath,
    Name,
    Slice,
    WildcardIndex,
)


class JSONPathTransformer(Transformer):
    def root(self, items: list[Token]):
        return JSONPath(segments=items)

    def field(self, items: list[Token]):
        (name_token,) = items
        return Field(name=name_token, wildcard=(name_token == "*"))  # noqa: S105

    def index(self, items: list[Token]):
        (idx_token,) = items
        return Index(idx=int(idx_token))

    def slice(self, items: list[Token]):
        start, end, step = (int(i) if i is not None else None for i in items)
        return Slice(start=start, end=end, step=step)

    def wildcard_index(self, _):
        return WildcardIndex()

    def index_list(self, items: list[Token]):
        indices = [int(i) for i in items]
        return IndexList(indices=indices)

    def name(self, items: list[Token]):
        (name_token,) = items
        return Name(name=name_token)

    def bracket_selector(self, items: list[Token]):
        (content,) = items
        return BracketSelector(content=content)
