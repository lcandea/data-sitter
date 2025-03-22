from .NumericField import NumericField
from ..rules import register_field, register_rule
from decimal import Decimal


@register_field
class FloatField(NumericField):
    field_type = float

    @register_rule("Has at most {decimal_places:Integer} decimal places")
    def validate_max_decimal_places(self, decimal_places: int):
        def validator(value):
            decimal_str = str(Decimal(str(value)).normalize())
            # If no decimal point or only zeros after decimal, it has 0 decimal places
            if '.' not in decimal_str:
                decimal_places_count = 0
            else:
                decimal_places_count = len(decimal_str.split('.')[1])

            if decimal_places_count > decimal_places:
                raise ValueError(f"Value must have at most {decimal_places} decimal places.")
            return value
        return validator
