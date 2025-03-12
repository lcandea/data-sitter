from typing import Dict, List, Type

from pydantic import BaseModel
from rules import SolvedRule, Resolver
from field_types import BaseField


class Contract:
    name: str
    field_validators: Dict[str, BaseField]
    rules: Dict[str, List[SolvedRule]]


    def __init__(self, name) -> None:
        self.name: str = name
        self.field_validators = {}
        self.rules = {}

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
            contract.rules[field["field_name"]] = []

            field_type_class: Type[BaseField] = Resolver.get_type(field_type)
            field_instance = field_type_class(field["field_name"])

            for field_rule in field["field_rules"]:
                rule = SolvedRule(field_type_class, field_rule, values)
                rule.add_to_instance(field_instance)
                contract.rules[field["field_name"]].append(rule)
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
    
    def get_front_end_contract(self):
        return {
            "name": self.name,
            "fields": [
                {
                    "field_name": field_name,
                    "field_type": field_validator.__class__.__name__,
                    "field_rules": [
                        {
                            "rule": rule.rule_alias,
                            "rule_params": rule.original_params
                        }
                        for rule in self.rules[field_name]
                    ]
                }
                for field_name, field_validator in self.field_validators.items()
            ]
        }


class ContractWithoutFields(Exception):
    pass


class ContractWithoutName(Exception):
    pass
