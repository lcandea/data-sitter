import re
from typing import Dict, Type

from pydantic import BaseModel
from rules import Resolver
from field_types import BaseField

res = Resolver()


class Contract:
    name: str
    field_validators: Dict[str, BaseField]

    def __init__(self, name) -> None:
        self.name: str = name
        self.field_validators = {}

    @classmethod
    def from_dict(cls, contract_dict: dict):
        if "name" not in contract_dict:
            raise ContractWithoutName()
        if "fields" not in contract_dict:
            raise ContractWithoutFields()

        contract = cls(contract_dict["name"])
        values = contract_dict.get('values', {})

        for field in contract_dict["fields"]:
            field_type = field["field_type"]
            field_type_class: Type[BaseField] = Resolver.get_type(field_type)

            field_instance = field_type_class(field["field_name"])

            for field_rule in field["field_rules"]:
                field_rule = replace_reference_for_values(field_rule, values)
                validator_rule, validator_params = res.resolve(field_type, field_rule)
                validator_rule(self=field_instance, **validator_params)
            contract.field_validators[field["field_name"]] = field_instance

        return contract

    def model_validate(self, item: dict):
        pydantic_model = self.get_pydantic_model()
        return pydantic_model.model_validate(item).model_dump()

    def get_pydantic_model(self) -> BaseModel:
        return type(self.name, (BaseModel,), {
            "__annotations__": {
                field_name: field_validator.get_annotation()
                for field_name, field_validator in self.field_validators.items()
            }
        })

def replace_reference_for_values(rule: str, values: dict) -> str:
    def replace_match(match):
        key = match.group(1)
        if key not in values:
            raise KeyError(f"Key '{key}' not found in values")
        return repr(values.get(key))
    # Regex to match references like $values.key
    pattern = r'\$values\.([a-zA-Z0-9_]+)'
    # Replace all matches in the rule
    return re.sub(pattern, replace_match, rule)


class ContractWithoutFields(Exception):
    pass


class ContractWithoutName(Exception):
    pass
