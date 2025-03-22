import pytest
from typing import Optional, Dict, List

from pydantic import BaseModel, Field
from data_sitter.Validation import Validation


class TestModel(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(ge=18)
    email: Optional[str] = None


@pytest.fixture
def test_model():
    return TestModel


@pytest.fixture
def valid_item():
    return {
        "name": "John Doe",
        "age": 25,
        "email": "john@example.com"
    }


@pytest.fixture
def invalid_item():
    return {
        "name": "Jo",  # too short
        "age": 16,     # below 18
        "email": "invalid-email",
        "unknown_field": "some value"
    }


class TestValidation:
    def test_init(self):
        """Test initialization of Validation class"""
        item = {"name": "Test"}
        errors = {"name": ["too short"]}
        unknowns = {"extra": "value"}

        validation = Validation(item, errors, unknowns)

        assert validation.item == item
        assert validation.errors == errors
        assert validation.unknowns == unknowns

    def test_init_with_defaults(self):
        """Test initialization with default values"""
        item = {"name": "Test"}
        validation = Validation(item)

        assert validation.item == item
        assert validation.errors is None
        assert validation.unknowns is None

    def test_to_dict_with_all_fields(self):
        """Test to_dict method when all fields are present"""
        item = {"name": "Test"}
        errors = {"name": ["too short"]}
        unknowns = {"extra": "value"}

        validation = Validation(item, errors, unknowns)
        result = validation.to_dict()

        assert result == {
            "item": item,
            "errors": errors,
            "unknowns": unknowns
        }

    def test_to_dict_with_no_errors_or_unknowns(self):
        """Test to_dict method when errors and unknowns are None"""
        item = {"name": "Test"}
        validation = Validation(item)
        result = validation.to_dict()

        assert result == {"item": item}
        assert "errors" not in result
        assert "unknowns" not in result

    def test_validate_valid_data(self, test_model, valid_item):
        """Test validate method with valid data"""
        validation = Validation.validate(test_model, valid_item)

        assert validation.errors is None
        assert validation.unknowns is None
        assert validation.item["name"] == "John Doe"
        assert validation.item["age"] == 25
        assert validation.item["email"] == "john@example.com"

    def test_validate_invalid_data(self, test_model, invalid_item):
        """Test validate method with invalid data"""
        validation = Validation.validate(test_model, invalid_item)

        # Check errors
        assert "name" in validation.errors
        assert "age" in validation.errors

        # Check unknowns
        assert validation.unknowns == {"unknown_field": "some value"}

        # Ensure item still has all expected fields
        assert "name" in validation.item
        assert "age" in validation.item
        assert "email" in validation.item

    def test_validate_missing_fields(self, test_model):
        """Test validate method with missing fields"""
        item = {"age": 20}  # Missing required 'name' field
        validation = Validation.validate(test_model, item)

        assert "name" in validation.errors
        assert validation.item["name"] is None
        assert validation.item["age"] == 20
        assert validation.item["email"] is None

    def test_validate_empty_input(self, test_model):
        """Test validate method with empty input"""
        validation = Validation.validate(test_model, {})

        assert "name" in validation.errors  # 'name' is required
        assert "age" in validation.errors   # 'age' is required
        assert validation.item["name"] is None
        assert validation.item["age"] is None
        assert validation.item["email"] is None
        assert validation.unknowns == None
