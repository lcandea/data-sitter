from typing import  Dict, List, Type, Union

from .field_types import BaseField
from .rules import Rule, ProcessedRule, LogicalRule, MatchedRule, RuleRegistry, LogicalOperator
from .rules.Parser import RuleParser


class RuleNotFoundError(Exception):
    """No matching rule found for the given parsed rule."""


class MalformedLogicalRuleError(Exception):
    """Logical rule structure not recognised."""


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

    def get_field_validator(
        self, name: str, parsed_rules: List[Union[str, dict]], description: str = None
    ) -> BaseField:
        field_validator = self.field_class(name, description)
        processed_rules = self.get_processed_rules(parsed_rules)
        validators = [pr.get_validator(field_validator) for pr in processed_rules]
        field_validator.validators = validators
        return field_validator

    def get_processed_rules(self, parsed_rules: List[Union[str, dict]]) -> List[ProcessedRule]:
        processed_rules = []
        for parsed_rule in parsed_rules:
            if isinstance(parsed_rule, dict):
                if len(keys := tuple(parsed_rule)) != 1 or (operator := keys[0]) not in LogicalOperator:
                    raise MalformedLogicalRuleError()
                if operator == LogicalOperator.NOT and not isinstance(parsed_rule[operator], list):
                    parsed_rule = {operator: [parsed_rule[operator]]}  # NOT operator can be a single rule
                processed_rule = LogicalRule(operator, self.get_processed_rules(parsed_rule[operator]))
            elif isinstance(parsed_rule, str):
                processed_rule = self._match_rule(parsed_rule)
                if not processed_rule:
                    raise RuleNotFoundError(f"Rule not found for parsed rule: '{parsed_rule}'")
            else:
                raise TypeError(f'Parsed Rule type not recognised: {type(parsed_rule)}')
            processed_rules.append(processed_rule)
        return processed_rules

    def _match_rule(self, parsed_rule: str) -> MatchedRule:
        if parsed_rule in self._match_rule_cache:
            return self._match_rule_cache[parsed_rule]

        for rule in self.rules:
            matched_rule = self.rule_parser.match(rule, parsed_rule)
            if matched_rule:
                self._match_rule_cache[parsed_rule] = matched_rule
                return matched_rule
        return None
