import logging
from parse import Parser

from rules.alias_parameters_parser import alias_parameters_types


CASE_SENSITIVE_RULES = False

logger = logging.getLogger(__name__)


class Rule:
    rule_alias: str
    rule_setter: callable
    alias_parser: Parser

    def __init__(self, rule_alias: str, rule_setter: callable) -> None:
        self.rule_alias = rule_alias
        self.rule_setter = rule_setter
        self.alias_parser = Parser(rule_alias, extra_types=alias_parameters_types, case_sensitive=CASE_SENSITIVE_RULES)

    # @classmethod
    # def add_parser(cls, parser: Parser) -> None:
    #     cls._class_parser = parser

    # @classmethod
    # def register_type(cls, **kwargs) -> None:
    #     cls._class_parser.register_type(**kwargs)

    def match(self, rule_str: str):
        match = self.alias_parser.parse(rule_str)
        if match is None:
            return
        return self.rule_setter, match.named, self.rule_alias

    def __repr__(self):
        return self.rule_alias
