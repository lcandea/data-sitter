from abc import ABC
from typing import Annotated, List, Type

from pydantic import AfterValidator
from ..rules import register_rule, register_field


def aggregated_validator(validators: List[callable]):
    def _validator(value):
        for validator_func in validators:
            validator_func(value)
        return value
    return _validator

@register_field
class BaseField(ABC):
    name: str
    validators = None
    field_type = None

    def __init__(self, name) -> None:
        self.name = name
        self.validators = []

    @register_rule("Validate Not Null")
    def validator_not_null(self):
        def _validator(value):
            if value is None:
                raise ValueError()
            return value

        self.validators.append(_validator)

    def validate(self, value):
        for validator in self.validators:
            validator(value)

    def get_annotation(self):
        return Annotated[self.field_type, AfterValidator(aggregated_validator(self.validators))]

    @classmethod
    def get_parents(cls: Type["BaseField"]) -> List[Type["BaseField"]]:
        if cls.__name__ == "BaseField":
            return []
        ancestors = []
        for base in cls.__bases__:
            if base.__name__.endswith("Field"):
                ancestors.append(base)
                ancestors.extend(base.get_parents())  # It wont break because we have a base case
        return ancestors
