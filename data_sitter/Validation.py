from collections import defaultdict
from typing import Any, Dict, List, Type

from pydantic import BaseModel, ValidationError


class Validation():
    item: Dict[str, Any]
    errors: Dict[str, List[str]]
    unknowns: Dict[str, Any]

    def __init__(self, item: dict, errors: dict = None, unknowns: dict = None):
        self.item = item
        self.errors = errors if errors else None
        self.unknowns = unknowns if unknowns else None

    def to_dict(self) -> dict:
        return {key: value for key in ["item", "errors", "unknowns"] if (value := getattr(self, key))}

    @classmethod
    def validate(cls, PydanticModel: Type[BaseModel], input_item: dict) -> "Validation":
        model_keys = PydanticModel.model_json_schema()['properties'].keys()
        item = {key: None for key in model_keys}  # Filling not present values with Nones
        errors = defaultdict(list)
        unknowns = {}
        for key, value in input_item.items():
            if key in item:
                item[key] = value
            else:
                unknowns[key] = value
        try:
            validated = PydanticModel(**item).model_dump()
        except ValidationError as e:
            validated = item
            for error in e.errors():
                field = error['loc'][0]  # Extract the field name
                msg = error['msg']
                errors[field].append(msg)
        return Validation(item=validated, errors=dict(errors), unknowns=unknowns)
