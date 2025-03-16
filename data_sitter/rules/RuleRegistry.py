from itertools import chain
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Type

from .Rule import Rule
from ..utils.logger_config import get_logger


if TYPE_CHECKING:
    from field_types.BaseField import BaseField

logger = get_logger(__name__)


class RuleRegistry:
    rules: Dict[str, List[Rule]] = defaultdict(list)
    type_map: Dict[str, Type["BaseField"]] = {}

    @classmethod
    def register_rule(cls, field_rule: str, fixed_params: dict = None):
        def _register(func: callable):
            field_type, func_name = func.__qualname__.split(".")
            logger.debug("Registering function '%s' for %s. Rule: %s", func_name, field_type, field_rule)

            rule = Rule(field_type, field_rule, func, fixed_params)
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
        if field_class.__name__ == "BaseField":
            return cls.rules["BaseField"]
        parent_rules = list(chain.from_iterable(cls.get_rules_for(p) for p in field_class.get_parents()))
        return cls.rules[field_class.__name__] + parent_rules

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


def register_rule(rule: str, fixed_params: dict = None):
    return RuleRegistry.register_rule(rule, fixed_params)


def register_field(field_class: type):
    return RuleRegistry.register_field(field_class)
