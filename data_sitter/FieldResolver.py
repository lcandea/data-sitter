from typing import  Dict, List, Type, Union

from .field_types import BaseField
from .rules import Rule, ProcessedRule, MatchedRule, RuleRegistry
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

    def get_field_validator(self, field_name: str, parsed_rules: List[Union[str, dict]]) -> BaseField:
        validator = self.field_class(field_name)
        processed_rules = self.get_processed_rules(parsed_rules)
        validators = [pr.get_validators(validator) for pr in processed_rules]
        validator.validators = validators
        return validator

    def get_processed_rules(self, parsed_rules: List[Union[str, dict]]) -> List[ProcessedRule]:
        processed_rules = []
        for parsed_rule in parsed_rules:
            if isinstance(parsed_rule, str):
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
