# Data-Sitter

## Overview

Data-Sitter is a Python library designed to simplify data validation by converting data contracts into Pydantic models. This allows for easy and efficient validation of structured data, ensuring compliance with predefined rules and constraints.

## Features

- Define structured data contracts in JSON format.
- Generate Pydantic models automatically from contracts.
- Enforce validation rules at the field level.
- Support for rule references within the contract.

## Installation

You can install Data-Sitter directly from GitHub:

```sh
pip install git+https://github.com/Kenr0t/data-sitter.git@main
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
pydantic_contract = contract.get_pydantic_model()
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

- Validate Not Null

#### StringField - (Inherits from `BaseField`)

- Is not empty
- Starts with `{prefix:String}`
- Ends with `{sufix:String}`
- Value in `{possible_values:Strings}`
- Length between `{min_val:Integer}` and `{max_val:Integer}`
- Maximum length of `{max_len:Integer}`
- Length shorter than `{max_len:Integer}`
- Minimum length of `{min_len:Integer}`
- Length longer than `{min_len:Integer}`
- Is uppercase

#### NumericField - (Inherits from `BaseField`)

- Not Zero
- Positive
- Negative
- Minimum `{min_val:Number}`
- Maximum `{max_val:Number}`
- Greater than `{threshold:Number}`
- Less than `{threshold:Number}`
- Between `{min_val:Number}` and `{max_val:Number}`

#### IntegerField  - (Inherits from `NumericField`)

#### FloatField  - (Inherits from `NumericField`)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests in the [GitHub repository](https://github.com/Kenr0t/data-sitter).

## License

Data-Sitter is licensed under the MIT License.
