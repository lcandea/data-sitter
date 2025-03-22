import pytest
from data_sitter.field_types.IntegerField import IntegerField
from data_sitter.field_types.NumericField import NumericField


class TestIntegerField:
    def test_inheritance(self):
        """Test that IntegerField inherits from NumericField"""
        field = IntegerField("test_field")
        assert isinstance(field, NumericField)
        assert field.field_type == int
    
    def test_non_zero_validator(self):
        """Test that validate_non_zero works with integer values"""
        field = IntegerField("test_field")
        validator = field.validate_non_zero()
        
        # Valid cases
        validator(1)
        validator(-1)
        
        # Invalid case
        with pytest.raises(ValueError, match="Value cannot be zero."):
            validator(0)
    
    def test_positive_validator(self):
        """Test that validate_positive works with integer values"""
        field = IntegerField("test_field")
        validator = field.validate_positive()
        
        # Valid case
        validator(1)
        
        # Invalid cases
        with pytest.raises(ValueError, match="Value must be positive."):
            validator(0)
        
        with pytest.raises(ValueError, match="Value must be positive."):
            validator(-1)
    
    def test_negative_validator(self):
        """Test that validate_negative works with integer values"""
        field = IntegerField("test_field")
        validator = field.validate_negative()
        
        # Valid case
        validator(-1)
        
        # Invalid cases
        with pytest.raises(ValueError, match="Value must be less than zero."):
            validator(0)
        
        with pytest.raises(ValueError, match="Value must be less than zero."):
            validator(1)
    
    def test_min_validator(self):
        """Test that validate_min works with integer values"""
        field = IntegerField("test_field")
        min_val = 5
        validator = field.validate_min(min_val)
        
        # Valid cases
        validator(5)
        validator(6)
        
        # Invalid case
        with pytest.raises(ValueError, match=f"Value must be at least {min_val}."):
            validator(4)
    
    def test_max_validator(self):
        """Test that validate_max works with integer values"""
        field = IntegerField("test_field")
        max_val = 10
        validator = field.validate_max(max_val)
        
        # Valid cases
        validator(10)
        validator(9)
        
        # Invalid case
        with pytest.raises(ValueError, match=f"Value must not exceed {max_val}."):
            validator(11)
    
    def test_greater_than_validator(self):
        """Test that validate_greater_than works with integer values"""
        field = IntegerField("test_field")
        threshold = 7
        validator = field.validate_greater_than(threshold)
        
        # Valid case
        validator(8)
        
        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be greater than {threshold}."):
            validator(7)
        
        with pytest.raises(ValueError, match=f"Value must be greater than {threshold}."):
            validator(6)
    
    def test_less_than_validator(self):
        """Test that validate_less_than works with integer values"""
        field = IntegerField("test_field")
        threshold = 7
        validator = field.validate_less_than(threshold)
        
        # Valid case
        validator(6)
        
        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be less than {threshold}."):
            validator(7)
        
        with pytest.raises(ValueError, match=f"Value must be less than {threshold}."):
            validator(8)
    
    def test_between_validator(self):
        """Test that validate_between works with integer values"""
        field = IntegerField("test_field")
        min_val, max_val = 5, 10
        validator = field.validate_between(min_val, max_val, negative=False)
        
        # Valid case
        validator(7)
        
        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(5)  # Equal to min (exclusive)
            
        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(10)  # Equal to max (exclusive)
        
        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(4)  # Less than min
            
        with pytest.raises(ValueError, match=f"Value must be between {min_val} and {max_val}."):
            validator(11)  # Greater than max 