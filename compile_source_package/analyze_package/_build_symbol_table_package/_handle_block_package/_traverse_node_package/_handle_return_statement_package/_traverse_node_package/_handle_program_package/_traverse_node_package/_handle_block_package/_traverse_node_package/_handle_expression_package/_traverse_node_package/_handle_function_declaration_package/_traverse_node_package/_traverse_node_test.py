# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === relative imports ===
from ._traverse_node_src import _traverse_node

# === ADT aliases (for test clarity) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_node_is_none_returns_silently(self):
        """Test that None node returns without side effects."""
        _traverse_node(None, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_function_declaration_dispatches_to_handler(self):
        """Test that function_declaration nodes call _handle_function_declaration."""
        node: AST = {
            "type": "function_declaration",
            "value": "test_func",
            "data_type": "int",
            "children": [],
            "line": 1,
            "column": 1
        }

        with patch(
            "._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration"
        ) as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_variable_declaration_dispatches_to_handler(self):
        """Test that variable_declaration nodes call _handle_variable_declaration."""
        node: AST = {
            "type": "variable_declaration",
            "value": "test_var",
            "data_type": "char",
            "children": [],
            "line": 2,
            "column": 5
        }

        with patch(
            "._handle_variable_declaration_package._handle_variable_declaration_src._handle_variable_declaration"
        ) as mock_handler:
            _traverse_node(node, self.symbol_table)
            mock_handler.assert_called_once_with(node, self.symbol_table)

    def test_other_type_recursively_traverses_children(self):
        """Test that other node types recursively traverse children."""
        child1: AST = {"type": "expression", "value": "a", "children": []}
        child2: AST = {"type": "expression", "value": "b", "children": []}
        node: AST = {
            "type": "block",
            "children": [child1, child2],
            "line": 3,
            "column": 1
        }

        # Should not raise and should traverse both children
        _traverse_node(node, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_empty_children_returns_without_error(self):
        """Test that node with empty children list returns without error."""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 4,
            "column": 1
        }

        _traverse_node(node, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_missing_children_field_returns_without_error(self):
        """Test that node without children field returns without error."""
        node: AST = {
            "type": "expression",
            "value": "x",
            "line": 5,
            "column": 1
        }

        _traverse_node(node, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_missing_type_field_traverses_children(self):
        """Test that node without type field still traverses children."""
        child: AST = {"type": "expression", "value": "y", "children": []}
        node: AST = {
            "value": "no_type",
            "children": [child],
            "line": 6,
            "column": 1
        }

        _traverse_node(node, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_nested_children_are_traversed(self):
        """Test that deeply nested children are all traversed."""
        grandchild: AST = {"type": "identifier", "value": "z", "children": []}
        child: AST = {"type": "expression", "children": [grandchild]}
        node: AST = {
            "type": "block",
            "children": [child],
            "line": 7,
            "column": 1
        }

        _traverse_node(node, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_handler_exception_added_to_errors(self):
        """Test that handler exceptions are caught and added to symbol_table errors."""
        node: AST = {
            "type": "function_declaration",
            "value": "bad_func",
            "children": [],
            "line": 8,
            "column": 1
        }

        with patch(
            "._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration",
            side_effect=RuntimeError("Handler failed")
        ):
            _traverse_node(node, self.symbol_table)

            self.assertEqual(len(self.symbol_table["errors"]), 1)
            error = self.symbol_table["errors"][0]
            self.assertEqual(error["type"], "handler_error")
            self.assertIn("Handler failed", error["message"])
            self.assertEqual(error["line"], 8)
            self.assertEqual(error["column"], 1)

    def test_multiple_children_all_traversed(self):
        """Test that all children in a list are traversed."""
        children = [
            {"type": "expression", "value": f"expr_{i}", "children": []}
            for i in range(5)
        ]
        node: AST = {
            "type": "block",
            "children": children,
            "line": 9,
            "column": 1
        }

        _traverse_node(node, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_mixed_node_types_in_children(self):
        """Test traversal of children with mixed node types."""
        children = [
            {"type": "expression", "value": "a", "children": []},
            {"type": "block", "children": []},
            {"type": "statement", "value": "stmt", "children": []},
        ]
        node: AST = {
            "type": "program",
            "children": children,
            "line": 10,
            "column": 1
        }

        _traverse_node(node, self.symbol_table)
        self.assertEqual(self.symbol_table["errors"], [])

    def test_handler_exception_does_not_stop_traversal(self):
        """Test that one handler exception doesn't prevent other children from being traversed."""
        child1: AST = {"type": "expression", "value": "ok", "children": []}
        child2: AST = {
            "type": "function_declaration",
            "value": "bad",
            "children": []
        }
        child3: AST = {"type": "expression", "value": "also_ok", "children": []}
        node: AST = {
            "type": "block",
            "children": [child1, child2, child3],
            "line": 11,
            "column": 1
        }

        with patch(
            "._handle_function_declaration_package._handle_function_declaration_src._handle_function_declaration",
            side_effect=RuntimeError("Handler failed")
        ):
            _traverse_node(node, self.symbol_table)

            # Should have recorded the error
            self.assertEqual(len(self.symbol_table["errors"]), 1)
            # child1 and child3 should still be processed (no errors from them)
            self.assertEqual(self.symbol_table["errors"][0]["type"], "handler_error")


if __name__ == "__main__":
    unittest.main()
