import pytest
from unittest.mock import MagicMock, patch

from data_sitter.FieldResolver import FieldResolver, RuleNotFoundError, MalformedLogicalRuleError
from data_sitter.rules.Parser import RuleParser
from data_sitter.rules import Rule, MatchedRule, ProcessedRule, LogicalRule, LogicalOperator


@pytest.fixture
def rule_parser():
    return RuleParser({"min_val": 10, "max_val": 100})


@pytest.fixture
def mock_field_class():
    field_class = MagicMock()
    field_class.__name__ = "MockField"
    return field_class


@pytest.fixture
def mock_rule():
    rule = MagicMock(spec=Rule)
    rule.pattern = r"test_rule:(\d+)"
    return rule


@pytest.fixture
def mock_matched_rule():
    return MagicMock(spec=MatchedRule)


@pytest.fixture
def field_resolver(mock_field_class, rule_parser):
    # Directly mock the class method without using patch
    with patch('data_sitter.FieldResolver.RuleRegistry.get_rules_for', return_value=[]) as mock_get_rules:
        resolver = FieldResolver(mock_field_class, rule_parser)
        return resolver


class TestFieldResolver:
    def test_init(self, field_resolver, mock_field_class, rule_parser):
        """Test initialization of FieldResolver"""
        assert field_resolver.field_class == mock_field_class
        assert field_resolver.rule_parser == rule_parser
        assert hasattr(field_resolver, 'rules')
        assert hasattr(field_resolver, '_match_rule_cache')

    def test_get_field_validator(self, field_resolver, mock_field_class):
        """Test get_field_validator method"""
        # Setup
        mock_field_instance = MagicMock()
        mock_field_class.return_value = mock_field_instance

        # Mock get_processed_rules to return a list of processed rules
        mock_processed_rule = MagicMock(spec=ProcessedRule)
        mock_validator = MagicMock()
        mock_processed_rule.get_validator.return_value = mock_validator

        with patch.object(field_resolver, 'get_processed_rules', return_value=[mock_processed_rule]):
            # Call the method
            result = field_resolver.get_field_validator("test_field", ["rule1", "rule2"])

            # Assertions
            assert result == mock_field_instance
            mock_field_class.assert_called_once_with("test_field")
            mock_processed_rule.get_validator.assert_called_once_with(mock_field_instance)
            assert mock_field_instance.validators == [mock_validator]

    def test_get_processed_rules_with_string_rules(self, field_resolver):
        """Test get_processed_rules method with string rules"""
        # Setup
        mock_matched_rule = MagicMock(spec=MatchedRule)

        with patch.object(field_resolver, '_match_rule', return_value=mock_matched_rule):
            # Call the method
            result = field_resolver.get_processed_rules(["rule1", "rule2"])

            # Assertions
            assert len(result) == 2
            assert all(r == mock_matched_rule for r in result)
            assert field_resolver._match_rule.call_count == 2

    def test_get_processed_rules_with_logical_rules(self, field_resolver):
        """Test get_processed_rules method with logical rules"""
        # Setup
        mock_matched_rule = MagicMock(spec=MatchedRule)

        with patch.object(field_resolver, '_match_rule', return_value=mock_matched_rule):
            # Call the method with a logical AND rule
            result = field_resolver.get_processed_rules([{"AND": ["rule1", "rule2"]}])

            # Assertions
            assert len(result) == 1
            assert isinstance(result[0], LogicalRule)
            assert result[0].operator == LogicalOperator.AND
            assert len(result[0].processed_rules) == 2

    def test_get_processed_rules_with_not_operator(self, field_resolver):
        """Test get_processed_rules method with NOT operator"""
        # Setup
        mock_matched_rule = MagicMock(spec=MatchedRule)

        with patch.object(field_resolver, '_match_rule', return_value=mock_matched_rule):
            # Call the method with a NOT rule (single rule version)
            result = field_resolver.get_processed_rules([{"NOT": "rule1"}])

            # Assertions
            assert len(result) == 1
            assert isinstance(result[0], LogicalRule)
            assert result[0].operator == LogicalOperator.NOT
            assert len(result[0].processed_rules) == 1

    def test_rule_not_found_error(self, field_resolver):
        """Test that RuleNotFoundError is raised when no rule matches"""
        with patch.object(field_resolver, '_match_rule', return_value=None):
            with pytest.raises(RuleNotFoundError):
                field_resolver.get_processed_rules(["unknown_rule"])

    def test_malformed_logical_rule_error(self, field_resolver):
        """Test that MalformedLogicalRuleError is raised for invalid logical rules"""
        # Invalid operator
        with pytest.raises(MalformedLogicalRuleError):
            field_resolver.get_processed_rules([{"invalid_operator": ["rule1", "rule2"]}])

        # Multiple operators
        with pytest.raises(MalformedLogicalRuleError):
            field_resolver.get_processed_rules([{"and": ["rule1"], "or": ["rule2"]}])

    def test_match_rule_cache(self, field_resolver, mock_rule, mock_matched_rule):
        """Test that _match_rule uses caching for efficiency"""
        field_resolver.rules = [mock_rule]

        with patch.object(field_resolver.rule_parser, 'match', return_value=mock_matched_rule):
            # First call - should call rule_parser.match
            result1 = field_resolver._match_rule("test_rule:42")
            assert result1 == mock_matched_rule
            field_resolver.rule_parser.match.assert_called_once()

            # Reset mock to verify it's not called again
            field_resolver.rule_parser.match.reset_mock()

            # Second call with same parsed_rule - should use cache
            result2 = field_resolver._match_rule("test_rule:42")
            assert result2 == mock_matched_rule
            field_resolver.rule_parser.match.assert_not_called()

    def test_match_rule_no_match(self, field_resolver, mock_rule):
        """Test that _match_rule returns None when no rule matches"""
        field_resolver.rules = [mock_rule]

        with patch.object(field_resolver.rule_parser, 'match', return_value=None):
            result = field_resolver._match_rule("unknown_rule")
            assert result is None

    def test_type_error_for_invalid_rule_type(self, field_resolver):
        """Test that TypeError is raised for invalid rule types"""
        with pytest.raises(TypeError):
            field_resolver.get_processed_rules([42])  # Integer is not a valid rule type
