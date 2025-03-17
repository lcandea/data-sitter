from .NumericField import NumericField
from ..rules import register_field, register_rule


@register_field
class FloatField(NumericField):
    field_type = float

    @register_rule("Has at most {decimal_places:Integer} decimal places")
    def validate_max_decimal_places(self, decimal_places: int):
        def validator(value):
            if not isinstance(value, float):
                raise ValueError("Value must be a floating-point number.")
            if len(str(value).split(".")[1]) > decimal_places:
                raise ValueError(f"Value must have at most {decimal_places} decimal places.")
            return value
        self.validators.append(validator)
