from itertools import chain
from typing import TYPE_CHECKING, Callable, Dict, List, NamedTuple, Type


from .Rule import Rule
from ..utils.logger_config import get_logger
from ..field_types.FieldTypes import FieldTypes


if TYPE_CHECKING:  # pragma: no cover
    from field_types.BaseField import BaseField

logger = get_logger(__name__)


class RuleMetadata(NamedTuple):
    rule: str
    fixed_params: dict


class RuleRegistry:
    rules: Dict[str, List[Rule]] = {}
    type_map: Dict[str, Type["BaseField"]] = {}

    @classmethod
    def register_field(cls, field_class: Type["BaseField"]) -> Type["BaseField"]:
        field_type_name = field_class.type_name
        cls.type_map[field_class.type_name] = field_class
        cls.rules[field_class.type_name] = []

        for method in field_class.__dict__.values():
            metadata: RuleMetadata = getattr(method, "_rule_metadata", None)
            if metadata is None:
                continue
            rule = Rule(
                field_type=field_type_name,
                field_rule=metadata.rule,
                rule_setter=method,
                fixed_params=metadata.fixed_params
            )
            cls.add_rule(field_class, rule)
        return field_class

    @classmethod
    def add_rule(cls, field_class: Type["BaseField"], rule: Rule):
        if field_class.type_name not in cls.rules:
            raise ValueError(f"Field not registered: {field_class.type_name}")
        cls.rules[field_class.type_name].append(rule)

    @classmethod
    def get_type(cls, type_name: str) -> Type["BaseField"]:
        return cls.type_map.get(type_name)

    @classmethod
    def get_rules_for(cls, field_class: Type["BaseField"]):
        if field_class.type_name == FieldTypes.BASE:
            return cls.rules[FieldTypes.BASE]
        parent_rules = list(chain.from_iterable(cls.get_rules_for(p) for p in field_class.get_parents()))
        return cls.rules[field_class.type_name] + parent_rules

    @classmethod
    def get_rules_definition(cls):
        return [
            {
                "field": name,
                "parent_field": [p.type_name for p in field_class.get_parents()],
                "rules": cls.rules.get(name, [])
            }
            for name, field_class in cls.type_map.items()
        ]


def register_rule(rule: str, fixed_params: dict = None):
    def _register(func: Callable):
        setattr(func, "_rule_metadata",
            RuleMetadata(
                rule=rule,
                fixed_params=fixed_params or {}
            )
        )
        return func
    return _register


def register_field(field_class: type):
    return RuleRegistry.register_field(field_class)
