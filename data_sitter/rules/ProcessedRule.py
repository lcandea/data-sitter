from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Union

from .Rule import Rule
from .Enums import LogicalOperator

if TYPE_CHECKING:
    from ..field_types import BaseField

MatchedParsedRule = str
LogicalParsedRule = Dict[LogicalOperator, List["ParsedRule"]]
ParsedRule = Union[MatchedParsedRule, LogicalParsedRule]


class ProcessedRule(Rule, ABC):
    parsed_rule: ParsedRule

    @abstractmethod
    def get_validator(self, field_instance: "BaseField"):
        raise NotImplementedError()

    @abstractmethod
    def get_front_end_repr(self) -> dict:
        raise NotImplementedError()
