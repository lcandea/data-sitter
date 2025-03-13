import json
import logging

from utils.logger_config import configure_logging
from Contract import Contract

configure_logging()
logger = logging.getLogger(__name__)


def prettyp(dictio):
    print(json.dumps(dictio, indent=4, default=str))


contract_example = {
    "name": "test",
    "fields": [
        {
            "field_name": "FID",
            "field_type": "IntegerField",
            "field_rules": [
                "Positive",
            ],
        },
        {
            "field_name": "ID",
            "field_type": "IntegerField",
            "field_rules": [
                "Positive",
            ],
        },
        {
            "field_name": "SECCLASS",
            "field_type": "StringField",
            "field_rules": [
                "Validate Not Null",
                "Value In ['UNCLASSIFIED', 'CLASSIFIED']",
                "Value In $values.classes",
                "Starts with 'UN'",
            ],
        },
        {
            "field_name": "NAME",
            "field_type": "StringField",
            "field_rules": [
                "Length Between $values.min_length and $values.max_length",
            ],
        },
    ],
    "values": {"classes": ["UNCLASSIFIED"], "min_length": 5,"max_length": 50},
}

item_example = {
    "FID": "1001",
    "ID": "11699187",
    "SECCLASS": "UNCLASSIFIED",
    "NAME": "MOWRY MEDICAL PHARMACY",
}

contract_validator = Contract.from_dict(contract_example)
validated_item = contract_validator.model_validate(item_example)
prettyp(validated_item)

# prettyp(contract_validator.get_front_end_contract())

# prettyp(RuleRegistry.get_rules_definition())
