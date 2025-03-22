import pytest
from data_sitter.rules.Rule import Rule, NotAClassMethod, RuleFunctionParamsMismatch


class TestRule:
    def test_init(self):
        """Test Rule initialization"""
        def dummy_method(self, param):
            return param

        rule = Rule("TestField", "Test rule with {param:Integer}", dummy_method)

        assert rule.field_type == "TestField"
        assert rule.field_rule == "Test rule with {param:Integer}"
        assert rule.rule_setter == dummy_method
        assert rule.fixed_params == {}

    def test_init_with_fixed_params(self):
        """Test Rule initialization with fixed parameters"""
        def dummy_method(self, param1, param2):
            return param1, param2

        rule = Rule("TestField", "Test rule with {param1:Integer}", dummy_method,
                    fixed_params={"param2": "fixed_value"})

        assert rule.field_type == "TestField"
        assert rule.field_rule == "Test rule with {param1:Integer}"
        assert rule.fixed_params == {"param2": "fixed_value"}

        # Check that the rule_setter has been partially applied
        # When using functools.partial, the parameter is still visible but has a default value
        import inspect
        params = inspect.signature(rule.rule_setter).parameters
        assert "param2" in params
        assert params["param2"].default == "fixed_value"

    def test_repr(self):
        """Test Rule __repr__ method"""
        def dummy_method(self, param):
            return param

        rule = Rule("TestField", "Test rule with {param:Integer}", dummy_method)

        assert repr(rule) == "Test rule with {param:Integer}"

    def test_rule_params(self):
        """Test rule_params property"""
        def dummy_method(self, param1, param2):
            return param1, param2

        rule = Rule("TestField", "Test with {param1:Integer} and {param2:String}", dummy_method)

        assert rule.rule_params == {"param1": "Integer", "param2": "String"}

    def test_validate_non_class_method(self):
        """Test validation fails for functions that are not class methods"""
        def not_a_class_method(param):
            return param

        with pytest.raises(NotAClassMethod):
            Rule("TestField", "Test rule with {param:Integer}", not_a_class_method)

    def test_validate_params_mismatch(self):
        """Test validation fails when rule params and function params don't match"""
        def wrong_params(self, wrong_name):
            return wrong_name

        with pytest.raises(RuleFunctionParamsMismatch):
            Rule("TestField", "Test rule with {param:Integer}", wrong_params)

    def test_validate_fixed_params_not_in_function(self):
        """Test validation fails when fixed params are not in function signature"""
        def dummy_method(self, param):
            return param

        with pytest.raises(ValueError, match="The fixed parameter 'not_a_param' is not in the function"):
            Rule("TestField", "Test rule with {param:Integer}", dummy_method,
                fixed_params={"not_a_param": "value"})

    def test_fixed_params_matching(self):
        """Test rule creation works when rule params + fixed params match function params"""
        def three_params(self, param1, param2, param3):
            return param1, param2, param3

        # This should work - param1 from rule, param2 and param3 fixed
        rule = Rule("TestField", "Test with {param1:Integer}", three_params,
                    fixed_params={"param2": "fixed2", "param3": "fixed3"})

        assert rule.rule_params == {"param1": "Integer"}
        assert rule.fixed_params == {"param2": "fixed2", "param3": "fixed3"}
