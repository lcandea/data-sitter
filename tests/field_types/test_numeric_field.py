import pytest
from data_sitter.field_types.NumericField import NumericField
from data_sitter.field_types.BaseField import BaseField


class TestNumericField:
    def test_inheritance(self):
        """Test that NumericField inherits from BaseField"""
        field = NumericField("test_field")
        assert isinstance(field, BaseField)
        assert field.field_type.__name__ == "Union"  # Should be Union[int, float]
    
    def test_validate_non_zero(self):
        """Test validate_non_zero validator"""
        field = NumericField("test_field")
        validator = field.validate_non_zero()
        
        # Valid cases
        validator(1)
        validator(-1)
        validator(0.5)
        
        # Invalid case
        with pytest.raises(ValueError, match="Value cannot be zero."):
            validator(0)
    
    def test_validate_positive(self):
        """Test validate_positive validator"""
        field = NumericField("test_field")
        validator = field.validate_positive()
        
        # Valid cases
        validator(1)
        validator(0.1)
        
        # Invalid cases
        with pytest.raises(ValueError, match="Value must be positive."):
            validator(0)
        
        with pytest.raises(ValueError, match="Value must be positive."):
            validator(-1)
    
    def test_validate_negative(self):
        """Test validate_negative validator"""
        field = NumericField("test_field")
        validator = field.validate_negative()
        
        # Valid case
        validator(-1)
        validator(-0.1)
        
        # Invalid cases
        with pytest.raises(ValueError, match="Value must be less than zero."):
            validator(0)
        
        with pytest.raises(ValueError, match="Value must be less than zero."):
            validator(1)
    
    def test_validate_min(self):
        """Test validate_min validator"""
        field = NumericField("test_field")
        min_val = 5
        validator = field.validate_min(min_val)
        
        # Valid cases
        validator(5)
        validator(6)
        
        # Invalid case
        with pytest.raises(ValueError, match=f"Value must be at least {min_val}."):
            validator(4)
    
    def test_validate_max(self):
        """Test validate_max validator"""
        field = NumericField("test_field")
        max_val = 10
        validator = field.validate_max(max_val)
        
        # Valid cases
        validator(10)
        validator(9)
        
        # Invalid case
        with pytest.raises(ValueError, match=f"Value must not exceed {max_val}."):
            validator(11)
    
    def test_validate_greater_than(self):
        """Test validate_greater_than validator"""
        field = NumericField("test_field")
        threshold = 7
        validator = field.validate_greater_than(threshold)
        
        # Valid case
        validator(8)
        
        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be greater than {threshold}."):
            validator(7)
        
        with pytest.raises(ValueError, match=f"Value must be greater than {threshold}."):
            validator(6)
    
    def test_validate_less_than(self):
        """Test validate_less_than validator"""
        field = NumericField("test_field")
        threshold = 7
        validator = field.validate_less_than(threshold)
        
        # Valid case
        validator(6)
        
        # Invalid cases
        with pytest.raises(ValueError, match=f"Value must be less than {threshold}."):
            validator(7)
        
        with pytest.raises(ValueError, match=f"Value must be less than {threshold}."):
            validator(8)
    
    def test_validate_between_positive(self):
        """Test validate_between validator with negative=False"""
        field = NumericField("test_field")
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
    
    def test_validate_between_negative(self):
        """Test validate_between validator with negative=True"""
        field = NumericField("test_field")
        min_val, max_val = 5, 10
        validator = field.validate_between(min_val, max_val, negative=True)
        
        # Valid cases
        validator(4)  # Less than min
        validator(11)  # Greater than max
        validator(5)  # Equal to min (exclusive)
        validator(10)  # Equal to max (exclusive)
        
        # Invalid case
        with pytest.raises(ValueError, match=f"Value must not be between {min_val} and {max_val}."):
            validator(7) 