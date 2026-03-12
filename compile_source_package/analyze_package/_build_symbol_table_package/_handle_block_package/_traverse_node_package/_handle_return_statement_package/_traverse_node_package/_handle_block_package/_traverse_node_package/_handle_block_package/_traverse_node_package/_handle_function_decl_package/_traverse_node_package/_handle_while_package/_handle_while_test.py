import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._handle_while_src import _handle_while

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhile(unittest.TestCase):
    """Test cases for _handle_while function."""

    def test_happy_path_valid_while_node(self):
        """Test handling a valid while node with condition and body."""
        condition_node = {"type": "assignment", "value": "x > 0"}
        body_node = {"type": "block", "children": []}
        while_node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse') as mock_traverse:
            _handle_while(while_node, symbol_table)

            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(condition_node, symbol_table)
            mock_traverse.assert_any_call(body_node, symbol_table)

            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_error_handling_insufficient_children(self):
        """Test error handling when while node has less than 2 children."""
        while_node = {
            "type": "while",
            "children": [{"type": "assignment"}],
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse') as mock_traverse:
            _handle_while(while_node, symbol_table)

            mock_traverse.assert_not_called()

            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["message"], "While node must have condition and body")
            self.assertEqual(error["line"], 15)
            self.assertEqual(error["column"], 8)
            self.assertEqual(error["severity"], "error")

            self.assertEqual(symbol_table["current_scope"], 0)

    def test_error_handling_no_children(self):
        """Test error handling when while node has no children."""
        while_node = {
            "type": "while",
            "children": [],
            "line": 20,
            "column": 3
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse') as mock_traverse:
            _handle_while(while_node, symbol_table)

            mock_traverse.assert_not_called()

            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["message"], "While node must have condition and body")

            self.assertEqual(symbol_table["current_scope"], 0)

    def test_initializes_errors_list_if_missing(self):
        """Test that errors list is initialized if not present in symbol_table."""
        condition_node = {"type": "assignment"}
        body_node = {"type": "block"}
        while_node = {
            "type": "while",
            "children": [condition_node, body_node]
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse'):
            _handle_while(while_node, symbol_table)

            self.assertIn("errors", symbol_table)
            self.assertIsInstance(symbol_table["errors"], list)

    def test_initializes_current_scope_if_missing(self):
        """Test that current_scope is handled if not present in symbol_table."""
        condition_node = {"type": "assignment"}
        body_node = {"type": "block"}
        while_node = {
            "type": "while",
            "children": [condition_node, body_node]
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse'):
            _handle_while(while_node, symbol_table)

            self.assertEqual(symbol_table["current_scope"], 0)

    def test_scope_management_nested(self):
        """Test scope management with nested while loops."""
        inner_condition = {"type": "assignment"}
        inner_body = {"type": "block"}
        inner_while = {
            "type": "while",
            "children": [inner_condition, inner_body]
        }

        outer_condition = {"type": "assignment"}
        outer_body = {"type": "block", "children": [inner_while]}
        outer_while = {
            "type": "while",
            "children": [outer_condition, outer_body]
        }

        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        def traverse_side_effect(node, st):
            if node.get("type") == "while":
                st["current_scope"] += 1
                st["current_scope"] -= 1

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse', side_effect=traverse_side_effect):
            _handle_while(outer_while, symbol_table)

            self.assertEqual(symbol_table["current_scope"], 0)

    def test_error_propagation_from_inline_traverse(self):
        """Test that errors from _inline_traverse are preserved."""
        condition_node = {"type": "assignment"}
        body_node = {"type": "block"}
        while_node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 5,
            "column": 2
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": [{"message": "Pre-existing error"}]
        }

        def add_error(node, st):
            st["errors"].append({"message": "Error from traverse"})

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse', side_effect=add_error):
            _handle_while(while_node, symbol_table)

            self.assertEqual(len(symbol_table["errors"]), 2)
            self.assertEqual(symbol_table["errors"][0]["message"], "Pre-existing error")
            self.assertEqual(symbol_table["errors"][1]["message"], "Error from traverse")

    def test_scope_increment_decrement_balance(self):
        """Test that scope is properly incremented and decremented."""
        condition_node = {"type": "assignment"}
        body_node = {"type": "block"}
        while_node = {
            "type": "while",
            "children": [condition_node, body_node]
        }
        symbol_table = {
            "variables": {},
            "current_scope": 5,
            "errors": []
        }

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse'):
            _handle_while(while_node, symbol_table)

            self.assertEqual(symbol_table["current_scope"], 5)

    def test_missing_children_key_defaults_to_empty_list(self):
        """Test that missing children key is handled (defaults to empty list)."""
        while_node = {
            "type": "while",
            "line": 25,
            "column": 1
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        with patch('._inline_traverse_package._inline_traverse_src._inline_traverse') as mock_traverse:
            _handle_while(while_node, symbol_table)

            mock_traverse.assert_not_called()

            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["message"], "While node must have condition and body")


if __name__ == "__main__":
    unittest.main()
