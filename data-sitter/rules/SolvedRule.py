import re
from typing import Type

from field_types import BaseField
from rules import Resolver

res = Resolver()


class SolvedRule:
    field_class: Type[BaseField]
    rule_alias: str
    rule_setter: callable
    rule_reff_params: set
    rule_params: dict
    rule: str
    values: dict

    def __init__(self, field_class: Type[BaseField], rule: str, values: dict):
        self.field_class = field_class
        self.rule = rule
        self.values = values
        self.rule_reff_params = set()

        rule_setter, rule_params, rule_alias = res.resolve(field_class, self.rule_with_values)
        self.rule_setter = rule_setter
        self.rule_params = rule_params
        self.rule_alias = rule_alias

    @property
    def rule_with_values(self):
        def replace_match(match):
            key = match.group(1)
            if key not in self.values:
                raise KeyError(f"Key '{key}' not found in values")
            self.rule_reff_params.add(key)
            return repr(self.values.get(key))
        # Regex to match references like $values.key
        pattern = r'\$values\.([a-zA-Z0-9_]+)'
        # Replace all matches in the rule
        return re.sub(pattern, replace_match, self.rule)

    @property
    def original_params(self):
        print(self.rule, self.rule_reff_params)
        return {k: f'$values.{k}' if k in self.rule_reff_params else v for k, v in self.rule_params.items()}


    def add_to_instance(self, field_instance: BaseField):
        if not isinstance(field_instance, self.field_class):
            raise InvalidFieldTypeError(
                f"Cannot add rule to {type(field_instance).__name__}, expected {self.field_class.__name__}."
            )
        self.rule_setter(self=field_instance, **self.rule_params)
        


class InvalidFieldTypeError(TypeError):
    """Raised when attempting to add a rule to an incompatible field type."""
