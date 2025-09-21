from dataclasses import dataclass


@dataclass
class JSONPath:
    """Represents a complete JSONPath expression.

    A JSONPath is composed of multiple segments that define a path
    through a JSON structure.
    """

    segments: list[any]


@dataclass
class Index:
    """Represents an array index selector.

    Used to access specific elements in arrays by their numeric index.
    """

    idx: int


@dataclass
class Slice:
    """Represents a slice selector for arrays.

    Allows selecting ranges of elements from arrays using Python-style
    slice notation with start, end, and step parameters.
    """

    start: int | None
    end: int | None
    step: int | None


@dataclass
class Field:
    """Represents a field selector for objects.

    Used to access properties of JSON objects by name, with support
    for wildcard matching.
    """

    name: str
    wildcard: bool = False


@dataclass
class Name:
    """Represents a name token.

    Basic container for string names used in various JSONPath contexts.
    """

    name: str


@dataclass
class WildcardIndex:
    """Represents a wildcard index selector.

    Matches all elements in an array, equivalent to using '*' as an index.
    """


@dataclass
class IndexList:
    """Represents a list of specific indices.

    Allows selecting multiple specific elements from an array by their
    numeric indices.
    """

    indices: list[int]


@dataclass
class BracketSelector:
    """Represents a bracket notation selector.

    Container for various types of selectors that can appear within
    square brackets in JSONPath expressions.
    """

    content: Index | Slice | WildcardIndex | IndexList | Name


@dataclass
class RecursiveSelector:
    """Represents a recursive descent selector.

    Used for deep searching through nested structures, typically
    represented by '..' in JSONPath syntax.
    """

    name: Field | BracketSelector | None  # Can be None for cases like '..'


@dataclass
class FilterSelector:
    expression: str  # Placeholder for filter expression representation
