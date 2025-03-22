import pytest
from unittest.mock import MagicMock, patch
from data_sitter.rules.LogicalRule import LogicalRule, and_or_validator, not_validator
from data_sitter.rules.Enums import LogicalOperator
from data_sitter.rules.ProcessedRule import ProcessedRule


class TestAndOrValidator:
    def test_and_validator(self):
        """Test and_or_validator with AND operator"""
        # Create validators - one passes, one fails
        def validator1(value):
            return value  # Always passes

        def validator2(value):
            if value < 10:
                raise ValueError("Value must be at least 10")
            return value

        # Combine with AND
        combined = and_or_validator([validator1, validator2], LogicalOperator.AND)

        # Value passes both validators
        assert combined(10) == 10

        # Value fails one validator
        with pytest.raises(ValueError, match="Not all conditions were met"):
            combined(5)

    def test_or_validator(self):
        """Test and_or_validator with OR operator"""
        # Create validators - both may fail
        def validator1(value):
            if value < 10:
                raise ValueError("Value must be at least 10")
            return value

        def validator2(value):
            if value % 2 != 0:
                raise ValueError("Value must be even")
            return value

        # Combine with OR
        combined = and_or_validator([validator1, validator2], LogicalOperator.OR)

        # Value passes first validator only
        assert combined(11) == 11

        # Value passes second validator only
        assert combined(8) == 8

        # Value passes both validators
        assert combined(10) == 10

        # Value fails both validators
        with pytest.raises(ValueError, match="None of the conditions were met"):
            combined(5)


class TestNotValidator:
    def test_not_validator(self):
        """Test not_validator function"""
        # Create a validator
        def validator(value):
            if value < 10:
                raise ValueError("Value must be at least 10")
            return value

        # Create NOT validator
        not_val = not_validator(validator)

        # Value fails original validator, so passes NOT validator
        assert not_val(5) == 5

        # Value passes original validator, so fails NOT validator
        with pytest.raises(ValueError, match="Condition was met, but expected NOT to be met"):
            not_val(10)


