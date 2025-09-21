import pytest


class TestTransformer:
    def test_transform_simple(self, transformer, sample_json_path_complex):
        tree = transformer.parse(sample_json_path_complex)
        result = transformer.transform(tree)
        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0

    def test_transform_invalid(self, transformer):
        invalid_json_path = "^"
        with pytest.raises(Exception):
            tree = transformer.parse(invalid_json_path)
            transformer.transform(tree)
