import pytest
from data_sitter.rules.Enums import LogicalOperator


class TestLogicalOperator:
    def test_enum_values(self):
        """Test that LogicalOperator enum has the expected values"""
        assert LogicalOperator.AND == "AND"
        assert LogicalOperator.OR == "OR"
        assert LogicalOperator.NOT == "NOT"

    def test_enum_members(self):
        """Test that LogicalOperator enum has the expected members"""
        assert set(LogicalOperator) == {LogicalOperator.AND, LogicalOperator.OR, LogicalOperator.NOT}

    def test_str_conversion(self):
        """Test that LogicalOperator enum values convert properly to strings"""
        assert str(LogicalOperator.AND) == "AND"
        assert str(LogicalOperator.OR) == "OR"
        assert str(LogicalOperator.NOT) == "NOT"
