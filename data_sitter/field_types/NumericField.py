from typing import Union

from .BaseField import BaseField
from ..rules import register_rule, register_field

Numeric = Union[int, float]


@register_field
class NumericField(BaseField):
    field_type = Numeric

    @register_rule("Is not zero")
    def validate_non_zero(self):
        def validator(value: Numeric):
            if value == 0:
                raise ValueError("Value cannot be zero.")
            return value
        self.validators.append(validator)

    @register_rule("Is positive")
    def validate_positive(self):
        def validator(value: Numeric):
            if value < 0:
                raise ValueError("Value must be positive.")
            return value
        self.validators.append(validator)

    @register_rule("Is negative")
    def validate_negative(self):
        def validator(value: Numeric):
            if value >= 0:
                raise ValueError("Value must be less than zero.")
            return value
        self.validators.append(validator)

    @register_rule("Is at least {min_val:Number}")
    def validate_min(self, min_val: Numeric):
        def validator(value: Numeric):
            if value < min_val:
                raise ValueError(f"Value must be at least {min_val}.")
            return value
        self.validators.append(validator)

    @register_rule("Is at most {max_val:Number}")
    def validate_max(self, max_val: Numeric):
        def validator(value: Numeric):
            if value > max_val:
                raise ValueError(f"Value must not exceed {max_val}.")
            return value
        self.validators.append(validator)

    @register_rule("Is greater than {threshold:Number}")
    def validate_greater_than(self, threshold: Numeric):
        def validator(value: Numeric):
            if value <= threshold:
                raise ValueError(f"Value must be greater than {threshold}.")
            return value
        self.validators.append(validator)

    @register_rule("Is less than {threshold:Number}")
    def validate_less_than(self, threshold: Numeric):
        def validator(value: Numeric):
            if value >= threshold:
                raise ValueError(f"Value must be less than {threshold}.")
            return value
        self.validators.append(validator)

    @register_rule("Is between {min_val:Number} and {max_val:Number}", fixed_params={"negative": False})
    @register_rule("Is not between {min_val:Number} and {max_val:Number}", fixed_params={"negative": True})
    def validate_between(self, min_val: Numeric, max_val: Numeric, negative: bool):
        def validator(value: Numeric):
            condition = (min_val < value < max_val)
            if condition and negative:
                raise ValueError(f"Value must not be between {min_val} and {max_val}.")
            if not condition and not negative:
                raise ValueError(f"Value must be between {min_val} and {max_val}.")
            return value
        self.validators.append(validator)
