from field_types.NumericField import NumericField
from rules.Resolver import register_field


@register_field
class FloatField(NumericField):
    field_type = float
