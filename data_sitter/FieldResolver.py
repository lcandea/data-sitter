from typing import  Dict, List, Type

from .field_types import BaseField
from .rules import MatchedRule, Rule, RuleRegistry
from .rules.Parser import RuleParser


class RuleNotFoundError(Exception):
    """No matching rule found for the given parsed rule."""


class FieldResolver:
    field_class: Type[BaseField]
    rule_parser: RuleParser
    rules: List[Rule]
    _match_rule_cache: Dict[str, MatchedRule]

    def __init__(self, field_class: Type[BaseField], rule_parser: RuleParser) -> None:
        self.field_class = field_class
        self.rule_parser = rule_parser
        self.rules = RuleRegistry.get_rules_for(field_class)
        self._match_rule_cache = {}

    def get_matched_rules(self, parsed_rules: List[str]) -> List[MatchedRule]:
        matched_rules = []
        for parsed_rule in parsed_rules:
            matched_rule = self.match_rule(parsed_rule)
            if not matched_rule:
                raise RuleNotFoundError(f"Rule not found for parsed rule: '{parsed_rule}'")
            matched_rules.append(matched_rule)
        return matched_rules

    def get_field_validator(self, field_name: str, parsed_rules: List[str]) -> BaseField:
        validator = self.field_class(field_name)
        matched_rules = self.get_matched_rules(parsed_rules)
        for matched_rule in matched_rules:
            matched_rule.add_to_instance(validator)
        return validator

    def match_rule(self, parsed_rule: str) -> MatchedRule:
        if parsed_rule in self._match_rule_cache:
            return self._match_rule_cache[parsed_rule]

        for rule in self.rules:
            matched_rule = self.rule_parser.match(rule, parsed_rule)
            if matched_rule:
                self._match_rule_cache[parsed_rule] = matched_rule
                return matched_rule
        return None
