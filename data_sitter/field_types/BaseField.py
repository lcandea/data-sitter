from abc import ABC
from typing import Annotated, Callable, List, Optional, Type

from pydantic import AfterValidator

from .FieldTypes import FieldTypes
from ..rules import register_rule, register_field


class NotInitialisedError(Exception):
    """The field instance is initialised without validators"""


def aggregated_validator(validators: List[Callable], is_optional: bool):
    def validator(value):
        if is_optional and value is None:
            return value
        for validator_func in validators:
            validator_func(value)
        return value
    return validator

@register_field
class BaseField(ABC):
    name: str
    is_optional: bool
    validators = None
    field_type = None
    type_name = FieldTypes.BASE

    def __init__(self, name: str) -> None:
        self.name = name
        self.is_optional = True
        self.validators = None

    @register_rule("Is not null")
    def validator_not_null(self):
        def validator(value):
            if value is None:
                raise ValueError("Value cannot be null.")
            return value

        self.is_optional = False
        return validator

    def validate(self, value):
        if self.validators is None:
            raise NotInitialisedError()
        for validator in self.validators:
            validator(value)

    def get_annotation(self):
        if self.validators is None:
            raise NotInitialisedError()
        field_type = Optional[self.field_type] if self.is_optional else self.field_type
        return Annotated[field_type, AfterValidator(aggregated_validator(self.validators, self.is_optional))]

    @classmethod
    def get_parents(cls: Type["BaseField"]) -> List[Type["BaseField"]]:
        if cls == BaseField:
            return []
        ancestors = set()
        for base in cls.__bases__:
            if issubclass(base, BaseField):
                ancestors.add(base)
                ancestors.update(base.get_parents())
        return list(ancestors)
