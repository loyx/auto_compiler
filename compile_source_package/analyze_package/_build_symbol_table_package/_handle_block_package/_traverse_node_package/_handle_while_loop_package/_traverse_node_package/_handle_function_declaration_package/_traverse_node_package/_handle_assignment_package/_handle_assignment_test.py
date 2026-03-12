"""
Unit tests for _handle_assignment function.
"""
import unittest
from unittest.mock import patch
from typing import Any, Dict

# Import the function under test using relative import
from ._handle_assignment_src import _handle_assignment

# Type aliases matching the source
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_assignment_with_existing_variable(self):
        """Test assignment when variable already exists in symbol_table."""
        node: AST = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": 10},
            "line": 5,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"type": "int", "line": 1, "column": 5, "scope": 0}
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

            # Variable should still exist (not modified)
            self.assertIn("x", symbol_table["variables"])
            # _traverse_node should be called with the value expression
            mock_traverse.assert_called_once_with({"type": "literal", "value": 10}, symbol_table)

    def test_assignment_with_new_variable(self):
        """Test assignment creates new variable entry when variable doesn't exist."""
        node: AST = {
            "type": "assignment",
            "target": "y",
            "value": {"type": "literal", "value": 20},
            "line": 10,
            "column": 15
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

            # New variable should be created
            self.assertIn("y", symbol_table["variables"])
            self.assertEqual(symbol_table["variables"]["y"]["line"], 10)
            self.assertEqual(symbol_table["variables"]["y"]["column"], 15)
            self.assertEqual(symbol_table["variables"]["y"]["scope"], 1)
            # _traverse_node should be called
            mock_traverse.assert_called_once()

    def test_assignment_without_value(self):
        """Test assignment when value is None."""
        node: AST = {
            "type": "assignment",
            "target": "z",
            "value": None,
            "line": 15,
            "column": 20
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

            # Variable should still be created
            self.assertIn("z", symbol_table["variables"])
            # _traverse_node should NOT be called when value is None
            mock_traverse.assert_not_called()

    def test_assignment_missing_target_key(self):
        """Test assignment when target key is missing from node."""
        node: AST = {
            "type": "assignment",
            "value": {"type": "literal", "value": 30},
            "line": 20,
            "column": 25
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._traverse_node_src._traverse_node") as mock_traverse:
            # Should not raise, target will be None
            _handle_assignment(node, symbol_table)

            # None should be added as a key (edge case behavior)
            self.assertIn(None, symbol_table["variables"])
            mock_traverse.assert_called_once()

    def test_assignment_with_empty_symbol_table(self):
        """Test assignment with minimal/empty symbol_table."""
        node: AST = {
            "type": "assignment",
            "target": "a",
            "value": {"type": "binary_op", "op": "+", "left": 1, "right": 2},
            "line": 25,
            "column": 30
        }
        symbol_table: SymbolTable = {}

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

            # variables dict should be created and variable added
            self.assertIn("variables", symbol_table)
            self.assertIn("a", symbol_table["variables"])
            # scope should default to 0 when current_scope is missing
            self.assertEqual(symbol_table["variables"]["a"]["scope"], 0)
            mock_traverse.assert_called_once()

    def test_assignment_with_complex_value_expression(self):
        """Test assignment with nested/complex value expression."""
        node: AST = {
            "type": "assignment",
            "target": "result",
            "value": {
                "type": "call",
                "function": "add",
                "args": [
                    {"type": "literal", "value": 5},
                    {"type": "literal", "value": 3}
                ]
            },
            "line": 30,
            "column": 35
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "add": {"return_type": "int", "params": ["a", "b"], "line": 1, "column": 1}
            },
            "current_scope": 0,
            "scope_stack": [0]
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

            self.assertIn("result", symbol_table["variables"])
            mock_traverse.assert_called_once_with(node["value"], symbol_table)

    def test_assignment_preserves_existing_variable_info(self):
        """Test that existing variable metadata is preserved during assignment."""
        node: AST = {
            "type": "assignment",
            "target": "existing_var",
            "value": {"type": "literal", "value": 100},
            "line": 50,
            "column": 55
        }
        original_var_info = {
            "type": "int",
            "line": 1,
            "column": 5,
            "scope": 0,
            "declared": True
        }
        symbol_table: SymbolTable = {
            "variables": {
                "existing_var": original_var_info.copy()
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_assignment_package._traverse_node_src._traverse_node"):
            _handle_assignment(node, symbol_table)

            # Existing variable info should be preserved (not overwritten)
            self.assertEqual(symbol_table["variables"]["existing_var"], original_var_info)


if __name__ == "__main__":
    unittest.main()
