# Data-Sitter

![Coverage](./coverage.svg)

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

## Development and Deployment

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. **Pull Request Checks**
   - Automatically checks if the version has been bumped in `pyproject.toml`
   - Fails if the version is the same as in the main branch
   - Ensures every PR includes a version update

2. **Automatic Releases**
   - When code is merged to the main branch:
     - Builds the package
     - Publishes to PyPI automatically
   - Uses PyPI API token for secure authentication

To set up the CI/CD pipeline:

1. Create a PyPI API token:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Create a new API token with "Upload" scope
   - Copy the token

2. Add the token to GitHub:
   - Go to your repository's Settings > Secrets and variables > Actions
   - Create a new secret named `PYPI_API_TOKEN`
   - Paste your PyPI API token

### Setting Up Development Environment

To set up a development environment with all the necessary tools, install the package with development dependencies:

```sh
pip install -e ".[dev]"
```

This will install:
- The package in editable mode
- Testing tools (pytest, pytest-cov, pytest-mock)
- Build tools (build, twine)

### Building the Package

To build the package, run:

```sh
python -m build
```

This will create a `dist` directory containing both a source distribution (`.tar.gz`) and a wheel (`.whl`).

### Deploying to PyPI

To upload to PyPI:

```sh
twine upload dist/*
```

You'll be prompted for your PyPI username and password. For security, it's recommended to use an API token instead of your password.

## Usage

### Creating a Pydantic Model from a Contract

To convert a data contract into a Pydantic model, follow these steps:

```python
from data_sitter import Contract

contract_dict = {
    "name": "test",
    "fields": [
        {
            "name": "FID",
            "type": "Integer",
            "rules": ["Positive"]
        },
        {
            "name": "SECCLASS",
            "type": "String",
            "rules": [
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
            "name": "CATEGORY",
            "type": "String",
            "rules": ["Value In $values.categories"]
        },
        {
            "name": "NAME",
            "type": "String",
            "rules": [
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

#### Base

- Is not null

#### String - (Inherits from `Base`)

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

#### Numeric - (Inherits from `Base`)

- Is not zero
- Is positive
- Is negative
- Is at least {min_val:Number}
- Is at most {max_val:Number}
- Is greater than {threshold:Number}
- Is less than {threshold:Number}
- Is not between {min_val:Number} and {max_val:Number}
- Is between {min_val:Number} and {max_val:Number}

#### Integer  - (Inherits from `Numeric`)

#### Float  - (Inherits from `Numeric`)

- Has at most {decimal_places:Integer} decimal places

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests in the [GitHub repository](https://github.com/lcandea/data-sitter).

## License

Data-Sitter is licensed under the MIT License.
