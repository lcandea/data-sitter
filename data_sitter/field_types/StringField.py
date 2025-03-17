import re
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
                raise ValueError("String cannot be empty.")
            return value
        self.validators.append(validator)

    @register_rule("Starts with {prefix:String}")
    def validate_starts_with(self, prefix: List[str]):
        def validator(value: str):
            if not value.startswith(prefix):
                raise ValueError(f"Value must start with '{prefix}'.")
            return value
        self.validators.append(validator)

    @register_rule("Ends with {suffix:String}")
    def validate_ends_with(self, suffix: List[str]):
        def validator(value: str):
            if not value.endswith(suffix):
                raise ValueError(f"Value must end with '{suffix}'.")
            return value
        self.validators.append(validator)

    @register_rule("Is one of {possible_values:Strings}", fixed_params={"negative": False})
    @register_rule("Is not one of {possible_values:Strings}", fixed_params={"negative": True})
    def validate_in(self, possible_values: List[str], negative: bool):
        def validator(value: str):
            condition = value in possible_values
            if condition and negative:
                raise ValueError(f"Value '{value}' is not allowed.")
            if not condition and not negative:
                raise ValueError(f"Value '{value}' must be one of the possible values.")
            return value
        self.validators.append(validator)

    @register_rule("Has length between {min_val:Integer} and {max_val:Integer}")
    def validate_length_between(self, min_val: int, max_val: int):
        def validator(value: str):
            if not (min_val < len(value) < max_val):
                raise ValueError(f"Length must be between {min_val} and {max_val} characters.")
            return value
        self.validators.append(validator)

    @register_rule("Has maximum length {max_len:Integer}")
    def validate_max_length(self, max_len: int):
        def validator(value: str):
            if len(value) > max_len:
                raise ValueError(f"Length must not exceed {max_len} characters.")
            return value
        self.validators.append(validator)

    @register_rule("Has minimum length {min_len:Integer}")
    def validate_min_length(self, min_len: int):
        def validator(value: str):
            if len(value) < min_len:
                raise ValueError(f"Length must be at least {min_len} characters.")
            return value
        self.validators.append(validator)

    @register_rule("Is uppercase")
    def validate_uppercase(self):
        def validator(value: str):
            if not value.isupper():
                raise ValueError("Value must be in uppercase.")
            return value
        self.validators.append(validator)

    @register_rule("Is lowercase")
    def validate_lowercase(self):
        def validator(value: str):
            if not value.islower():
                raise ValueError("Value must be in lowercase.")
            return value
        self.validators.append(validator)

    @register_rule("Matches regex {pattern:String}")
    def validate_matches_regex(self, pattern: str):
        def validator(value: str):
            if not re.match(pattern, value):
                raise ValueError(f"Value does not match the required pattern {pattern}.")
            return value
        self.validators.append(validator)

    @register_rule("Is valid email")
    def validate_email(self):
        EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        def validator(value: str):
            if not re.match(EMAIL_REGEX, value):
                raise ValueError("Invalid email format.")
            return value
        self.validators.append(validator)

    @register_rule("Is valid URL")
    def validate_url(self):
        URL_REGEX = r"^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$"

        def validator(value: str):
            if not re.match(URL_REGEX, value):
                raise ValueError("Invalid URL format.")
            return value
        self.validators.append(validator)

    @register_rule("Has no digits")
    def validate_no_digits(self):
        def validator(value: str):
            if any(char.isdigit() for char in value):
                raise ValueError("Value must not contain any digits.")
            return value
        self.validators.append(validator)
