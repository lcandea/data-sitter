import pytest
from data_sitter.rules.Parser.parser_utils import (
    get_key_from_reference,
    get_value_from_reference,
    MalformedReference,
    ReferenceNotFound
)


class TestParserUtils:
    def test_get_key_from_reference_valid(self):
        """Test get_key_from_reference with valid reference"""
        reference = "$values.test_key"
        key = get_key_from_reference(reference)
        assert key == "test_key"

        # Test with more complex key name
        reference = "$values.complex_key_123"
        key = get_key_from_reference(reference)
        assert key == "complex_key_123"

    def test_get_key_from_reference_invalid(self):
        """Test get_key_from_reference with invalid reference format"""
        # Missing $values. prefix
        with pytest.raises(MalformedReference, match="Unrecognised Reference"):
            get_key_from_reference("test_key")

        # Wrong prefix
        with pytest.raises(MalformedReference, match="Unrecognised Reference"):
            get_key_from_reference("$wrong.test_key")

        # Invalid characters in key
        with pytest.raises(MalformedReference, match="Unrecognised Reference"):
            get_key_from_reference("$values.test-key")  # hyphen not allowed

        # Extra content after key
        with pytest.raises(MalformedReference, match="Unrecognised Reference"):
            get_key_from_reference("$values.test_key.extra")

    def test_get_value_from_reference_existing(self):
        """Test get_value_from_reference with existing key"""
        values = {"test_key": "test_value", "number_key": 123}

        # String value
        value = get_value_from_reference("$values.test_key", values)
        assert value == "test_value"

        # Numeric value
        value = get_value_from_reference("$values.number_key", values)
        assert value == 123

    def test_get_value_from_reference_not_found(self):
        """Test get_value_from_reference with non-existent key"""
        values = {"test_key": "test_value"}

        with pytest.raises(ReferenceNotFound, match="Reference 'missing_key' not found in values"):
            get_value_from_reference("$values.missing_key", values)

    def test_get_value_from_reference_invalid_reference(self):
        """Test get_value_from_reference with invalid reference format"""
        values = {"test_key": "test_value"}

        with pytest.raises(MalformedReference, match="Unrecognised Reference"):
            get_value_from_reference("invalid_reference", values)
