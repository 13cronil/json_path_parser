import json

from json_path_parser.parsed_dataclasses import (
    JSONPath,
    Slice,
    WildcardIndex,
    IndexList,
    Index,
    Field,
    Name,
    BracketSelector,
    FilterSelector,
    RecursiveSelector,
)


class JSONPathEvaluator:
    def __init__(self, json_data: dict[str, any]):
        self.json_data = json_data

    def select(self, path: JSONPath) -> list[any]:
        """Evaluate the JSONPath against the JSON data."""
        current_selection = [self.json_data]

        while path.segments:
            segment = path.segments.pop(0)
            next_selection = []

            # Apply segments in sequence, passing results to the next segment
            for item in current_selection:
                results = self._apply_segment_to_value(item, segment)
                next_selection.extend(results)

            current_selection = next_selection
        return current_selection

    def _apply_segment_to_value(self, value: any, segment: any) -> list[any]:
        """Apply a segment to a value (object, array, or primitive)."""
        if isinstance(segment, Field):
            return self._apply_field(value, segment.name)
        if isinstance(segment, BracketSelector):
            return self._apply_bracket_selector(value, segment.content)
        if isinstance(segment, RecursiveSelector):
            return self._apply_recursive(value, segment)
        if isinstance(segment, FilterSelector):
            return self._apply_filter(value, segment)
        return []

    def _apply_field(self, item: any, field_name: str) -> list[any]:
        """Apply a field selector to an item.

        Args:
            item: The JSON item (object or array) to apply the field selector to.
            field_name: The name of the field to select, or '*' for wildcard selection.

        Returns:
            A list of selected values. If the field does not exist, returns empty list.

        Example:
        item = {"name": "Alice", "age": 30}
        field_name = "name"
        Returns: ["Alice"]

        """
        if not isinstance(item, dict):
            return []

        if field_name == "*":
            return list(item.values())
        if field_name in item:
            return [item[field_name]]
        return []

    def _apply_filter(self, items: list[any], filter: FilterSelector) -> list[any]:
        """Apply a filter to a list of items."""
        # Placeholder implementation; actual filter logic would depend on filter structure
        msg = "Filter application not implemented yet."
        raise NotImplementedError(msg)

    def _apply_wildcard(self, item: any) -> list[any]:
        """Apply a wildcard segment to an item."""
        if isinstance(item, list):
            return item  # All elements in the array
        if isinstance(item, dict):
            return list(item.values())  # All values in the object
        return []

    def _apply_index_list(self, item: any, indices: list[int]) -> list[any]:
        """Apply a list of indices to an item."""
        if not isinstance(item, list):
            return []
        return [item[idx] for idx in indices if -len(item) <= idx < len(item)]

    def _apply_slice(self, item: any, slice_obj: Slice) -> list[any]:
        """Apply a slice to an item."""
        if not isinstance(item, list):
            return []
        start = slice_obj.start
        end = slice_obj.end
        step = slice_obj.step
        return item[start:end:step]

    def _apply_bracket_selector(
        self,
        item: any,
        segment: any,
    ) -> list[any]:
        """Apply a bracket selector to an item."""
        if isinstance(segment, Index):
            return self._apply_index_list(item, [segment.idx])
        if isinstance(segment, Slice):
            return self._apply_slice(item, segment)
        if isinstance(segment, WildcardIndex):
            return self._apply_wildcard(item)
        if isinstance(segment, IndexList):
            return self._apply_index_list(item, segment.indices)
        if isinstance(segment, Name):
            return self._apply_field(item, segment.name)
        return []

    def _apply_recursive(self, item: any, segment: any) -> list[any]:
        """Recursively apply a segment to an item and its children."""
        return []  # Placeholder for recursive logic
