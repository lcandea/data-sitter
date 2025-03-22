import pytest
from data_sitter.rules.ProcessedRule import ProcessedRule


class TestProcessedRule:
    def test_abstract_class(self):
        """Test that ProcessedRule is an abstract class that can't be instantiated directly"""

        # Direct instantiation should fail
        with pytest.raises(TypeError, match="Can't instantiate abstract class ProcessedRule"):
            ProcessedRule("TestField", "Test rule", lambda self: None)

    def test_abstract_methods(self):
        """Test that ProcessedRule has the expected abstract methods"""

        # Create a concrete subclass that doesn't implement the abstract methods
        class ConcreteRule(ProcessedRule):
            pass

        # Instantiation should still fail because abstract methods aren't implemented
        with pytest.raises(TypeError, match="Can't instantiate abstract class ConcreteRule"):
            ConcreteRule("TestField", "Test rule", lambda self: None)

        # Create a concrete subclass that implements only one abstract method
        class PartialRule(ProcessedRule):
            def get_validator(self, field_instance):
                return lambda x: x

        # Instantiation should still fail because not all abstract methods are implemented
        with pytest.raises(TypeError, match="Can't instantiate abstract class PartialRule"):
            PartialRule("TestField", "Test rule", lambda self: None)

        # Create a fully-implemented concrete subclass
        class FullRule(ProcessedRule):
            def get_validator(self, field_instance):
                return lambda x: x

            def get_front_end_repr(self):
                return {"rule": self.field_rule}

        # This should succeed
        rule = FullRule("TestField", "Test rule", lambda self: None)
        assert isinstance(rule, ProcessedRule)
