import pytest
import pydantic
from pydantic import BaseModel

from data_sitter.field_types.BaseField import BaseField
from data_sitter.field_types.StringField import StringField
from data_sitter.rules import register_rule


# Create a chain of field types
class NumberField(BaseField):
    field_type = int

    @register_rule("Is positive")
    def validate_positive(self):
        def validator(value):
            if value <= 0:
                raise ValueError("Value must be positive")
            return value
        return validator

class PositiveIntegerField(NumberField):
    @register_rule("Is even")
    def validate_even(self):
        def validator(value):
            if value % 2 != 0:
                raise ValueError("Value must be even")
            return value
        return validator


class TestFieldIntegration:
    def test_field_combination(self):
        """Test combining multiple validators in a single field"""
        field = StringField("test_field")

        # Add multiple validators
        field.validators = [
            field.validator_not_null(),
            field.validate_not_empty(),
            field.validate_min_length(3),
            field.validate_max_length(10),
            field.validate_lowercase()
        ]

        # Valid case
        field.validate("valid")

        # Invalid cases - each in its own context
        with pytest.raises(ValueError, match="Value cannot be null"):
            field.validate(None)

        with pytest.raises(ValueError, match="String cannot be empty"):
            field.validate("")

        with pytest.raises(ValueError, match="Length must be at least 3 characters"):
            field.validate("ab")

        with pytest.raises(ValueError, match="Length must not exceed 10 characters"):
            field.validate("thisiswaytoolong")

        with pytest.raises(ValueError, match="Value must be in lowercase"):
            field.validate("UPPERCASE")

    def test_model_creation(self):
        """Test creating a Pydantic model with field annotations"""
        # Create and configure fields
        name_field = StringField("name")
        name_field.validators = [
            name_field.validator_not_null(),
            name_field.validate_not_empty(),
            name_field.validate_max_length(50)
        ]
        name_field.is_optional = False

        email_field = StringField("email")
        email_field.validators = [
            email_field.validator_not_null(),
            email_field.validate_email()
        ]
        email_field.is_optional = False

        # Create model dynamically
        class UserModel(BaseModel):
            name: name_field.get_annotation()
            email: email_field.get_annotation()

        # Valid case
        user = UserModel(name="John Doe", email="john@example.com")
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

        # Invalid cases - each in its own context
        with pytest.raises(pydantic.ValidationError):
            UserModel(name="", email="john@example.com")  # Empty name
    
        with pytest.raises(pydantic.ValidationError):
            UserModel(name="A" * 51, email="john@example.com")  # Name too long
    
        with pytest.raises(pydantic.ValidationError):
            UserModel(name="John Doe", email="not-an-email")  # Invalid email

    def test_inheritance_chain(self):
        """Test the inheritance chain and its effects on available validators"""

        # Create fields
        int_field = NumberField("number")
        int_field.validators = [
            int_field.validator_not_null(),
            int_field.validate_positive()
        ]
        int_field.is_optional = False

        # Test basic validators
        int_field.validate(5)  # Valid

        with pytest.raises(ValueError, match="Value must be positive"):
            int_field.validate(-5)
    
        # Test inheritance
        even_field = PositiveIntegerField("even_number")
        even_field.validators = [
            even_field.validator_not_null(),
            even_field.validate_positive(),
            even_field.validate_even()
        ]
        even_field.is_optional = False

        even_field.validate(6)  # Valid

        with pytest.raises(ValueError, match="Value must be positive"):
            even_field.validate(-6)
    
        with pytest.raises(ValueError, match="Value must be even"):
            even_field.validate(5)
