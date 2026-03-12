# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._handle_variable_declaration_src import _handle_variable_declaration

# === type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVariableDeclaration(unittest.TestCase):
    """Test cases for _handle_variable_declaration function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    def test_variable_with_name_and_type_only(self):
        """Test variable declaration with name and data_type but no initial value."""
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "value": None,
            "line": 10,
            "column": 5
        }

        _handle_variable_declaration(node, self.symbol_table)

        # Verify variable is registered in symbol_table
        self.assertIn("x", self.symbol_table["variables"])
        var_info = self.symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["is_declared"], True)
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)

    def test_variable_with_initial_value(self):
        """Test variable declaration with initial value triggers recursive traversal."""
        node: AST = {
            "type": "variable_declaration",
            "name": "y",
            "data_type": "char",
            "value": {"type": "literal", "value": "a"},
            "line": 15,
            "column": 8
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_variable_declaration(node, self.symbol_table)

            # Verify variable is registered
            self.assertIn("y", self.symbol_table["variables"])
            self.assertEqual(self.symbol_table["variables"]["y"]["data_type"], "char")

            # Verify _traverse_node was called with the value
            mock_traverse.assert_called_once()
            call_args = mock_traverse.call_args
            self.assertEqual(call_args[0][0], {"type": "literal", "value": "a"})
            self.assertEqual(call_args[0][1], self.symbol_table)

    def test_variable_without_initial_value_no_traverse(self):
        """Test that _traverse_node is NOT called when value is None."""
        node: AST = {
            "type": "variable_declaration",
            "name": "z",
            "data_type": "int",
            "value": None,
            "line": 20,
            "column": 3
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_variable_declaration(node, self.symbol_table)

            # Verify _traverse_node was NOT called
            mock_traverse.assert_not_called()

    def test_variable_with_scope_level(self):
        """Test variable registration respects current_scope level."""
        self.symbol_table["current_scope"] = 2
        self.symbol_table["scope_stack"] = ["global", "func1", "block1"]

        node: AST = {
            "type": "variable_declaration",
            "name": "local_var",
            "data_type": "int",
            "value": None,
            "line": 25,
            "column": 10
        }

        _handle_variable_declaration(node, self.symbol_table)

        var_info = self.symbol_table["variables"]["local_var"]
        self.assertEqual(var_info["scope_level"], 2)

    def test_missing_variable_name(self):
        """Test handling when variable name is missing."""
        node: AST = {
            "type": "variable_declaration",
            "name": None,
            "data_type": "int",
            "value": None,
            "line": 30,
            "column": 1
        }

        _handle_variable_declaration(node, self.symbol_table)

        # Variable should NOT be registered without a name
        self.assertEqual(len(self.symbol_table["variables"]), 0)

    def test_missing_data_type(self):
        """Test handling when data_type is missing."""
        node: AST = {
            "type": "variable_declaration",
            "name": "incomplete_var",
            "data_type": None,
            "value": None,
            "line": 35,
            "column": 1
        }

        _handle_variable_declaration(node, self.symbol_table)

        # Variable should NOT be registered without data_type
        self.assertEqual(len(self.symbol_table["variables"]), 0)

    def test_multiple_variables_sequential(self):
        """Test registering multiple variables sequentially."""
        nodes = [
            {"type": "variable_declaration", "name": "a", "data_type": "int", "value": None, "line": 1, "column": 1},
            {"type": "variable_declaration", "name": "b", "data_type": "char", "value": None, "line": 2, "column": 1},
            {"type": "variable_declaration", "name": "c", "data_type": "int", "value": None, "line": 3, "column": 1}
        ]

        for node in nodes:
            _handle_variable_declaration(node, self.symbol_table)

        # Verify all variables are registered
        self.assertEqual(len(self.symbol_table["variables"]), 3)
        self.assertIn("a", self.symbol_table["variables"])
        self.assertIn("b", self.symbol_table["variables"])
        self.assertIn("c", self.symbol_table["variables"])
        self.assertEqual(self.symbol_table["variables"]["a"]["data_type"], "int")
        self.assertEqual(self.symbol_table["variables"]["b"]["data_type"], "char")
        self.assertEqual(self.symbol_table["variables"]["c"]["data_type"], "int")

    def test_variable_with_zero_line_column(self):
        """Test variable with zero line and column values."""
        node: AST = {
            "type": "variable_declaration",
            "name": "zero_pos",
            "data_type": "int",
            "value": None,
            "line": 0,
            "column": 0
        }

        _handle_variable_declaration(node, self.symbol_table)

        var_info = self.symbol_table["variables"]["zero_pos"]
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_empty_node_dict(self):
        """Test handling of empty node dictionary."""
        node: AST = {}

        _handle_variable_declaration(node, self.symbol_table)

        # Should not register any variable
        self.assertEqual(len(self.symbol_table["variables"]), 0)

    def test_value_is_empty_dict_not_none(self):
        """Test that empty dict value still triggers traversal."""
        node: AST = {
            "type": "variable_declaration",
            "name": "with_empty_value",
            "data_type": "int",
            "value": {},
            "line": 40,
            "column": 5
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_variable_declaration(node, self.symbol_table)

            # Empty dict is not None, so traversal should be called
            mock_traverse.assert_called_once()


if __name__ == "__main__":
    unittest.main()
