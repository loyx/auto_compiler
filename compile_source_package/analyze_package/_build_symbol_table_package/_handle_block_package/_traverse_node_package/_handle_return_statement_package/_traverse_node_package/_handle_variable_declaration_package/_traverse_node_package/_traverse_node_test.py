# -*- coding: utf-8 -*-
"""Unit tests for _traverse_node function."""

import unittest
from typing import Any, Dict

from ._traverse_node_src import _traverse_node


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNodeLiteral(unittest.TestCase):
    """Test cases for literal node type."""

    def test_literal_int_value(self):
        """Literal node with integer value returns the value."""
        node: AST = {"type": "literal", "value": 42}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 42)

    def test_literal_string_value(self):
        """Literal node with string value returns the value."""
        node: AST = {"type": "literal", "value": "hello"}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, "hello")

    def test_literal_float_value(self):
        """Literal node with float value returns the value."""
        node: AST = {"type": "literal", "value": 3.14}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 3.14)

    def test_literal_none_value(self):
        """Literal node with None value returns None."""
        node: AST = {"type": "literal", "value": None}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)


class TestTraverseNodeIdentifier(unittest.TestCase):
    """Test cases for identifier node type."""

    def test_identifier_defined_variable(self):
        """Identifier node with defined variable returns variable value."""
        node: AST = {"type": "identifier", "name": "x", "line": 5}
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"value": 10, "data_type": "int", "is_declared": True}
            }
        }
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 10)

    def test_identifier_undefined_variable(self):
        """Identifier node with undefined variable records error and returns None."""
        node: AST = {"type": "identifier", "name": "y", "line": 10}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Undefined variable 'y'", symbol_table["errors"][0])
        self.assertIn("line 10", symbol_table["errors"][0])

    def test_identifier_existing_errors_list(self):
        """Identifier with undefined variable appends to existing errors list."""
        node: AST = {"type": "identifier", "name": "z", "line": 15}
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": ["Previous error"]
        }
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0], "Previous error")

    def test_identifier_missing_line_info(self):
        """Identifier without line info uses 'unknown' for line."""
        node: AST = {"type": "identifier", "name": "a"}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)
        self.assertIn("unknown", symbol_table["errors"][0])


class TestTraverseNodeBinaryExpression(unittest.TestCase):
    """Test cases for binary_expression node type."""

    def test_binary_addition(self):
        """Binary expression with + operator adds values."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 8)

    def test_binary_subtraction(self):
        """Binary expression with - operator subtracts values."""
        node: AST = {
            "type": "binary_expression",
            "operator": "-",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 4}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 6)

    def test_binary_multiplication(self):
        """Binary expression with * operator multiplies values."""
        node: AST = {
            "type": "binary_expression",
            "operator": "*",
            "left": {"type": "literal", "value": 6},
            "right": {"type": "literal", "value": 7}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 42)

    def test_binary_division(self):
        """Binary expression with / operator divides values."""
        node: AST = {
            "type": "binary_expression",
            "operator": "/",
            "left": {"type": "literal", "value": 20},
            "right": {"type": "literal", "value": 4}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 5.0)

    def test_binary_division_by_zero(self):
        """Binary expression with division by zero records error and returns None."""
        node: AST = {
            "type": "binary_expression",
            "operator": "/",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 0},
            "line": 25
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Division by zero", symbol_table["errors"][0])
        self.assertIn("line 25", symbol_table["errors"][0])

    def test_binary_invalid_operator(self):
        """Binary expression with invalid operator returns None."""
        node: AST = {
            "type": "binary_expression",
            "operator": "%",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 3}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_binary_left_operand_undefined(self):
        """Binary expression with undefined left variable returns None."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "identifier", "name": "undefined_var", "line": 30},
            "right": {"type": "literal", "value": 5}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_binary_right_operand_undefined(self):
        """Binary expression with undefined right variable returns None."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "identifier", "name": "undefined_var", "line": 35}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_binary_nested_expression(self):
        """Binary expression with nested binary expressions."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {
                "type": "binary_expression",
                "operator": "*",
                "left": {"type": "literal", "value": 2},
                "right": {"type": "literal", "value": 3}
            },
            "right": {
                "type": "binary_expression",
                "operator": "-",
                "left": {"type": "literal", "value": 10},
                "right": {"type": "literal", "value": 4}
            }
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 12)  # (2*3) + (10-4) = 6 + 6 = 12

    def test_binary_with_identifier_operands(self):
        """Binary expression with identifier operands."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "identifier", "name": "a", "line": 40},
            "right": {"type": "identifier", "name": "b", "line": 40}
        }
        symbol_table: SymbolTable = {
            "variables": {
                "a": {"value": 7, "data_type": "int"},
                "b": {"value": 3, "data_type": "int"}
            }
        }
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, 10)


class TestTraverseNodeEdgeCases(unittest.TestCase):
    """Test cases for edge cases and error handling."""

    def test_node_is_none(self):
        """None node returns None."""
        result = _traverse_node(None, {"variables": {}})
        self.assertIsNone(result)

    def test_unknown_node_type(self):
        """Unknown node type returns None."""
        node: AST = {"type": "unknown_type", "value": 42}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_node_missing_type_field(self):
        """Node without type field returns None."""
        node: AST = {"value": 42}
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_binary_expression_missing_left(self):
        """Binary expression without left operand returns None."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "right": {"type": "literal", "value": 5}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_binary_expression_missing_right(self):
        """Binary expression without right operand returns None."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "literal", "value": 5}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_binary_expression_missing_operator(self):
        """Binary expression without operator returns None."""
        node: AST = {
            "type": "binary_expression",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_symbol_table_without_variables(self):
        """Symbol table without variables key uses empty dict."""
        node: AST = {"type": "identifier", "name": "x", "line": 50}
        symbol_table: SymbolTable = {}
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_identifier_variable_without_value(self):
        """Identifier with variable that has no value returns None."""
        node: AST = {"type": "identifier", "name": "x", "line": 55}
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True}
            }
        }
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)

    def test_string_concatenation(self):
        """Binary expression with + operator on strings concatenates."""
        node: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "literal", "value": "hello"},
            "right": {"type": "literal", "value": " world"}
        }
        symbol_table: SymbolTable = {"variables": {}}
        result = _traverse_node(node, symbol_table)
        self.assertEqual(result, "hello world")


if __name__ == "__main__":
    unittest.main()
