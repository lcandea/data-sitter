import string
from inspect import signature
from typing import Callable


class NotAClassMethod(Exception):
    pass


class RuleFunctionParamsMismatch(Exception):
    pass


class Rule:
    field_type: str
    field_rule: str
    rule_setter: Callable

    def __init__(self, field_type: str, field_rule: str, rule_setter: Callable) -> None:
        self.field_type = field_type
        self.field_rule = field_rule
        self.rule_setter = rule_setter
        self.__validate_rule_function_params()

    def __repr__(self):
        return self.field_rule

    @property
    def rule_params(self) -> dict:
        params = string.Formatter().parse(self.field_rule)
        return {param: param_type for _, param, param_type, _ in params if param is not None}

    def __get_rule_setter_params(self) -> set:
        rule_setter_sign = signature(self.rule_setter)
        return set(rule_setter_sign.parameters.keys())

    def __validate_rule_function_params(self):
        rule_setter_params = self.__get_rule_setter_params()
        if "self" not in rule_setter_params:
            raise NotAClassMethod()

        rule_setter_params.remove("self")
        if set(self.rule_params) != rule_setter_params:
            raise RuleFunctionParamsMismatch(f"Rule Params: {self.rule_params}, Setter Params: {rule_setter_params}")
