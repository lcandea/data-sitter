from field_types.NumericField import NumericField
from rules.Resolver import register_field


@register_field
class IntegerField(NumericField):
    field_type = int
