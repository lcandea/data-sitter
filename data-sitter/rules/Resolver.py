from collections import defaultdict
import string
import logging
from typing import TYPE_CHECKING, Dict, List, Type
from inspect import signature

from rules import Rule


if TYPE_CHECKING:  # This is only for types
    from field_types.BaseField import BaseField

logger = logging.getLogger(__name__)


class Resolver:
    rules: Dict[str, List[Rule]] = defaultdict(list)
    type_map: Dict[str, Type["BaseField"]] = {}

    @classmethod
    def register_rule(cls, alias: str):
        def _register(func: callable):
            field_type, func_name = func.__qualname__.split(".")
            # if field_type not in cls.rules:
            #     raise TypeNotImplemented(field_type)
            logger.debug("Registering function '%s' for %s. Alias: %s", func_name, field_type, alias)
            validate_alias_function_params(alias, func)

            rule = Rule(alias, func)

            cls.rules[field_type].append(rule)
            logger.debug("Function '%s' Registered", func_name)
            return func

        return _register

    @classmethod
    def register_field(cls, field_class: Type["BaseField"]) -> Type["BaseField"]:
        cls.type_map[field_class.__name__] = field_class
        return field_class

    @classmethod
    def get_type(cls, field_type: str) -> Type["BaseField"]:
        return cls.type_map.get(field_type)

    @classmethod
    def get_rules_for(cls, field_class: Type["BaseField"]):
        return list(cls.rules[field_class.__name__])

    def resolve(self, field_class: Type["BaseField"], rule_str: str) -> Rule:
        type_rules: List[Rule] = self._get_validators_for_type(field_class)
        if type_rules is None:
            raise TypeNotImplemented()

        rules = [rule for validator in type_rules if (rule := validator.match(rule_str)) is not None]
        if not rules:
            raise RuleNotFound(f"Rule '{rule_str}' not in {field_class} or subtypes")
        if len(rules) > 1:
            raise AmbiguousRuleSolution()
        return rules[0]

    def _get_validators_for_type(self, field_class: Type["BaseField"]) -> List[Rule]:
        possible_validators = self.get_rules_for(field_class)
        for parent_field_type in field_class.get_parents():
            possible_validators.extend(self._get_validators_for_type(parent_field_type))
        return possible_validators

    @classmethod
    def get_rules_definition(cls):
        return [
            {
                "field": field_name,
                "parent_field": [p.__name__ for p in field_class.get_parents()],
                "rules": cls.rules.get(field_name, [])
            }
            for field_name, field_class in cls.type_map.items()
        ]


def get_params_from_function(func: callable) -> set:
    sign = signature(func)
    return set(sign.parameters.keys())


def get_params_from_alias(alias: str) -> dict:
    formatter = string.Formatter()
    params = {param: param_type for _, param, param_type, _ in formatter.parse(alias) if param is not None}
    return params


def validate_alias_function_params(alias: str, func: callable):
    alias_params = set(get_params_from_alias(alias))
    func_params = get_params_from_function(func)
    if "self" not in func_params:
        raise NotAClassMethod()
    func_params.remove("self")

    if func_params != alias_params:
        raise AliasFunctionParamsMismatch()


class RuleNotFound(Exception):
    pass


class NotAClassMethod(Exception):
    pass


class AliasFunctionParamsMismatch(Exception):
    pass


class TypeNotImplemented(Exception):
    pass


class AmbiguousRuleSolution(Exception):
    pass


def register_rule(rule: str):
    return Resolver.register_rule(rule)


def register_field(field_class: type):
    return Resolver.register_field(field_class)
