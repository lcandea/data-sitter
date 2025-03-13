from typing import List

from .BaseField import BaseField
from ..rules import register_rule, register_field


@register_field
class StringField(BaseField):
    field_type = str

    @register_rule("Is not empty")
    def validate_not_empty(self):
        def validator(value: str):
            if value == "":
                raise ValueError("The value is empty")
            return value
        self.validators.append(validator)

    @register_rule("Starts with {prefix:String}")
    def validate_starts_with(self, prefix: List[str]):
        def validator(value: str):
            if not value.startswith(prefix):
                raise ValueError(f"The value '{value}' does not start with '{prefix}'.")
            return value
        self.validators.append(validator)

    @register_rule("Ends with {sufix:String}")
    def validate_ends_with(self, sufix: List[str]):
        def validator(value: str):
            if not value.endswith(sufix):
                raise ValueError(f"The value '{value}' does not ends with '{sufix}'.")
            return value
        self.validators.append(validator)

    @register_rule("Value in {possible_values:Strings}")
    def validate_in(self, possible_values: List[str]):
        def validator(value: str):
            if value not in possible_values:
                raise ValueError(f"The value '{value}' is not in the list.")
            return value
        self.validators.append(validator)

    @register_rule("Length between {min_val:Integer} and {max_val:Integer}")
    def validate_length_between(self, min_val: int, max_val: int):
        def validator(value: str):
            if not (min_val < len(value) < max_val):
                raise ValueError(f"Length {len(value)} is not in between {min_val} and {max_val}.")
            return value
        self.validators.append(validator)

    @register_rule("Maximum length of {max_len:Integer}")
    def validate_max_length(self, max_len: int):
        def validator(value: str):
            if len(value) > max_len:
                raise ValueError(f"Length {len(value)} is longer than {max_len}.")
            return value
        self.validators.append(validator)

    @register_rule("Length shorter than {max_len:Integer}")
    def validate_shorter_than(self, max_len: int):
        def validator(value: str):
            if len(value) >= max_len:
                raise ValueError(f"Length {len(value)} is not in shorter than {max_len}.")
            return value
        self.validators.append(validator)

    @register_rule("Minimum length of {min_len:Integer}")
    def validate_min_length(self, min_len: int):
        def validator(value: str):
            if len(value) < min_len:
                raise ValueError(f"Length {len(value)} is shorter than {min_len}.")
            return value
        self.validators.append(validator)

    @register_rule("Length longer than {min_len:Integer}")
    def validate_longer_than(self, min_len: int):
        def validator(value: str):
            if len(value) <= min_len:
                raise ValueError(f"Length {len(value)} is not in longer than {min_len}.")
            return value
        self.validators.append(validator)

    @register_rule("Is uppercase")
    def validate_uppercase(self):
        def validator(value: str):
            if not value.isupper():
                raise ValueError("Not Uppercase")
            return value
        self.validators.append(validator)
