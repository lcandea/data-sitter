# Data-Sitter

## Overview

Data-Sitter is a Python library designed to simplify data validation by converting data contracts into Pydantic models. This allows for easy and efficient validation of structured data, ensuring compliance with predefined rules and constraints.

## Features

- Define structured data contracts in JSON format.
- Generate Pydantic models automatically from contracts.
- Enforce validation rules at the field level.
- Support for rule references within the contract.

## Installation

```sh
pip install data-sitter
```

## Usage

### Creating a Pydantic Model from a Contract

To convert a data contract into a Pydantic model, follow these steps:

```python
from data_sitter import Contract

contract_dict = {
    "name": "test",
    "fields": [
        {
            "field_name": "FID",
            "field_type": "IntegerField",
            "field_rules": ["Positive"]
        },
        {
            "field_name": "SECCLASS",
            "field_type": "StringField",
            "field_rules": [
                "Validate Not Null",
                "Value In ['UNCLASSIFIED', 'CLASSIFIED']",
            ]
        }
    ],
}

contract = Contract.from_dict(contract_dict)
pydantic_contract = contract.pydantic_model
```

### Using Rule References

Data-Sitter allows you to define reusable values in the `values` key and reference them in field rules using `$values.[key]`. For example:

```json
{
    "name": "example_contract",
    "fields": [
        {
            "field_name": "CATEGORY",
            "field_type": "StringField",
            "field_rules": ["Value In $values.categories"]
        },
        {
            "field_name": "NAME",
            "field_type": "StringField",
            "field_rules": [
                "Length Between $values.min_length and $values.max_length"
            ]
        }

    ],
    "values": {"categories": ["A", "B", "C"], "min_length": 5,"max_length": 50}
}
```

## Available Rules

The available validation rules can be retrieved programmatically:

```python
from data_sitter import RuleRegistry

rules = RuleRegistry.get_rules_definition()
print(rules)
```

### Rule Definitions

Below are the available rules grouped by field type:

#### BaseField

- Is not null

#### StringField - (Inherits from `BaseField`)

- Is not empty
- Starts with {prefix:String}
- Ends with {suffix:String}
- Is not one of {possible_values:Strings}
- Is one of {possible_values:Strings}
- Has length between {min_val:Integer} and {max_val:Integer}
- Has maximum length {max_len:Integer}
- Has minimum length {min_len:Integer}
- Is uppercase
- Is lowercase
- Matches regex {pattern:String}
- Is valid email
- Is valid URL
- Has no digits

#### NumericField - (Inherits from `BaseField`)

- Is not zero
- Is positive
- Is negative
- Is at least {min_val:Number}
- Is at most {max_val:Number}
- Is greater than {threshold:Number}
- Is less than {threshold:Number}
- Is not between {min_val:Number} and {max_val:Number}
- Is between {min_val:Number} and {max_val:Number}

#### IntegerField  - (Inherits from `NumericField`)

#### FloatField  - (Inherits from `NumericField`)

- Has at most {decimal_places:Integer} decimal places

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests in the [GitHub repository](https://github.com/lcandea/data-sitter).

## License

Data-Sitter is licensed under the MIT License.
