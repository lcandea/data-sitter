from typing import Callable, Dict, Optional

from parse import with_pattern, Parser
from parse_type import TypeBuilder

from .parser_utils import REF_PATTERN, get_value_from_reference, get_key_from_reference
from .alias_parameters_parser import NotCompatibleTypes, alias_parameters_types
from ..Rule import Rule
from ..MatchedRule import MatchedRule


CASE_SENSITIVE_RULES = False


class RuleParser:
    values: dict
    aliases: dict
    parsers: Dict[str, Parser]

    def __init__(self, values: dict):
        self.values = values
        self.parsers = {}
        self.aliases = self.get_aliases_with_reference_support()

    def match(self, rule: Rule, parsed_rule: str) -> Optional[MatchedRule]:
        parser = self.get_parser_for_rule(rule)
        parsed_values = parser.parse(parsed_rule)
        if parsed_values is None:
            return
        return MatchedRule(rule, parsed_rule, parsed_values.named, self.values)

    def get_parser_for_rule(self, rule: Rule) -> Parser:
        if rule.field_rule not in self.parsers:
            parser = Parser(rule.field_rule, extra_types=self.aliases, case_sensitive=CASE_SENSITIVE_RULES)
            self.parsers[rule.field_rule] = parser
        return self.parsers[rule.field_rule]

    def parse_reference_of(self, type_name: str, type_parser: Callable):
        _parser = Parser(f"{{value:{type_name}}}", extra_types={type_name: type_parser})

        def parse_reference(text):
            reference_value = get_value_from_reference(text, self.values)
            validation = _parser.parse(repr(reference_value))
            if validation is None:
                key = get_key_from_reference(text)
                raise NotCompatibleTypes(f"The reference value of '{key}' is not compatible with '{type_name}'.")
            return text
        return with_pattern(REF_PATTERN)(parse_reference)

    def get_aliases_with_reference_support(self):
        return {
            param_type: TypeBuilder.make_variant([parser_func, self.parse_reference_of(param_type, parser_func)])
            for param_type, parser_func in alias_parameters_types.items()
        }
