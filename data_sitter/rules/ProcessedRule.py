from abc import ABC
from typing import TYPE_CHECKING, Dict, List

from .Rule import Rule
from .Enums import LogicalOperator

if TYPE_CHECKING:
    from field_types import BaseField


class ProcessedRule(Rule, ABC):
    parsed_rule: str | Dict[LogicalOperator, List["ProcessedRule"]]

    def add_to_instance(self, field_instance: "BaseField"):
        raise NotImplementedError()

    def get_front_end_repr(self):
        raise NotImplementedError()
