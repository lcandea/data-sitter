from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Union

from .Rule import Rule
from .Enums import LogicalOperator

if TYPE_CHECKING:
    from ..field_types import BaseField


class ProcessedRule(Rule, ABC):
    parsed_rule: Union[str, Dict[LogicalOperator, List["ProcessedRule"]]]

    @abstractmethod
    def get_validators(self, field_instance: "BaseField"):
        raise NotImplementedError()

    @abstractmethod
    def get_front_end_repr(self) -> dict:
        raise NotImplementedError()
