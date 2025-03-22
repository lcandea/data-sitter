import pytest
import json
import yaml

from data_sitter import Contract


@pytest.fixture
def sample_contract_dict():
    return {
        "name": "TestContract",
        "fields": [
            {
                "field_name": "name",
                "field_type": "StringField",
                "field_rules": [
                    "Is not null",
                    "Has minimum length 3"
                ]
            },
            {
                "field_name": "age",
                "field_type": "IntegerField",
                "field_rules": [
                    "Is not null",
                    "Is at least 18"
                ]
            }
        ],
        "values": {
            "min_age": 18
        }
    }


@pytest.fixture
def sample_contract(sample_contract_dict):
    return Contract.from_dict(sample_contract_dict)


class TestContract:
    def test_contract_creation(self, sample_contract):
        """Test basic contract creation from dictionary"""
        assert sample_contract.name == "TestContract"
        assert len(sample_contract.fields) == 2
        assert sample_contract.fields[0].field_name == "name"
        assert sample_contract.fields[0].field_type == "StringField"
        assert "Is not null" in sample_contract.fields[0].field_rules

    def test_from_dict(self, sample_contract_dict):
        """Test contract creation from dictionary"""
        contract = Contract.from_dict(sample_contract_dict)
        assert contract.name == "TestContract"
        assert len(contract.fields) == 2

    def test_from_json(self, sample_contract_dict):
        """Test contract creation from JSON string"""
        contract_json = json.dumps(sample_contract_dict)
        contract = Contract.from_json(contract_json)
        assert contract.name == "TestContract"
        assert len(contract.fields) == 2

    def test_from_yaml(self, sample_contract_dict):
        """Test contract creation from YAML string"""
        contract_yaml = yaml.dump(sample_contract_dict)
        contract = Contract.from_yaml(contract_yaml)
        assert contract.name == "TestContract"
        assert len(contract.fields) == 2

    def test_missing_name(self):
        """Test that ContractWithoutName is raised when name is missing"""
        from data_sitter.Contract import ContractWithoutName

        contract_dict = {
            "fields": [
                {
                    "field_name": "name",
                    "field_type": "StringField",
                    "field_rules": ["required"]
                }
            ]
        }
        with pytest.raises(ContractWithoutName):
            Contract.from_dict(contract_dict)

    def test_missing_fields(self):
        """Test that ContractWithoutFields is raised when fields are missing"""
        from data_sitter.Contract import ContractWithoutFields

        contract_dict = {
            "name": "TestContract"
        }
        with pytest.raises(ContractWithoutFields):
            Contract.from_dict(contract_dict)

    def test_field_validators(self, sample_contract):
        """Test that field validators are correctly created"""
        validators = sample_contract.field_validators
        assert "name" in validators
        assert "age" in validators
        assert validators["name"].__class__.__name__ == "StringField"
        assert validators["age"].__class__.__name__ == "IntegerField"

    def test_rules(self, sample_contract):
        """Test that rules are correctly parsed and processed"""
        rules = sample_contract.rules
        assert "name" in rules
        assert "age" in rules
        assert len(rules["name"]) == 2
        assert rules["name"][0].parsed_rule == "Is not null"
        assert rules["name"][1].parsed_rule == "Has minimum length 3"

    def test_pydantic_model(self, sample_contract):
        """Test that a valid pydantic model is created"""
        model = sample_contract.pydantic_model
        assert model.__name__ == "TestContract"
        fields = model.model_json_schema()["properties"]
        assert "name" in fields
        assert "age" in fields

    def test_validate_valid_data(self, sample_contract):
        """Test validation with valid data"""
        valid_data = {
            "name": "John Doe",
            "age": 25
        }
        validation = sample_contract.validate(valid_data)
        assert validation.errors is None
        assert validation.unknowns is None
        assert validation.item["name"] == "John Doe"
        assert validation.item["age"] == 25

    def test_validate_invalid_data(self, sample_contract):
        """Test validation with invalid data"""
        invalid_data = {
            "name": "Jo",  # too short
            "age": 16,     # under minimum age
            "extra": "value"  # unknown field
        }
        validation = sample_contract.validate(invalid_data)
        assert "name" in validation.errors
        assert "age" in validation.errors
        assert validation.unknowns == {"extra": "value"}

    def test_get_json_contract(self, sample_contract):
        """Test JSON contract generation"""
        json_contract = sample_contract.get_json_contract()
        contract_dict = json.loads(json_contract)
        assert contract_dict["name"] == "TestContract"
        assert len(contract_dict["fields"]) == 2

    def test_get_yaml_contract(self, sample_contract):
        """Test YAML contract generation"""
        yaml_contract = sample_contract.get_yaml_contract()
        contract_dict = yaml.safe_load(yaml_contract)
        assert contract_dict["name"] == "TestContract"
        assert len(contract_dict["fields"]) == 2

    def test_get_front_end_contract(self, sample_contract):
        """Test front-end contract representation"""
        frontend_contract = sample_contract.get_front_end_contract()
        assert frontend_contract["name"] == "TestContract"
        assert len(frontend_contract["fields"]) == 2
        # Check that rules have front-end representation
        assert isinstance(frontend_contract["fields"][0]["field_rules"], list)
