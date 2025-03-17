import csv
import json
import argparse
from pathlib import Path

from .Contract import Contract


DEFAULT_ENCODING = "utf8"

def main():
    parser = argparse.ArgumentParser(description='Data Sitter CLI')
    parser.add_argument('-c', '--contract', required=True, help='Path to contract file')
    parser.add_argument('-f', '--file', required=True, help='Path to data file')
    parser.add_argument('-e', '--encoding', help='Files Encoding', default=DEFAULT_ENCODING)

    args = parser.parse_args()
    # Add your logic here using args.contract and args.file
    print(f"Processing {args.file} with contract {args.contract}")

    file_path = Path(args.file)
    encoding = args.encoding
    contract_path = Path(args.contract)
    contract_dict = json.loads(contract_path.read_text(encoding))
    contract = Contract.from_dict(contract_dict)
    pydantic_contract = contract.pydantic_model

    if file_path.suffix == '.csv':
        with open(file_path, encoding=encoding) as f:
            reader = csv.DictReader(f)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            records = [{k: v.strip() for k, v in row.items()} for row in reader]

    elif file_path.suffix == '.json':
        file_data = json.loads(file_path.read_text(encoding))
        if isinstance(file_data, dict):
            records = [file_data]
        else:
            records = file_data
    else:
        raise NotImplementedError(f"Type {file_path.suffix} not implemented.")

    _ = [pydantic_contract.model_validate(row) for row in records]
    print(f"The file {args.file} pass the contract {args.contract}")


if __name__ == '__main__':
    main()
