# === imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# === relative imports ===
from ._handle_variable_declaration_src import _handle_variable_declaration
from . import _handle_variable_declaration_src

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVariableDeclaration(unittest.TestCase):
    """Test cases for _handle_variable_declaration function."""

    def test_register_new_variable(self):
        """Happy path: register a new variable to symbol table."""
        node: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    def test_register_variable_char_type(self):
        """Test registering a variable with char data type."""
        node: AST = {
            "type": "variable_declaration",
            "value": "c",
            "data_type": "char",
            "line": 5,
            "column": 3,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 1
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["c"]["scope_level"], 1)

    def test_duplicate_variable_same_scope_records_error(self):
        """Test that duplicate variable in same scope records an error."""
        node1: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        node2: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 15,
            "column": 8,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }

        _handle_variable_declaration(node1, symbol_table)
        _handle_variable_declaration(node2, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "Variable 'x' already declared")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertEqual(error["type"], "redefinition")
        # Variable info should be updated to the new declaration
        self.assertEqual(symbol_table["variables"]["x"]["line"], 15)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 8)

    def test_duplicate_variable_different_scope_allows_shadowing(self):
        """Test that variable shadowing in different scope is allowed without error."""
        node1: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        node2: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "char",
            "line": 20,
            "column": 10,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }

        _handle_variable_declaration(node1, symbol_table)
        
        # Change scope
        symbol_table["current_scope"] = 1
        _handle_variable_declaration(node2, symbol_table)

        # No error should be recorded
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)
        # Variable should be updated to the new scope
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 20)

    def test_initializes_symbol_table_fields_if_missing(self):
        """Test that function initializes missing symbol_table fields."""
        node: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {}

        _handle_variable_declaration(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("current_scope", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["errors"], [])

    def test_processes_children_initialization_expression(self):
        """Test that initialization expression children are processed."""
        child_node: AST = {
            "type": "expression",
            "value": 42,
            "children": []
        }
        node: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [child_node]
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }
        
        # Create a mock for _traverse_node
        mock_traverse = MagicMock()
        # Patch the _get_traverse_node function to return our mock
        with patch.object(_handle_variable_declaration_src, '_get_traverse_node', return_value=mock_traverse):
            _handle_variable_declaration(node, symbol_table)
            mock_traverse.assert_called_once_with(child_node, symbol_table)

    def test_does_not_process_empty_children(self):
        """Test that empty children list does not trigger traverse_node call."""
        node: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }
        
        mock_traverse = MagicMock()
        with patch.object(_handle_variable_declaration_src, '_get_traverse_node', return_value=mock_traverse):
            _handle_variable_declaration(node, symbol_table)
            mock_traverse.assert_not_called()

    def test_does_not_process_missing_children_key(self):
        """Test that missing children key does not trigger traverse_node call."""
        node: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }
        
        mock_traverse = MagicMock()
        with patch.object(_handle_variable_declaration_src, '_get_traverse_node', return_value=mock_traverse):
            _handle_variable_declaration(node, symbol_table)
            mock_traverse.assert_not_called()

    def test_multiple_errors_accumulated(self):
        """Test that multiple redefinition errors are accumulated."""
        node1: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        node2: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 15,
            "column": 8,
            "children": []
        }
        node3: AST = {
            "type": "variable_declaration",
            "value": "x",
            "data_type": "int",
            "line": 20,
            "column": 12,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }

        _handle_variable_declaration(node1, symbol_table)
        _handle_variable_declaration(node2, symbol_table)
        _handle_variable_declaration(node3, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["line"], 15)
        self.assertEqual(symbol_table["errors"][1]["line"], 20)

    def test_preserves_existing_symbol_table_data(self):
        """Test that existing symbol_table data is preserved."""
        node: AST = {
            "type": "variable_declaration",
            "value": "y",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_scope": 2,
            "variables": {"x": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 1}},
            "functions": {"main": {"return_type": "int"}},
            "errors": [{"message": "pre-existing error"}]
        }

        _handle_variable_declaration(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["functions"]["main"]["return_type"], "int")
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "pre-existing error")


if __name__ == "__main__":
    unittest.main()
