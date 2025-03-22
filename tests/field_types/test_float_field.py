import pytest
from data_sitter.field_types.FloatField import FloatField
from data_sitter.field_types.NumericField import NumericField


class TestFloatField:
    def test_inheritance(self):
        """Test that FloatField inherits from NumericField"""
        field = FloatField("test_field")
        assert isinstance(field, NumericField)
        assert field.field_type == float

    def test_non_zero_validator(self):
        """Test that validate_non_zero works with float values"""
        field = FloatField("test_field")
        validator = field.validate_non_zero()

        # Valid cases
        validator(1.5)
        validator(-1.5)

        # Invalid case
        with pytest.raises(ValueError, match="Value cannot be zero."):
            validator(0.0)

    def test_positive_validator(self):
        """Test that validate_positive works with float values"""
        field = FloatField("test_field")
        validator = field.validate_positive()

        # Valid cases
        validator(1.5)
        validator(0.1)

        # Invalid cases
        with pytest.raises(ValueError, match="Value must be positive."):
            validator(0.0)

        with pytest.raises(ValueError, match="Value must be positive."):
            validator(-1.5)

    def test_negative_validator(self):
        """Test that validate_negative works with float values"""
        field = FloatField("test_field")
        validator = field.validate_negative()

        # Valid cases
        validator(-1.5)
        validator(-0.1)

        # Invalid cases
        with pytest.raises(ValueError, match="Value must be less than zero."):
            validator(0.0)

        with pytest.raises(ValueError, match="Value must be less than zero."):
            validator(1.5)

    def test_min_validator(self):
        """Test that validate_min works with float values"""
        field = FloatField("test_field")
        min_val = 5.5
        validator = field.validate_min(min_val)

        # Valid cases
        validator(5.5)
        validator(6.7)

        # Invalid case
        with pytest.raises(ValueError, match=f"Value must be at least {min_val}."):
            validator(5.4)

    def test_max_validator(self):
        """Test that validate_max works with float values"""
        field = FloatField("test_field")
        max_val = 10.5
        validator = field.validate_max(max_val)

        # Valid cases
        validator(10.5)
        validator(9.9)

        # Invalid case
        with pytest.raises(ValueError, match=f"Value must not exceed {max_val}."):
            validator(10.6)

    def test_greater_than_validator(self):
        """Test that validate_greater_than works with float values"""
        field = FloatField("test_field")
        threshold = 7.5
        validator = field.validate_greater_than(threshold)

        # Valid case
        validator(7.6)

        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be greater than {threshold}."):
            validator(7.5)

        with pytest.raises(ValueError, match=f"Value must be greater than {threshold}."):
            validator(7.4)

    def test_less_than_validator(self):
        """Test that validate_less_than works with float values"""
        field = FloatField("test_field")
        threshold = 7.5
        validator = field.validate_less_than(threshold)

        # Valid case
        validator(7.4)

        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be less than {threshold}."):
            validator(7.5)

        with pytest.raises(ValueError, match=f"Value must be less than {threshold}."):
            validator(7.6)

    def test_between_validator(self):
        """Test that validate_between works with float values"""
        field = FloatField("test_field")
        min_val, max_val = 5.5, 10.5
        validator = field.validate_between(min_val, max_val, negative=False)

        # Valid case
        validator(7.5)

        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(5.5)  # Equal to min (exclusive)

        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(10.5)  # Equal to max (exclusive)

        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(5.4)  # Less than min

        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(10.6)  # Greater than max

    def test_validate_max_decimal_places(self):
        """Test validate_max_decimal_places validator"""
        field = FloatField("test_field")

        # Test with 2 decimal places
        decimal_places = 2
        validator = field.validate_max_decimal_places(decimal_places)

        # Valid cases
        validator(123.45)  # Exactly 2 decimal places
        validator(123.4)   # 1 decimal place
        validator(123.0)   # 0 decimal places
        validator(123.)    # Alternate syntax for 0 decimal places
        validator(123)     # Integer should be converted to float

        # Edge cases
        validator(0.01)    # Small number with 2 places
        validator(1e2)     # Scientific notation, no decimal places
        validator(1.2e1)   # Scientific notation, 1 decimal place (12.0)

        # Invalid case
        with pytest.raises(ValueError, match=f"Value must have at most {decimal_places} decimal places."):
            validator(123.456)  # 3 decimal places

        with pytest.raises(ValueError, match=f"Value must have at most {decimal_places} decimal places."):
            validator(0.123)    # 3 decimal places

        with pytest.raises(ValueError, match=f"Value must have at most {decimal_places} decimal places."):
            validator(1.23e-1) # Scientific notation, 2 decimal places (0.123)

        # Test with 0 decimal places
        decimal_places = 0
        validator = field.validate_max_decimal_places(decimal_places)

        # Valid cases
        validator(123.0)
        validator(123.)
        validator(123)
        validator(1e2)     # 100.0

        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must have at most {decimal_places} decimal places."):
            validator(123.1)

        with pytest.raises(ValueError, match=f"Value must have at most {decimal_places} decimal places."):
            validator(0.1)
