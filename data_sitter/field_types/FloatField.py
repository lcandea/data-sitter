from .NumericField import NumericField
from ..rules import register_field


@register_field
class FloatField(NumericField):
    field_type = float