class TestLogicalRule:
    def test_init_with_and_operator(self):
        """Test LogicalRule initialization with AND operator"""
        # Create processed rules
        rule1 = MagicMock(spec=ProcessedRule)
        rule2 = MagicMock(spec=ProcessedRule)

        # Create logical rule
        logical_rule = LogicalRule(LogicalOperator.AND, [rule1, rule2])

        # Check properties
        assert logical_rule.operator == LogicalOperator.AND
        assert logical_rule.processed_rules == [rule1, rule2]

    def test_init_with_or_operator(self):
        """Test LogicalRule initialization with OR operator"""
        # Create processed rules
        rule1 = MagicMock(spec=ProcessedRule)
        rule2 = MagicMock(spec=ProcessedRule)

        # Create logical rule
        logical_rule = LogicalRule(LogicalOperator.OR, [rule1, rule2])

        # Check properties
        assert logical_rule.operator == LogicalOperator.OR
        assert logical_rule.processed_rules == [rule1, rule2]

    def test_init_with_not_operator(self):
        """Test LogicalRule initialization with NOT operator"""
        # Create processed rule
        rule = MagicMock(spec=ProcessedRule)

        # Create logical rule
        logical_rule = LogicalRule(LogicalOperator.NOT, [rule])

        # Check properties
        assert logical_rule.operator == LogicalOperator.NOT
        assert logical_rule.processed_rules == [rule]

    def test_init_with_invalid_operator(self):
        """Test LogicalRule initialization with an invalid operator"""
        rule = MagicMock(spec=ProcessedRule)

        with pytest.raises(TypeError, match="Logical Operator not recognised"):
            LogicalRule("INVALID", [rule])

    def test_init_with_empty_rules(self):
        """Test LogicalRule initialization with empty rules list"""
        with pytest.raises(ValueError, match="Logical rules must have at least one rule"):
            LogicalRule(LogicalOperator.AND, [])

    def test_init_not_with_multiple_rules(self):
        """Test LogicalRule initialization with NOT operator and multiple rules"""
        rule1 = MagicMock(spec=ProcessedRule)
        rule2 = MagicMock(spec=ProcessedRule)

        with pytest.raises(TypeError, match="Not Operator can only contain one rule"):
            LogicalRule(LogicalOperator.NOT, [rule1, rule2])

    def test_parsed_rule_property(self):
        """Test parsed_rule property"""
        # Create processed rules with parsed_rule property
        rule1 = MagicMock(spec=ProcessedRule)
        rule1.parsed_rule = "Rule 1"
        rule2 = MagicMock(spec=ProcessedRule)
        rule2.parsed_rule = "Rule 2"

        # Create logical rule
        logical_rule = LogicalRule(LogicalOperator.AND, [rule1, rule2])

        # Check parsed_rule property
        assert logical_rule.parsed_rule == {LogicalOperator.AND: ["Rule 1", "Rule 2"]}

    def test_get_validator_and(self):
        """Test get_validator method with AND operator"""
        # Create processed rules with get_validator method
        rule1 = MagicMock(spec=ProcessedRule)
        rule1.get_validator.return_value = lambda x: x + 1

        rule2 = MagicMock(spec=ProcessedRule)
        rule2.get_validator.return_value = lambda x: x * 2

        # Create logical rule
        logical_rule = LogicalRule(LogicalOperator.AND, [rule1, rule2])

        # Get validator
        field_instance = MagicMock()
        validator = logical_rule.get_validator(field_instance)

        # Each rule's get_validator should be called
        rule1.get_validator.assert_called_once_with(field_instance)
        rule2.get_validator.assert_called_once_with(field_instance)

        # Both validations should pass
        assert validator(5) == 5

    def test_get_validator_not(self):
        """Test get_validator method with NOT operator"""
        # Create processed rule with get_validator method
        rule = MagicMock(spec=ProcessedRule)

        def fails_for_negative(x):
            if x < 0:
                raise ValueError("Value must be non-negative")
            return x

        rule.get_validator.return_value = fails_for_negative

        # Create logical rule
        logical_rule = LogicalRule(LogicalOperator.NOT, [rule])

        # Get validator
        field_instance = MagicMock()
        validator = logical_rule.get_validator(field_instance)

        # Rule's get_validator should be called
        rule.get_validator.assert_called_once_with(field_instance)

        # Test validation - negative values should pass with NOT
        assert validator(-5) == -5

        # Positive values should fail with NOT
        with pytest.raises(ValueError, match="Condition was met, but expected NOT to be met"):
            validator(5)

    def test_get_validator_invalid_operator(self):
        """Test get_validator with an invalid operator"""
        rule = MagicMock(spec=ProcessedRule)
        logical_rule = LogicalRule(LogicalOperator.AND, [rule])

        # Hack the operator to an invalid value
        logical_rule.operator = "INVALID"

        # Should raise TypeError
        with pytest.raises(TypeError, match="Logical Operator not recognised"):
            logical_rule.get_validator(MagicMock())

    def test_get_front_end_repr(self):
        """Test get_front_end_repr method"""
        # Create processed rules with get_front_end_repr method
        rule1 = MagicMock(spec=ProcessedRule)
        rule1.get_front_end_repr.return_value = {"rule": "Rule 1"}

        rule2 = MagicMock(spec=ProcessedRule)
        rule2.get_front_end_repr.return_value = {"rule": "Rule 2"}

        # Create logical rule
        logical_rule = LogicalRule(LogicalOperator.OR, [rule1, rule2])

        # Get front end representation
        result = logical_rule.get_front_end_repr()

        # Check result
        assert result == {LogicalOperator.OR: [{"rule": "Rule 1"}, {"rule": "Rule 2"}]}
