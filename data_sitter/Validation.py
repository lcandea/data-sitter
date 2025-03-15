
from collections import defaultdict
from typing import Any, Dict, List, Type

from pydantic import BaseModel, ValidationError


class Validation():
    row: Dict[str, Any]
    errors: Dict[str, List[str]]

    def __init__(self, row: dict, errors: dict = None):
        self.row = row
        self.errors = errors or {}

    def to_dict(self) -> dict:
        return {"row": self.row, "errors": self.errors}
    
    @classmethod
    def validate(cls, model: Type[BaseModel], item: dict) -> "Validation":
        try:
            row = model(**item)  # Validate the row
            return Validation(row=row.model_dump())
        except ValidationError as e:
            errors = defaultdict(list)
            for error in e.errors():
                field = error['loc'][0]  # Extract the field name
                msg = error['msg']
                errors[field].append(msg)
            return Validation(row=item, errors=dict(errors))
