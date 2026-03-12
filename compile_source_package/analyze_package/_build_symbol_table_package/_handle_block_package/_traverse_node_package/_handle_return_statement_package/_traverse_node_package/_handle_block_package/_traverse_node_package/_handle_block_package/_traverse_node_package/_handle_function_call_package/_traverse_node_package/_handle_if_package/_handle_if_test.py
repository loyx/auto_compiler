# -*- coding: utf-8 -*-
"""
Unit tests for _handle_if function.
Tests cover happy paths, boundary conditions, and error handling.
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._handle_if_src import _handle_if

# Type aliases for test clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIf(unittest.TestCase):
    """Test cases for _handle_if function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.mock_traverse_node_patcher = patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_if_package._traverse_node"
        )
        self.mock_traverse_node = self.mock_traverse_node_patcher.start()

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        self.mock_traverse_node_patcher.stop()

    def _create_symbol_table(self) -> SymbolTable:
        """Helper to create a fresh symbol table."""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def _create_if_node(
        self,
        line: int = 10,
        column: int = 5,
        children: list = None
    ) -> AST:
        """Helper to create an if statement AST node."""
        return {
            "type": "if",
            "line": line,
            "column": column,
            "children": children if children is not None else []
        }

    # ==================== Happy Path Tests ====================

    def test_handle_if_with_condition_and_then_branch(self) -> None:
        """Test if statement with condition and then-branch (2 children)."""
        # Arrange
        condition_node = {"type": "binary_op", "value": "x > 0"}
        then_branch_node = {"type": "block", "children": []}
        node = self._create_if_node(
            line=10,
            column=5,
            children=[condition_node, then_branch_node]
        )
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.assertEqual(self.mock_traverse_node.call_count, 2)
        self.mock_traverse_node.assert_any_call(condition_node, symbol_table)
        self.mock_traverse_node.assert_any_call(then_branch_node, symbol_table)
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_handle_if_with_condition_then_and_else_branch(self) -> None:
        """Test if statement with condition, then-branch, and else-branch (3 children)."""
        # Arrange
        condition_node = {"type": "binary_op", "value": "x > 0"}
        then_branch_node = {"type": "block", "children": []}
        else_branch_node = {"type": "block", "children": []}
        node = self._create_if_node(
            line=15,
            column=8,
            children=[condition_node, then_branch_node, else_branch_node]
        )
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.assertEqual(self.mock_traverse_node.call_count, 3)
        self.mock_traverse_node.assert_any_call(condition_node, symbol_table)
        self.mock_traverse_node.assert_any_call(then_branch_node, symbol_table)
        self.mock_traverse_node.assert_any_call(else_branch_node, symbol_table)
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_handle_if_with_more_than_three_children(self) -> None:
        """Test if statement with extra children (e.g., elif branches)."""
        # Arrange
        condition_node = {"type": "binary_op", "value": "x > 0"}
        then_branch_node = {"type": "block", "children": []}
        else_branch_node = {"type": "block", "children": []}
        extra_node = {"type": "block", "children": []}
        node = self._create_if_node(
            line=20,
            column=3,
            children=[condition_node, then_branch_node, else_branch_node, extra_node]
        )
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        # Should process first 3 children (condition, then, else)
        self.assertEqual(self.mock_traverse_node.call_count, 3)
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    # ==================== Boundary Condition Tests ====================

    def test_handle_if_with_empty_children(self) -> None:
        """Test if statement with empty children list."""
        # Arrange
        node = self._create_if_node(
            line=25,
            column=10,
            children=[]
        )
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.mock_traverse_node.assert_not_called()
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("missing children", errors[0])
        self.assertIn("line 25", errors[0])
        self.assertIn("column 10", errors[0])

    def test_handle_if_with_none_children(self) -> None:
        """Test if statement with None as children."""
        # Arrange
        node = self._create_if_node(
            line=30,
            column=7,
            children=None
        )
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.mock_traverse_node.assert_not_called()
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("missing children", errors[0])

    def test_handle_if_without_children_key(self) -> None:
        """Test if statement node without 'children' key."""
        # Arrange
        node = {
            "type": "if",
            "line": 35,
            "column": 12
        }
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.mock_traverse_node.assert_not_called()
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("missing children", errors[0])

    def test_handle_if_with_only_one_child(self) -> None:
        """Test if statement with only condition (missing then-branch)."""
        # Arrange
        condition_node = {"type": "binary_op", "value": "x > 0"}
        node = self._create_if_node(
            line=40,
            column=5,
            children=[condition_node]
        )
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.mock_traverse_node.assert_not_called()
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("expected at least 2 children", errors[0])
        self.assertIn("got 1", errors[0])
        self.assertIn("line 40", errors[0])
        self.assertIn("column 5", errors[0])

    # ==================== Error Message Content Tests ====================

    def test_handle_if_error_message_contains_location_info(self) -> None:
        """Test that error messages include line and column information."""
        # Arrange
        node = self._create_if_node(
            line=100,
            column=25,
            children=[]
        )
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line 100", errors[0])
        self.assertIn("column 25", errors[0])
        self.assertIn("if statement", errors[0])

    def test_handle_if_error_message_with_unknown_location(self) -> None:
        """Test error message when line/column are missing from node."""
        # Arrange
        node = {
            "type": "if",
            "children": []
        }
        symbol_table = self._create_symbol_table()

        # Act
        _handle_if(node, symbol_table)

        # Assert
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("unknown", errors[0])

    # ==================== Side Effects Tests ====================

    def test_handle_if_appends_to_existing_errors_list(self) -> None:
        """Test that errors are appended to existing errors list."""
        # Arrange
        node = self._create_if_node(
            line=50,
            column=5,
            children=[]
        )
        symbol_table = self._create_symbol_table()
        symbol_table["errors"].append("pre-existing error")

        # Act
        _handle_if(node, symbol_table)

        # Assert
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0], "pre-existing error")
        self.assertIn("missing children", errors[1])

    def test_handle_if_creates_errors_list_if_not_exists(self) -> None:
        """Test that errors list is created if not present in symbol_table."""
        # Arrange
        node = self._create_if_node(
            line=55,
            column=8,
            children=[]
        )
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_handle_if_does_not_modify_other_symbol_table_fields(self) -> None:
        """Test that _handle_if only modifies errors list."""
        # Arrange
        node = self._create_if_node(
            line=60,
            column=10,
            children=[]
        )
        symbol_table = self._create_symbol_table()
        symbol_table["variables"]["x"] = {"data_type": "int", "is_declared": True}
        symbol_table["functions"]["main"] = {"return_type": "int", "params": []}
        symbol_table["current_scope"] = 1
        original_vars = dict(symbol_table["variables"])
        original_funcs = dict(symbol_table["functions"])
        original_scope = symbol_table["current_scope"]

        # Act
        _handle_if(node, symbol_table)

        # Assert
        self.assertEqual(symbol_table["variables"], original_vars)
        self.assertEqual(symbol_table["functions"], original_funcs)
        self.assertEqual(symbol_table["current_scope"], original_scope)


if __name__ == "__main__":
    unittest.main()
