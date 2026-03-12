# -*- coding: utf-8 -*-
"""
Unit tests for _traverse_node function.
Tests AST node traversal and handler dispatch logic.
"""

import unittest
from unittest.mock import patch
import sys
from io import StringIO

# Relative imports from the same package
from ._traverse_node_src import _traverse_node, AST, SymbolTable


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_function_declaration_dispatch(self):
        """Test dispatch to function_declaration handler."""
        node: AST = {
            "type": "function_declaration",
            "name": "test_func",
            "params": ["x", "y"],
            "body": {"type": "return_statement", "expression": 42},
            "return_type": "int",
            "line": 1,
            "column": 0
        }

        with patch("._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_variable_declaration_dispatch(self):
        """Test dispatch to variable_declaration handler."""
        node: AST = {
            "type": "variable_declaration",
            "name": "my_var",
            "var_type": "int",
            "value": 10,
            "line": 5,
            "column": 2
        }

        with patch("._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_assignment_dispatch(self):
        """Test dispatch to assignment handler."""
        node: AST = {
            "type": "assignment",
            "target": "my_var",
            "value": 20,
            "line": 10,
            "column": 4
        }

        with patch("._handle_assignment_package._handle_assignment_src._handle_assignment") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_if_statement_dispatch(self):
        """Test dispatch to if_statement handler."""
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": 1, "right": 2, "op": ">"},
            "then_branch": {"type": "assignment", "target": "x", "value": 1},
            "else_branch": {"type": "assignment", "target": "x", "value": 0},
            "line": 15,
            "column": 0
        }

        with patch("._handle_if_statement_package._handle_if_statement_src._handle_if_statement") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_loop_statement_dispatch(self):
        """Test dispatch to loop_statement handler."""
        node: AST = {
            "type": "loop_statement",
            "loop_type": "while",
            "condition": {"type": "binary_op", "left": "i", "right": 10, "op": "<"},
            "body": {"type": "assignment", "target": "i", "value": {"type": "binary_op", "left": "i", "right": 1, "op": "+"}},
            "line": 20,
            "column": 0
        }

        with patch("._handle_loop_statement_package._handle_loop_statement_src._handle_loop_statement") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_return_statement_dispatch(self):
        """Test dispatch to return_statement handler."""
        node: AST = {
            "type": "return_statement",
            "expression": 42,
            "line": 25,
            "column": 4
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._handle_return_statement") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_missing_type_field_raises_value_error(self):
        """Test that missing 'type' field raises ValueError."""
        node: AST = {
            "name": "test",
            "line": 30,
            "column": 0
        }

        with self.assertRaises(ValueError) as context:
            _traverse_node(node, self.symbol_table)

        self.assertIn("type", str(context.exception))
        self.assertIn("30", str(context.exception))

    def test_missing_type_field_with_unknown_line(self):
        """Test ValueError message when line number is also missing."""
        node: AST = {
            "name": "test",
            "column": 0
        }

        with self.assertRaises(ValueError) as context:
            _traverse_node(node, self.symbol_table)

        self.assertIn("type", str(context.exception))
        self.assertIn("unknown", str(context.exception))

    def test_unknown_node_type_logs_warning(self):
        """Test that unknown node type logs warning and continues."""
        node: AST = {
            "type": "unknown_type",
            "line": 35,
            "column": 0
        }

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            result = _traverse_node(node, self.symbol_table)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        self.assertIsNone(result)
        self.assertIn("Warning", output)
        self.assertIn("unknown_type", output)
        self.assertIn("35", output)

    def test_none_type_field_raises_value_error(self):
        """Test that None 'type' field raises ValueError."""
        node: AST = {
            "type": None,
            "line": 40,
            "column": 0
        }

        with self.assertRaises(ValueError) as context:
            _traverse_node(node, self.symbol_table)

        self.assertIn("type", str(context.exception))

    def test_empty_node_dict_raises_value_error(self):
        """Test that empty node dict raises ValueError."""
        node: AST = {}

        with self.assertRaises(ValueError) as context:
            _traverse_node(node, self.symbol_table)

        self.assertIn("type", str(context.exception))

    def test_handler_receives_correct_arguments(self):
        """Test that handler receives the exact node and symbol_table references."""
        node: AST = {
            "type": "function_declaration",
            "name": "test",
            "line": 45,
            "column": 0
        }

        with patch("._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_handler:
            _traverse_node(node, self.symbol_table)
            
            call_args = mock_handler.call_args
            self.assertIs(call_args[0][0], node)
            self.assertIs(call_args[0][1], self.symbol_table)

    def test_symbol_table_not_modified_for_unknown_type(self):
        """Test that symbol_table is not modified for unknown node types."""
        node: AST = {
            "type": "unknown_xyz",
            "line": 50,
            "column": 0
        }

        original_table = {
            "variables": {"x": 1},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        self.symbol_table.update(original_table)

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            _traverse_node(node, self.symbol_table)
        finally:
            sys.stdout = old_stdout

        self.assertEqual(self.symbol_table["variables"], {"x": 1})
        self.assertEqual(self.symbol_table["scope_stack"], [0])

    def test_multiple_node_types_sequential_dispatch(self):
        """Test sequential dispatch to different handlers."""
        nodes = [
            {"type": "function_declaration", "name": "func1", "line": 1},
            {"type": "variable_declaration", "name": "var1", "line": 2},
            {"type": "assignment", "target": "var1", "value": 10, "line": 3},
        ]

        with patch("._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_func:
            with patch("._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_var:
                with patch("._handle_assignment_package._handle_assignment_src._handle_assignment") as mock_assign:
                    for node in nodes:
                        _traverse_node(node, self.symbol_table)

                    self.assertEqual(mock_func.call_count, 1)
                    self.assertEqual(mock_var.call_count, 1)
                    self.assertEqual(mock_assign.call_count, 1)

    def test_handler_called_with_same_symbol_table_reference(self):
        """Test that all handlers receive the same symbol_table reference."""
        node1: AST = {"type": "function_declaration", "name": "f1", "line": 1}
        node2: AST = {"type": "variable_declaration", "name": "v1", "line": 2}

        with patch("._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_func:
            with patch("._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration") as mock_var:
                _traverse_node(node1, self.symbol_table)
                _traverse_node(node2, self.symbol_table)

                self.assertIs(mock_func.call_args[0][1], self.symbol_table)
                self.assertIs(mock_var.call_args[0][1], self.symbol_table)


class TestTraverseNodeEdgeCases(unittest.TestCase):
    """Edge case tests for _traverse_node function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_node_with_minimal_fields(self):
        """Test node with only required 'type' field."""
        node: AST = {"type": "return_statement"}

        with patch("._handle_return_statement_package._handle_return_statement_src._handle_return_statement") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_node_with_all_possible_fields(self):
        """Test node with all possible AST fields."""
        node: AST = {
            "type": "function_declaration",
            "name": "complete_func",
            "params": ["a", "b", "c"],
            "body": {"type": "return_statement", "expression": "a + b + c"},
            "return_type": "int",
            "line": 100,
            "column": 0,
            "value": None,
            "var_type": None,
            "target": None,
            "condition": None,
            "then_branch": None,
            "else_branch": None,
            "loop_type": None,
            "expression": None
        }

        with patch("._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_nested_node_structure(self):
        """Test node with deeply nested structure."""
        node: AST = {
            "type": "if_statement",
            "condition": {
                "type": "binary_op",
                "left": {
                    "type": "identifier",
                    "name": "x"
                },
                "right": {
                    "type": "literal",
                    "value": 10
                },
                "op": ">"
            },
            "then_branch": {
                "type": "block",
                "statements": [
                    {"type": "assignment", "target": "y", "value": 1}
                ]
            },
            "else_branch": None,
            "line": 1,
            "column": 0
        }

        with patch("._handle_if_statement_package._handle_if_statement_src._handle_if_statement") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_zero_line_number(self):
        """Test node with line number 0."""
        node: AST = {
            "type": "assignment",
            "target": "x",
            "value": 0,
            "line": 0,
            "column": 0
        }

        with patch("._handle_assignment_package._handle_assignment_src._handle_assignment") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_negative_column_number(self):
        """Test node with negative column number (edge case)."""
        node: AST = {
            "type": "return_statement",
            "expression": None,
            "line": 1,
            "column": -1
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._handle_return_statement") as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_empty_string_type(self):
        """Test node with empty string as type (treated as unknown)."""
        node: AST = {
            "type": "",
            "line": 1,
            "column": 0
        }

        captured_output = StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            result = _traverse_node(node, self.symbol_table)
            output = captured_output.getvalue()
        finally:
            sys.stdout = old_stdout

        self.assertIsNone(result)
        self.assertIn("Warning", output)
        self.assertIn("''", output)


if __name__ == "__main__":
    unittest.main()
