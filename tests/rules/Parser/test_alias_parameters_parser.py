import pytest
from data_sitter.rules.Parser.alias_parameters_parser import (
    parse_int,
    parse_float,
    parse_number,
    parse_string,
    parse_array_of,
    NotCompatibleTypes,
    alias_parameters_types
)


class TestAliasParametersParser:
    def test_parse_int(self):
        """Test the parse_int function"""
        assert parse_int("123") == 123
        assert parse_int("-456") == -456
        assert parse_int("0") == 0

    def test_parse_float(self):
        """Test the parse_float function"""
        assert parse_float("123.45") == 123.45
        assert parse_float("-67.89") == -67.89
        assert parse_float(".0") == 0.0

    def test_parse_number(self):
        """Test the parse_number function"""
        # Integer values
        assert parse_number("123") == 123
        assert parse_number("-456") == -456
        assert isinstance(parse_number("123"), int)

        # Float values
        assert parse_number("123.45") == 123.45
        assert parse_number("-67.89") == -67.89
        assert isinstance(parse_number("123.45"), float)

    def test_parse_string(self):
        """Test the parse_string function"""
        assert parse_string('"hello world"') == "hello world"
        assert parse_string("'hello world'") == "hello world"

        # Empty string
        assert parse_string('""') == ""
        assert parse_string("''") == ""

        # Special characters
        assert parse_string('"hello, world!"') == "hello, world!"
        assert parse_string('"123"') == "123"

    def test_parse_array_of_integers(self):
        """Test the parse_array_of function with integers"""
        # Use the actual parse_array_of function from the module
        parse_int_array = parse_array_of("Integer", parse_int)

        assert parse_int_array("[]") == []
        assert parse_int_array("[123]") == [123]
        assert parse_int_array("[123,456,789]") == [123, 456, 789]
        assert parse_int_array("[123,-456,0]") == [123, -456, 0]

    def test_parse_array_of_strings(self):
        """Test the parse_array_of function with strings"""
        # Use the actual parse_array_of function from the module
        parse_string_array = parse_array_of("String", parse_string)

        assert parse_string_array("[]") == []
        assert parse_string_array('["hello"]') == ["hello"]
        assert parse_string_array('["hello","world"]') == ["hello", "world"]
        assert parse_string_array("['hello','world']") == ["hello", "world"]
        assert parse_string_array('["hello",\'world\']') == ["hello", "world"]

    def test_parse_array_incompatible_types(self):
        """Test the parse_array_of function with incompatible types"""
        parse_int_array = parse_array_of("Integer", parse_int)

        # String in an integer array
        with pytest.raises(NotCompatibleTypes):
            parse_int_array('[123,"hello",456]')

    def test_alias_parameters_types_dict(self):
        """Test that alias_parameters_types contains all expected types"""
        expected_types = [
            "Integer", "Integers",
            "Float", "Floats",
            "Number", "Numbers",
            "String", "Strings"
        ]

        for type_name in expected_types:
            assert type_name in alias_parameters_types
