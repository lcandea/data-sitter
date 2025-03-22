import pytest
from parse import Parser

from data_sitter.rules.Parser.RuleParser import RuleParser
from data_sitter.rules.Parser.alias_parameters_parser import NotCompatibleTypes
from data_sitter.rules.Rule import Rule
from data_sitter.rules.MatchedRule import MatchedRule


class TestRuleParser:
    def test_init(self):
        """Test RuleParser initialization"""
        values = {"key1": "value1", "key2": 123}
        parser = RuleParser(values)

        assert parser.values == values
        assert isinstance(parser.parsers, dict)
        assert isinstance(parser.aliases, dict)

        # Check that basic alias types are registered
        for alias_type in ["Integer", "Float", "Number", "String"]:
            assert alias_type in parser.aliases

    def test_get_parser_for_rule(self):
        """Test get_parser_for_rule method"""
        parser = RuleParser({})

        # Create a real rule
        def dummy_validator(self, param):
            pass
        rule = Rule("TestField", "Test rule with {param:Integer}", dummy_validator)

        # Get parser for the rule
        result_parser = parser.get_parser_for_rule(rule)

        # Verify the parser is created correctly
        assert isinstance(result_parser, Parser)
        assert rule.field_rule in parser.parsers

        # Getting the same parser again should return the cached instance
        assert parser.get_parser_for_rule(rule) is result_parser

    def test_match_valid_rule(self):
        """Test match method with a valid rule"""
        values = {"existing_key": 123}
        parser = RuleParser(values)

        # Create a real rule with an integer parameter
        def dummy_validator(self, value):
            pass
        rule = Rule("TestField", "Value is {value:Integer}", dummy_validator)

        # Create a matching rule string
        parsed_rule = "Value is 42"

        # Match the rule
        result = parser.match(rule, parsed_rule)

        # Verify the result
        assert isinstance(result, MatchedRule)
        assert result.parsed_rule == parsed_rule
        assert result.parsed_values == {"value": 42}
        assert result.values == values

    def test_match_invalid_rule(self):
        """Test match method with an invalid rule"""
        parser = RuleParser({})

        # Create a real rule with an integer parameter
        def dummy_validator(self, value):
            pass
        rule = Rule("TestField", "Value is {value:Integer}", dummy_validator)

        # Create a non-matching rule string
        parsed_rule = "Value is not an integer"

        # Match should return None for non-matching rules
        result = parser.match(rule, parsed_rule)
        assert result is None

    def test_parse_reference_of_valid(self):
        """Test parse_reference_of with valid reference"""
        values = {"numeric_key": 42}
        parser = RuleParser(values)

        # Create a reference parser for integers
        int_ref_parser = parser.parse_reference_of("Integer", parser.aliases["Integer"])

        # Valid reference
        ref_text = "$values.numeric_key"
        result = int_ref_parser(ref_text)

        # Should return the reference text unchanged
        assert result == ref_text

    def test_parse_reference_of_invalid(self):
        """Test parse_reference_of with invalid reference"""
        values = {"string_key": "not_a_number"}
        parser = RuleParser(values)

        # Create a reference parser for integers
        int_ref_parser = parser.parse_reference_of("Integer", parser.aliases["Integer"])

        # Valid reference syntax but incompatible type
        ref_text = "$values.string_key"

        # Should raise NotCompatibleTypes
        with pytest.raises(NotCompatibleTypes):
            int_ref_parser(ref_text)

    def test_get_aliases_with_reference_support(self):
        """Test get_aliases_with_reference_support method"""
        parser = RuleParser({})
        aliases = parser.get_aliases_with_reference_support()

        # Check that all basic types are present
        for alias_type in ["Integer", "Float", "Number", "String"]:
            assert alias_type in aliases

        # Check that array types are present
        for array_type in ["Integers", "Floats", "Numbers", "Strings"]:
            assert array_type in aliases
