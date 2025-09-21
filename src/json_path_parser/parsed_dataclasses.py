from dataclasses import dataclass


@dataclass
class JSONPath:
    segments: list


@dataclass
class Index:
    idx: int


@dataclass
class Slice:
    start: int | None
    end: int | None
    step: int | None


@dataclass
class Field:
    name: str
    wildcard: bool = False


@dataclass
class Name:
    name: str


@dataclass
class WildcardIndex:
    pass


@dataclass
class IndexList:
    indices: list[int]


@dataclass
class BracketSelector:
    content: Index | Slice | WildcardIndex | IndexList | Name


@dataclass
class RecursiveSelector:
    name: Field | BracketSelector | None  # Can be None for cases like '..'


# @dataclass
# class FilterSelector:
#     expression: str  # Placeholder for filter expression representation
