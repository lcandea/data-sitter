from .NumericField import NumericField
from ..rules import register_field


@register_field
class IntegerField(NumericField):
    field_type = int
