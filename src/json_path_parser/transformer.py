from __future__ import annotations

from typing import Any

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
    """Transformer for converting parsed JSONPath tokens into structured objects."""

    def root(self, items: list[Token]) -> JSONPath:
        """Transform root JSONPath expression.

        Args:
            items: List of parsed tokens representing JSONPath segments.

        Returns:
            JSONPath object containing all segments.

        """
        return JSONPath(segments=items)

    def field(self, items: list[Token]) -> Field:
        """Transform field selector.

        Args:
            items: List containing a single field name token.

        Returns:
            Field object with name and wildcard flag.
        """
        (name_token,) = items
        return Field(name=str(name_token), wildcard=(name_token == "*"))  # noqa: S105

    def index(self, items: list[Token]) -> Index:
        """Transform array index selector.

        Args:
            items: List containing a single index token.

        Returns:
            Index object with parsed integer index.
        """
        (idx_token,) = items
        return Index(idx=int(idx_token))

    def slice(self, items: list[Token]) -> Slice:
        """Transform slice selector.

        Args:
            items: List of tokens representing slice parameters (start, end, step).

        Returns:
            Slice object with start, end, and step values.
        """
        padded = list(items) + [None] * (3 - len(items))
        start, end, step = (int(i) if i is not None else None for i in padded[:3])
        return Slice(start=start, end=end, step=step)

    def wildcard_index(self, _: Any) -> WildcardIndex:
        """Transform wildcard index selector.

        Args:
            _: Unused parameter (wildcard tokens).

        Returns:
            WildcardIndex object.
        """
        return WildcardIndex()

    def index_list(self, items: list[Token]) -> IndexList:
        """Transform list of indices.

        Args:
            items: List of index tokens.

        Returns:
            IndexList object containing parsed integer indices.
        """
        indices = [int(i) for i in items]
        return IndexList(indices=indices)

    def name(self, items: list[Token]) -> Name:
        """Transform name token.

        Args:
            items: List containing a single name token.

        Returns:
            Name object with the token value.
        """
        (name_token,) = items
        return Name(name=name_token)

    def bracket_selector(self, items: list[Token]) -> BracketSelector:
        """Transform bracket selector.

        Args:
            items: List containing a single content token.

        Returns:
            BracketSelector object with the content.
        """
        (content,) = items
        return BracketSelector(content=content)
