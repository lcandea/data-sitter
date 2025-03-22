from typing import TYPE_CHECKING, Any, Callable, Dict

from .Rule import Rule
from .RuleRegistry import RuleRegistry
from .ProcessedRule import ProcessedRule, MatchedParsedRule
from .Parser.parser_utils import get_value_from_reference

if TYPE_CHECKING:  # pragma: no cover
    from ..field_types import BaseField


class RuleParsedValuesMismatch(Exception):
    pass


class MatchedRule(ProcessedRule):
    parsed_rule: MatchedParsedRule
    parsed_values: Dict[str, Any]
    values: Dict[str, Any]

    def __init__(self,
        rule: Rule,
        parsed_rule: str,
        parsed_values: Dict[str, Any],
        values: Dict[str, Any]
    ):
        super().__init__(**vars(rule))
        self.parsed_rule = parsed_rule
        self.parsed_values = parsed_values
        self.values = values
        self.__validate_rule_parsed_values()

    @property
    def resolved_values(self) -> Dict[str, Any]:
        resolved = {}
        for rule_param, param_value in self.parsed_values.items():
            if isinstance(param_value, str) and param_value.startswith('$'):
                resolved[rule_param] = get_value_from_reference(param_value, self.values)
            else:
                resolved[rule_param] = param_value
        return resolved

    def __validate_rule_parsed_values(self):
        parsed_values_values = set(self.parsed_values.keys())
        if set(self.rule_params) != parsed_values_values:
            raise RuleParsedValuesMismatch(f"Rule Params: {self.rule_params}, Parsed Values: {parsed_values_values}")

    def get_validator(self, field_instance: "BaseField") -> Callable:
        field_class = RuleRegistry.get_type(self.field_type)
        if not isinstance(field_instance, field_class):
            raise TypeError(f"Cannot add rule to {type(field_instance).__name__}, expected {self.field_type}.")
        return self.rule_setter(self=field_instance, **self.resolved_values)

    def get_front_end_repr(self) -> dict:
        return {
            "rule": self.field_rule,
            "parsed_rule": self.parsed_rule,
            "rule_params": self.rule_params,
            "parsed_values": self.parsed_values,
        }
