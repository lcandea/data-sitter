from typing import Union

from .BaseField import BaseField
from ..rules import register_rule, register_field

Numeric = Union[int, float]


@register_field
class NumericField(BaseField):
    field_type = Numeric

    @register_rule("Not Zero")
    def validate_non_zero(self):
        def validator(value: Numeric):
            if value == 0:
                raise ValueError("Value must not be zero")
            return value
        self.validators.append(validator)

    @register_rule("Positive")
    def validate_positive(self):
        def validator(value: Numeric):
            if value < 0:
                raise ValueError(f"Value {value} is not positive")
            return value
        self.validators.append(validator)

    @register_rule("Negative")
    def validate_negative(self):
        def validator(value: Numeric):
            if value >= 0:
                raise ValueError(f"Value {value} is not negative")
            return value
        self.validators.append(validator)

    @register_rule("Minimum {min_val:Number}")
    def validate_min(self, min_val: Numeric):
        def validator(value: Numeric):
            if value < min_val:
                raise ValueError(f"Value {value} is less than minimum {min_val}")
            return value
        self.validators.append(validator)

    @register_rule("Maximum {max_val:Number}")
    def validate_max(self, max_val: Numeric):
        def validator(value: Numeric):
            if value > max_val:
                raise ValueError(f"Value {value} exceeds maximum {max_val}")
            return value
        self.validators.append(validator)

    @register_rule("Greate than {threshold:Number}")
    def validate_greater_than(self, threshold: Numeric):
        def validator(value: Numeric):
            if value <= threshold:
                raise ValueError(f"Value {value} is not greater than {threshold}")
            return value
        self.validators.append(validator)

    @register_rule("Less than {threshold:Number}")
    def validate_less_than(self, threshold: Numeric):
        def validator(value: Numeric):
            if value >= threshold:
                raise ValueError(f"Value {value} is not less than {threshold}")
            return value
        self.validators.append(validator)

    @register_rule("Between {min_val:Number} and {max_val:Number}")
    def validate_between(self, min_val: Numeric, max_val: Numeric):
        def validator(value: Numeric):
            if not (min_val < value < max_val):
                raise ValueError(f"Value {value} not in Between {min_val} and {max_val}.")
            return value
        self.validators.append(validator)
