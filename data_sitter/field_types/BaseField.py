from abc import ABC
from typing import Annotated, List, Optional, Type

from pydantic import AfterValidator
from ..rules import register_rule, register_field


def aggregated_validator(validators: List[callable], is_optional: bool):
    def _validator(value):
        if is_optional and value is None:
            return value
        for validator_func in validators:
            validator_func(value)
        return value
    return _validator

@register_field
class BaseField(ABC):
    name: str
    is_optional: bool
    validators = None
    field_type = None

    def __init__(self, name: str) -> None:
        self.name = name
        self.is_optional = True
        self.validators = []

    @register_rule("Is not null")
    def validator_not_null(self):
        def _validator(value):
            if self.is_optional:
                return value
            if value is None:
                raise ValueError("Value cannot be null.")
            return value

        self.is_optional = False
        self.validators.append(_validator)

    def validate(self, value):
        for validator in self.validators:
            validator(value)

    def get_annotation(self):
        field_type = Optional[self.field_type] if self.is_optional else self.field_type
        return Annotated[field_type, AfterValidator(aggregated_validator(self.validators, self.is_optional))]

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
