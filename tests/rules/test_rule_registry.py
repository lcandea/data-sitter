import pytest
from unittest.mock import MagicMock, patch

from data_sitter.rules.Rule import Rule
from data_sitter.field_types.FieldTypes import FieldTypes
from data_sitter.rules.RuleRegistry import RuleRegistry, register_rule, register_field


# Define hierarchy of fields
class BaseField:
    type_name = FieldTypes.BASE

    @staticmethod
    def get_parents():
        return []

    def test_rule(self, param):
        return lambda x: x

    def test_rule_fixed(self, fixed_param):
        return lambda x: x


class MiddleField:
    type_name = FieldTypes.NUMERIC

    @staticmethod
    def get_parents():
        return [BaseField]

class LeafField:
    type_name = FieldTypes.INT

    @staticmethod
    def get_parents():
        return [MiddleField]


class TestRuleRegistry:
    def setup_method(self):
        """Setup method to reset the RuleRegistry before each test"""
        RuleRegistry.rules.clear()
        RuleRegistry.type_map.clear()
        if hasattr(BaseField.test_rule, '_rule_metadata'):
            delattr(BaseField.test_rule, '_rule_metadata')
        if hasattr(BaseField.test_rule_fixed, '_rule_metadata'):
            delattr(BaseField.test_rule_fixed, '_rule_metadata')

    def test_add_rule(self):
        rule = Rule(
            field_type = FieldTypes.BASE,
            field_rule = "Test rule with {param:Integer}",
            rule_setter=BaseField.test_rule
        )
        with pytest.raises(ValueError, match="Field not registered: Base"):
            RuleRegistry.add_rule(BaseField, rule)


    def test_register_rule_decorator(self):
        """Test register_rule decorator functionality using a real decorator with patched Rule"""
        # Adding a rule to the existing class
        register_rule("Test rule with {param:Integer}")(BaseField.test_rule)
        
        # Verify that the rule method has metadata
        assert hasattr(BaseField.test_rule, '_rule_metadata')
        rule_metadata = getattr(BaseField.test_rule, '_rule_metadata')
        assert rule_metadata.rule == "Test rule with {param:Integer}"
        assert rule_metadata.fixed_params == {}

    @patch('data_sitter.rules.RuleRegistry.Rule')
    def test_register_rule_with_fixed_params(self, mock_rule):
        """Test register_rule with fixed parameters"""
        # Adding a rule to the existing class function
        register_rule("Test with fixed param", fixed_params={"fixed_param": 42})(BaseField.test_rule_fixed)

        # Verify that the rule method has metadata
        assert hasattr(BaseField.test_rule_fixed, '_rule_metadata')
        rule_metadata = getattr(BaseField.test_rule_fixed, '_rule_metadata')
        assert rule_metadata.rule == "Test with fixed param"
        assert rule_metadata.fixed_params == {"fixed_param": 42}

    @patch('data_sitter.rules.RuleRegistry.Rule')
    def test_register_field_decorator(self, mock_rule):
        """Test register_field decorator functionality"""
        # Setup mock Rule to return a configured rule object
        rule_instance = MagicMock()
        rule_instance.field_type = FieldTypes.BASE
        rule_instance.field_rule = "Test with fixed param"
        rule_instance.fixed_params = {"fixed_param": 42}
        mock_rule.return_value = rule_instance

        # Adding a rule to the existing class function
        register_rule("Test with fixed param", fixed_params={"fixed_param": 42})(BaseField.test_rule_fixed)

        # Register a field
        register_field(BaseField)

        # Check the field was registered
        assert RuleRegistry.type_map[FieldTypes.BASE] == BaseField

        # The decorator should return the class unchanged
        assert BaseField.__name__ == "BaseField"

        # Check the rules list
        assert len(RuleRegistry.rules[FieldTypes.BASE]) == 1
        assert RuleRegistry.rules[FieldTypes.BASE][0].fixed_params == {"fixed_param": 42}

        # Verify Rule was created with correct args
        mock_rule.assert_called_once()
        _, kwargs = mock_rule.call_args
        assert kwargs["field_type"] == FieldTypes.BASE  # field_type
        assert kwargs["field_rule"] == "Test with fixed param"  # field_rule
        assert kwargs["rule_setter"].__name__ == "test_rule_fixed"  # rule_setter
        assert kwargs["fixed_params"] == {"fixed_param": 42}  # Check fixed params

    def test_get_type(self):
        """Test get_type method"""
        # Register a field
        register_field(BaseField)

        # Check get_type returns the correct class
        assert RuleRegistry.get_type(FieldTypes.BASE) == BaseField

        # Check get_type returns None for non-existent type
        assert RuleRegistry.get_type("NonExistentField") is None

    def test_get_rules_for_single_level(self):
        """Test get_rules_for with a class with no parent fields"""
        # Register a field
        register_field(BaseField)

        # Create and add a rule directly to RuleRegistry
        rule = MagicMock()
        rule.field_type = FieldTypes.BASE
        rule.field_rule = "Base rule"
        RuleRegistry.rules[FieldTypes.BASE].append(rule)

        # Get rules for the base field
        rules = RuleRegistry.get_rules_for(BaseField)

        # Should only have the base rule
        assert len(rules) == 1
        assert rules[0].field_rule == "Base rule"

    def test_get_rules_for_inheritance(self):
        """Test get_rules_for with a class that inherits from another field"""
        # Register the fields
        register_field(BaseField)
        register_field(MiddleField)

        # Create and add rules directly to RuleRegistry
        base_rule = MagicMock()
        base_rule.field_type = FieldTypes.BASE
        base_rule.field_rule = "Base rule"
        RuleRegistry.rules[FieldTypes.BASE].append(base_rule)

        middle_rule = MagicMock()
        middle_rule.field_type = MiddleField.type_name
        middle_rule.field_rule = "Derived rule"
        RuleRegistry.rules[MiddleField.type_name].append(middle_rule)

        # Get rules for the derived field
        rules = RuleRegistry.get_rules_for(MiddleField)

        # Should have both base and derived rules
        assert len(rules) == 2
        rule_texts = [r.field_rule for r in rules]
        assert "Derived rule" in rule_texts
        assert "Base rule" in rule_texts

    def test_get_rules_for_multi_level_inheritance(self):
        """Test get_rules_for with multi-level inheritance"""
        # Register the fields
        register_field(BaseField)
        register_field(MiddleField)
        register_field(LeafField)

        # Create and add rules directly to RuleRegistry
        base_rule = MagicMock()
        base_rule.field_type = FieldTypes.BASE
        base_rule.field_rule = "Base rule"
        RuleRegistry.rules[FieldTypes.BASE].append(base_rule)

        middle_rule = MagicMock()
        middle_rule.field_type = MiddleField.type_name
        middle_rule.field_rule = "Middle rule"
        RuleRegistry.rules[MiddleField.type_name].append(middle_rule)

        leaf_rule = MagicMock()
        leaf_rule.field_type = LeafField.type_name
        leaf_rule.field_rule = "Leaf rule"
        RuleRegistry.rules[LeafField.type_name].append(leaf_rule)

        # Get rules for the leaf field
        rules = RuleRegistry.get_rules_for(LeafField)

        # Should have all rules in the hierarchy
        assert len(rules) == 3
        rule_texts = [r.field_rule for r in rules]
        assert "Leaf rule" in rule_texts
        assert "Middle rule" in rule_texts
        assert "Base rule" in rule_texts

    def test_get_rules_definition(self):
        """Test get_rules_definition method"""
        # Register the fields
        register_field(BaseField)
        register_field(MiddleField)

        # Create and add rules directly to RuleRegistry
        base_rule = MagicMock()
        base_rule.field_type = FieldTypes.BASE
        base_rule.field_rule = "Base rule"
        RuleRegistry.rules[FieldTypes.BASE].append(base_rule)

        middle_rule = MagicMock()
        middle_rule.field_type = MiddleField.type_name
        middle_rule.field_rule = "Child rule"
        RuleRegistry.rules[MiddleField.type_name].append(middle_rule)

        # Get rules definition
        rules_def = RuleRegistry.get_rules_definition()

        # Should have both fields
        assert len(rules_def) == 2

        # Find definitions for each field
        base_def = next(r for r in rules_def if r["field"] == FieldTypes.BASE)
        child_def = next(r for r in rules_def if r["field"] == MiddleField.type_name)

        # Check parent relationships
        assert base_def["parent_field"] == []
        assert child_def["parent_field"] == [FieldTypes.BASE]

        # Check rules
        assert len(base_def["rules"]) == 1
        assert base_def["rules"][0].field_rule == "Base rule"

        assert len(child_def["rules"]) == 1
        assert child_def["rules"][0].field_rule == "Child rule"
