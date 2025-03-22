import pytest
import re
from data_sitter.field_types.StringField import StringField
from data_sitter.field_types.BaseField import BaseField


class TestStringField:
    def test_inheritance(self):
        """Test that StringField inherits from BaseField"""
        field = StringField("test_field")
        assert isinstance(field, BaseField)
        assert field.field_type == str

    def test_validate_not_empty(self):
        """Test validate_not_empty validator"""
        field = StringField("test_field")
        validator = field.validate_not_empty()

        # Valid case
        validator("test")

        # Invalid case
        with pytest.raises(ValueError, match="String cannot be empty."):
            validator("")

    def test_validate_starts_with(self):
        """Test validate_starts_with validator"""
        field = StringField("test_field")
        prefix = "prefix"
        validator = field.validate_starts_with(prefix)

        # Valid case
        validator("prefix_test")

        # Invalid case
        with pytest.raises(ValueError, match=f"Value must start with '{prefix}'"):
            validator("test")

    def test_validate_ends_with(self):
        """Test validate_ends_with validator"""
        field = StringField("test_field")
        suffix = "suffix"
        validator = field.validate_ends_with(suffix)

        # Valid case
        validator("test_suffix")

        # Invalid case
        with pytest.raises(ValueError, match=f"Value must end with '{suffix}'"):
            validator("test")

    def test_validate_in_positive(self):
        """Test validate_in validator with negative=False"""
        field = StringField("test_field")
        possible_values = ["one", "two", "three"]
        validator = field.validate_in(possible_values, negative=False)

        # Valid case
        validator("one")

        # Invalid case
        with pytest.raises(ValueError, match="Value 'four' must be one of the possible values"):
            validator("four")

    def test_validate_in_negative(self):
        """Test validate_in validator with negative=True"""
        field = StringField("test_field")
        possible_values = ["one", "two", "three"]
        validator = field.validate_in(possible_values, negative=True)

        # Valid case
        validator("four")

        # Invalid case
        with pytest.raises(ValueError, match="Value 'one' is not allowed"):
            validator("one")

    def test_validate_length_between(self):
        """Test validate_length_between validator"""
        field = StringField("test_field")
        min_val, max_val = 2, 5
        validator = field.validate_length_between(min_val, max_val)

        # Valid case
        validator("abc")

        # Invalid cases
        with pytest.raises(ValueError, match=f"Length must be between {min_val} and {max_val} characters"):
            validator("a")  # Too short
    
        with pytest.raises(ValueError, match=f"Length must be between {min_val} and {max_val} characters"):
            validator("abcdef")  # Too long

    def test_validate_max_length(self):
        """Test validate_max_length validator"""
        field = StringField("test_field")
        max_len = 5
        validator = field.validate_max_length(max_len)

        # Valid cases
        validator("abc")
        validator("abcde")

        # Invalid case
        with pytest.raises(ValueError, match=f"Length must not exceed {max_len} characters"):
            validator("abcdef")

    def test_validate_min_length(self):
        """Test validate_min_length validator"""
        field = StringField("test_field")
        min_len = 3
        validator = field.validate_min_length(min_len)

        # Valid cases
        validator("abc")
        validator("abcde")

        # Invalid case
        with pytest.raises(ValueError, match=f"Length must be at least {min_len} characters"):
            validator("ab")

    def test_validate_uppercase(self):
        """Test validate_uppercase validator"""
        field = StringField("test_field")
        validator = field.validate_uppercase()

        # Valid case
        validator("TEST")

        # Invalid case
        with pytest.raises(ValueError, match="Value must be in uppercase"):
            validator("Test")

        with pytest.raises(ValueError, match="Value must be in uppercase"):
            validator("test")

    def test_validate_lowercase(self):
        """Test validate_lowercase validator"""
        field = StringField("test_field")
        validator = field.validate_lowercase()

        # Valid case
        validator("test")

        # Invalid case
        with pytest.raises(ValueError, match="Value must be in lowercase"):
            validator("Test")

        with pytest.raises(ValueError, match="Value must be in lowercase"):
            validator("TEST")

    def test_validate_matches_regex(self):
        """Test validate_matches_regex validator"""
        field = StringField("test_field")
        pattern = r"^\d{3}-\d{2}-\d{4}$"  # SSN pattern
        validator = field.validate_matches_regex(pattern)

        # Valid case
        validator("123-45-6789")

        # Invalid case
        with pytest.raises(ValueError, match=re.escape(f"Value does not match the required pattern {pattern}.")):
            validator("12-345-6789")

        with pytest.raises(ValueError, match=re.escape(f"Value does not match the required pattern {pattern}.")):
            validator("abc")

    def test_validate_email(self):
        """Test validate_email validator"""
        field = StringField("test_field")
        validator = field.validate_email()

        # Valid cases
        validator("test@example.com")
        validator("user.name@domain.co.uk")

        # Invalid cases
        with pytest.raises(ValueError, match="Invalid email format"):
            validator("not-an-email")

        with pytest.raises(ValueError, match="Invalid email format"):
            validator("@example.com")

        with pytest.raises(ValueError, match="Invalid email format"):
            validator("test@")

    def test_validate_url(self):
        """Test validate_url validator"""
        field = StringField("test_field")
        validator = field.validate_url()

        # Valid cases
        validator("https://example.com")
        validator("http://example.com/path")
        validator("ftp://example.com")

        # Invalid cases
        with pytest.raises(ValueError, match="Invalid URL format"):
            validator("not-a-url")

        with pytest.raises(ValueError, match="Invalid URL format"):
            validator("example.com")

        with pytest.raises(ValueError, match="Invalid URL format"):
            validator("http:/example.com")

    def test_validate_no_digits(self):
        """Test validate_no_digits validator"""
        field = StringField("test_field")
        validator = field.validate_no_digits()

        # Valid case
        validator("test")
        validator("Test!@#")

        # Invalid case
        with pytest.raises(ValueError, match="Value must not contain any digits"):
            validator("test123")

        with pytest.raises(ValueError, match="Value must not contain any digits"):
            validator("1test")

        with pytest.raises(ValueError, match="Value must not contain any digits"):
            validator("test1") 