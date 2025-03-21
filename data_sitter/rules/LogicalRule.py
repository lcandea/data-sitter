from typing import TYPE_CHECKING, Callable, List

from .Enums import LogicalOperator
from .ProcessedRule import ProcessedRule, LogicalParsedRule

if TYPE_CHECKING:
    from ..field_types import BaseField


def and_or_validator(validators: List[Callable], operator: LogicalOperator) -> Callable:
    def validator(value):
        exceptions = []
        for validator_ in validators:
            try:
                validator_(value)
                exceptions.append(None)  # No error, validation passed
            except Exception as e:
                exceptions.append(str(e))  # Store error message

        if operator == LogicalOperator.OR and all(exceptions):
            raise ValueError(f"None of the conditions were met. Errors: {exceptions}")
        if operator == LogicalOperator.AND and any(exceptions):
            exceptions = list(filter(None, exceptions))
            raise ValueError(f"Not all conditions were met. Errors: {exceptions}")
        return value
    return validator


def not_validator(validator_: Callable):
    def validator(value):
        try:
            validator_(value)
        except Exception:
            return value  # Validation passes if the condition fails
        else:
            raise ValueError("Condition was met, but expected NOT to be met.")
    return validator



class LogicalRule(ProcessedRule):
    operator: LogicalOperator
    processed_rules: List[ProcessedRule]

    def __init__(self, operator: LogicalOperator, processed_rules: List[ProcessedRule]):
        if operator not in LogicalOperator:
            raise TypeError(f'Logical Operator not recognised: {operator}')
        if not processed_rules:
            raise ValueError("Logical rules must have at least one rule.")
        if operator == LogicalOperator.NOT and len(processed_rules) != 1:
            raise TypeError(f'Not Operator can only contain one rule. Cotains: {len(processed_rules)}')
        self.operator = operator
        self.processed_rules = processed_rules

    @property
    def parsed_rule(self) -> LogicalParsedRule:
        return {self.operator: [pr.parsed_rule for pr in self.processed_rules]}

    def get_validator(self, field_instance: "BaseField") -> Callable:
        if self.operator in (LogicalOperator.OR, LogicalOperator.AND):
            return and_or_validator([pr.get_validator(field_instance) for pr in self.processed_rules], self.operator)
        elif self.operator == LogicalOperator.NOT:
            return not_validator(self.processed_rules[0].get_validator(field_instance))
        else:
            raise TypeError(f'Logical Operator not recognised: {self.operator}')

    def get_front_end_repr(self) -> dict:
        return {self.operator: [pr.get_front_end_repr() for pr in self.processed_rules]}
