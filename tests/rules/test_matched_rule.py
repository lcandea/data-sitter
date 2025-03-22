import pytest
from unittest.mock import MagicMock, patch
from data_sitter.rules.MatchedRule import MatchedRule, RuleParsedValuesMismatch
from data_sitter.rules.Rule import Rule
from data_sitter.rules.RuleRegistry import RuleRegistry


class TestMatchedRule:
    def test_init(self):
        """Test MatchedRule initialization"""
        # Create source rule
        def dummy_validator(self, param):
            return lambda x: x

        rule = Rule("TestField", "Test rule with {param:Integer}", dummy_validator)

        # Create MatchedRule
        parsed_rule = "Test rule with 42"
        parsed_values = {"param": 42}
        values = {"some_key": "some_value"}

        matched_rule = MatchedRule(rule, parsed_rule, parsed_values, values)

        # Check attributes
        assert matched_rule.field_type == "TestField"
        assert matched_rule.field_rule == "Test rule with {param:Integer}"
        assert matched_rule.parsed_rule == parsed_rule
        assert matched_rule.parsed_values == parsed_values
        assert matched_rule.values == values

    def test_init_validates_parsed_values(self):
        """Test that MatchedRule validates parsed values during initialization"""
        # Create source rule
        def dummy_validator(self, param1, param2):
            return lambda x: x

        rule = Rule("TestField", "Test with {param1:Integer} and {param2:String}", dummy_validator)

        # Create MatchedRule with mismatched parsed values
        parsed_rule = "Test with 42 and 'hello'"
        parsed_values = {"param1": 42}  # Missing param2
        values = {}

        # Initialization should fail due to missing params
        with pytest.raises(RuleParsedValuesMismatch):
            MatchedRule(rule, parsed_rule, parsed_values, values)

    def test_resolved_values_simple(self):
        """Test resolved_values property with simple values"""
        # Create source rule
        def dummy_validator(self, param):
            return lambda x: x

        rule = Rule("TestField", "Test rule with {param:Integer}", dummy_validator)

        # Create MatchedRule
        parsed_rule = "Test rule with 42"
        parsed_values = {"param": 42}
        values = {}

        matched_rule = MatchedRule(rule, parsed_rule, parsed_values, values)

        # Check resolved values
        assert matched_rule.resolved_values == {"param": 42}

    def test_resolved_values_with_references(self):
        """Test resolved_values property with references"""
        # Create source rule
        def dummy_validator(self, param1, param2):
            return lambda x: x

        rule = Rule("TestField", "Test with {param1:Integer} and {param2:String}", dummy_validator)

        # Create MatchedRule with references
        parsed_rule = "Test with 42 and $values.string_value"
        parsed_values = {"param1": 42, "param2": "$values.string_value"}
        values = {"string_value": "resolved_string"}

        matched_rule = MatchedRule(rule, parsed_rule, parsed_values, values)

        # Check resolved values
        assert matched_rule.resolved_values == {"param1": 42, "param2": "resolved_string"}

    @patch.object(RuleRegistry, 'get_type')
    def test_get_validator(self, mock_get_type):
        """Test get_validator method"""
        # Create source rule with a simple validator
        def rule_validator(self, param):
            def validator(value):
                return value + param
            return validator

        rule = Rule("TestField", "Test rule with {param:Integer}", rule_validator)

        # Create MatchedRule
        parsed_rule = "Test rule with 42"
        parsed_values = {"param": 42}
        values = {}

        matched_rule = MatchedRule(rule, parsed_rule, parsed_values, values)

        # Create field instance mock
        field_instance = MagicMock()

        # Create a test class instead of a mock for instancecheck to work
        class TestFieldClass:
            pass

        # Return the class and configure the mock field instance
        mock_get_type.return_value = TestFieldClass
        field_instance.__class__ = TestFieldClass

        # Get validator
        validator = matched_rule.get_validator(field_instance)

        # Verify get_type was called
        mock_get_type.assert_called_once_with("TestField")

        # Test the returned validator
        result = validator(10)
        assert result == 52  # 10 + 42

    @patch.object(RuleRegistry, 'get_type')
    def test_get_validator_type_mismatch(self, mock_get_type):
        """Test get_validator method when field instance type doesn't match"""
        # Create source rule
        def dummy_validator(self, param):
            return lambda x: x

        rule = Rule("TestField", "Test rule with {param:Integer}", dummy_validator)

        # Create MatchedRule
        matched_rule = MatchedRule(
            rule, "Test rule with 42", {"param": 42}, {}
        )

        # Create classes for type checking
        class ExpectedClass:
            pass

        class ActualClass:
            pass

        # Configure for type mismatch
        field_instance = ActualClass()
        mock_get_type.return_value = ExpectedClass

        # Should raise TypeError
        with pytest.raises(TypeError, match="Cannot add rule to"):
            matched_rule.get_validator(field_instance)

    def test_get_front_end_repr(self):
        """Test get_front_end_repr method"""
        # Create source rule
        def dummy_validator(self, param):
            return lambda x: x

        rule = Rule("TestField", "Test rule with {param:Integer}", dummy_validator)

        # Create MatchedRule
        parsed_rule = "Test rule with 42"
        parsed_values = {"param": 42}

        matched_rule = MatchedRule(rule, parsed_rule, parsed_values, {})

        # Get frontend representation
        result = matched_rule.get_front_end_repr()

        # Check returned dictionary
        assert result == {
            "rule": "Test rule with {param:Integer}",
            "parsed_rule": "Test rule with 42",
            "rule_params": {"param": "Integer"},
            "parsed_values": {"param": 42}
        }
