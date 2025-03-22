import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import argparse

from data_sitter.cli import main


@pytest.fixture
def sample_contract_dict():
    return {
        "name": "TestContract",
        "fields": [
            {
                "field_name": "name",
                "field_type": "StringField",
                "field_rules": [
                    "Is not null",
                    "Has minimum length 3"
                ]
            },
            {
                "field_name": "age",
                "field_type": "IntegerField",
                "field_rules": [
                    "Is not null",
                    "Is at least 18"
                ]
            }
        ]
    }


@pytest.fixture
def sample_csv_file(tmp_path):
    content = "name,age\nJohn Doe,25\nJane Smith,30\n"
    file_path = tmp_path / "data.csv"
    file_path.write_text(content)
    return str(file_path)


@pytest.fixture
def sample_json_file(tmp_path, sample_contract_dict):
    data = [
        {"name": "John Doe", "age": 25},
        {"name": "Jane Smith", "age": 30}
    ]
    file_path = tmp_path / "data.json"
    file_path.write_text(json.dumps(data))
    return str(file_path)


@pytest.fixture
def sample_single_object_json_file(tmp_path, sample_contract_dict):
    # Single object instead of an array
    data = {"name": "John Doe", "age": 25}
    file_path = tmp_path / "single_object.json"
    file_path.write_text(json.dumps(data))
    return str(file_path)


@pytest.fixture
def sample_contract_file(tmp_path, sample_contract_dict):
    file_path = tmp_path / "contract.json"
    file_path.write_text(json.dumps(sample_contract_dict))
    return str(file_path)


class TestCLI:
    @patch('sys.argv')
    @patch('builtins.print')
    def test_cli_with_csv_file(self, mock_print, mock_argv, sample_contract_file, sample_csv_file):
        """Test CLI with CSV file"""
        mock_argv.__getitem__.side_effect = lambda i: [
            "data-sitter", 
            "-c", sample_contract_file, 
            "-f", sample_csv_file
        ][i]
        
        main()
        
        # Check that the success message was printed
        assert any("pass the contract" in args[0] for args, _ in mock_print.call_args_list)

    @patch('sys.argv')
    @patch('builtins.print')
    def test_cli_with_json_file(self, mock_print, mock_argv, sample_contract_file, sample_json_file):
        """Test CLI with JSON file"""
        mock_argv.__getitem__.side_effect = lambda i: [
            "data-sitter", 
            "-c", sample_contract_file, 
            "-f", sample_json_file
        ][i]
        
        main()
        
        # Check that the success message was printed
        assert any("pass the contract" in args[0] for args, _ in mock_print.call_args_list)

    @patch('sys.argv')
    @patch('builtins.print')
    def test_cli_with_single_object_json_file(self, mock_print, mock_argv, sample_contract_file, sample_single_object_json_file):
        """Test CLI with JSON file containing a single object"""
        mock_argv.__getitem__.side_effect = lambda i: [
            "data-sitter", 
            "-c", sample_contract_file, 
            "-f", sample_single_object_json_file
        ][i]
        
        main()
        
        # Check that the success message was printed
        assert any("pass the contract" in args[0] for args, _ in mock_print.call_args_list)

    @patch('sys.argv')
    @patch('builtins.print')
    def test_cli_with_custom_encoding(self, mock_print, mock_argv, sample_contract_file, sample_csv_file):
        """Test CLI with custom encoding"""
        mock_argv.__getitem__.side_effect = lambda i: [
            "data-sitter", 
            "-c", sample_contract_file, 
            "-f", sample_csv_file,
            "-e", "utf-8"
        ][i]
        
        main()
        
        # Check that the success message was printed
        assert any("pass the contract" in args[0] for args, _ in mock_print.call_args_list)

    @patch('sys.argv')
    @patch('data_sitter.Contract.Contract.from_dict')
    @patch('builtins.print')
    def test_contract_validation_error(self, mock_print, mock_from_dict, mock_argv, sample_contract_file, sample_csv_file):
        """Test CLI when contract validation fails"""
        # Create a mock contract with a pydantic model that will raise an exception
        mock_pydantic_model = MagicMock()
        mock_pydantic_model.model_validate.side_effect = Exception("Validation error")
        
        mock_contract = MagicMock()
        mock_contract.pydantic_model = mock_pydantic_model
        mock_from_dict.return_value = mock_contract
        
        mock_argv.__getitem__.side_effect = lambda i: [
            "data-sitter", 
            "-c", sample_contract_file, 
            "-f", sample_csv_file
        ][i]
        
        with pytest.raises(Exception):  # We expect an exception to be raised
            main()

    @patch('sys.argv')
    def test_unsupported_file_type(self, mock_argv, sample_contract_file, tmp_path):
        """Test CLI with unsupported file type"""
        # Create a file with unsupported extension
        unsupported_file = tmp_path / "data.txt"
        unsupported_file.write_text("some data")
        
        mock_argv.__getitem__.side_effect = lambda i: [
            "data-sitter", 
            "-c", sample_contract_file, 
            "-f", str(unsupported_file)
        ][i]
        
        with pytest.raises(NotImplementedError):
            main()
            
    @patch('sys.argv')
    @patch('argparse.ArgumentParser.parse_args')
    def test_missing_required_arguments(self, mock_parse_args, mock_argv):
        """Test CLI with missing required arguments"""
        # Make the argument parser raise an error
        mock_parse_args.side_effect = argparse.ArgumentError(None, "argument -c/--contract is required")
        
        with pytest.raises(argparse.ArgumentError):
            main() 