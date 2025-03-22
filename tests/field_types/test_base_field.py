import pytest
from pydantic import ValidationError
from typing import Optional, Annotated, get_origin, get_args

from data_sitter.field_types.BaseField import (
    BaseField, NotInitialisedError, aggregated_validator
)


class TestBaseField:
    def test_init(self):
        """Test BaseField initialization"""
        field = BaseField("test_field")
        assert field.name == "test_field"
        assert field.is_optional is True
        assert field.validators is None

    def test_validator_not_null(self):
        """Test the not null validator"""
        field = BaseField("test_field")
        validator = field.validator_not_null()

        # Should not raise for non-None value
        validator("test")

        # Check that field is now non-optional
        assert field.is_optional is False

        # Should raise for None when not optional
        with pytest.raises(ValueError, match="Value cannot be null."):
            validator(None)

    def test_validate_without_initialisation(self):
        """Test validate method raises NotInitialisedError when validators not set"""
        field = BaseField("test_field")
        with pytest.raises(NotInitialisedError):
            field.validate("value")

    def test_validate_with_validators(self):
        """Test validate method with validators"""
        field = BaseField("test_field")

        # Mock validators
        validation_called = False
        def mock_validator(value):
            nonlocal validation_called
            validation_called = True
            return value

        field.validators = [mock_validator]
        field.validate("test")
        assert validation_called is True

    def test_get_annotation_without_initialisation(self):
        """Test get_annotation raises NotInitialisedError when validators not set"""
        field = BaseField("test_field")
        with pytest.raises(NotInitialisedError):
            field.get_annotation()

    def test_get_annotation(self):
        """Test get_annotation returns the correct annotation"""
        field = BaseField("test_field")
        field.field_type = str  # Set field type for testing

        # Mock validators
        def mock_validator(value):
            return value

        field.validators = [mock_validator]

        # Test with optional=True (default)
        annotation = field.get_annotation()
        assert get_origin(annotation) is Annotated
        assert get_args(annotation)[0] == Optional[str]

        # Test with optional=False
        field.is_optional = False
        annotation = field.get_annotation()
        assert get_origin(annotation) is Annotated
        assert get_args(annotation)[0] == str

    def test_get_parents(self):
        """Test the get_parents class method"""
        # BaseField should have no parents
        assert BaseField.get_parents() == []

        # Create a simple subclass for testing
        class TestField(BaseField):
            pass

        # TestField should have BaseField as parent
        parents = TestField.get_parents()
        assert len(parents) == 1
        assert parents[0] == BaseField


class TestAggregatedValidator:
    def test_aggregated_validator_optional(self):
        """Test aggregated_validator with optional values"""
        validation_called = False

        def mock_validator(value):
            nonlocal validation_called
            validation_called = True
            return value

        validator = aggregated_validator([mock_validator], is_optional=True)

        # None value should be returned without validation when optional
        result = validator(None)
        assert result is None
        assert validation_called is False

        # Non-None value should be validated
        result = validator("test")
        assert result == "test"
        assert validation_called is True

    def test_aggregated_validator_required(self):
        """Test aggregated_validator with required values"""
        called_validators = []

        def validator1(value):
            called_validators.append(1)
            return value

        def validator2(value):
            called_validators.append(2)
            return value

        validator = aggregated_validator([validator1, validator2], is_optional=False)

        # All validators should be called in order
        result = validator("test")
        assert result == "test"
        assert called_validators == [1, 2]

    def test_aggregated_validator_with_error(self):
        """Test aggregated_validator when a validator raises an error"""
        def validator1(value):
            return value

        def validator2(value):
            raise ValueError("Validation error")

        validator = aggregated_validator([validator1, validator2], is_optional=False)

        # Should raise the error from validator2
        with pytest.raises(ValueError, match="Validation error"):
            validator("test")
