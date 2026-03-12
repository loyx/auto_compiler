# -*- coding: utf-8 -*-
"""
Unit tests for _handle_identifier function.
Tests the leaf node handler for identifier AST nodes.
"""

import unittest

# Relative import from the same package
from ._handle_identifier_src import _handle_identifier, AST, SymbolTable


class TestHandleIdentifier(unittest.TestCase):
    """Test cases for _handle_identifier function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int", "scope": 0}},
            "functions": {"foo": {"params": [], "scope": 0}},
            "current_scope": 0,
            "scope_stack": [0]
        }

    def test_handle_identifier_valid_node(self) -> None:
        """Test handling a valid identifier node with name field."""
        node: AST = {"type": "identifier", "name": "x"}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()
        symbol_table["scope_stack"] = self.base_symbol_table["scope_stack"].copy()

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified (stub behavior)
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_handle_identifier_empty_name(self) -> None:
        """Test handling identifier node with empty name."""
        node: AST = {"type": "identifier", "name": ""}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])

    def test_handle_identifier_missing_name_field(self) -> None:
        """Test handling identifier node without name field."""
        node: AST = {"type": "identifier"}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()

        # Should not raise any exception (uses .get() with default)
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])

    def test_handle_identifier_undefined_variable(self) -> None:
        """Test handling identifier that is not in symbol table."""
        node: AST = {"type": "identifier", "name": "undefined_var"}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()

        # Should not raise any exception (stub doesn't validate)
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])

    def test_handle_identifier_function_name(self) -> None:
        """Test handling identifier that matches a function name."""
        node: AST = {"type": "identifier", "name": "foo"}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["functions"] = self.base_symbol_table["functions"].copy()

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["functions"], self.base_symbol_table["functions"])

    def test_handle_identifier_special_characters(self) -> None:
        """Test handling identifier with special characters in name."""
        node: AST = {"type": "identifier", "name": "_private_var"}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])

    def test_handle_identifier_unicode_name(self) -> None:
        """Test handling identifier with unicode characters."""
        node: AST = {"type": "identifier", "name": "变量"}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])

    def test_handle_identifier_empty_symbol_table(self) -> None:
        """Test handling identifier with minimal/empty symbol table."""
        node: AST = {"type": "identifier", "name": "x"}
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table structure is preserved
        self.assertEqual(symbol_table["variables"], {})
        self.assertEqual(symbol_table["functions"], {})

    def test_handle_identifier_nested_scope(self) -> None:
        """Test handling identifier in nested scope context."""
        node: AST = {"type": "identifier", "name": "y"}
        symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int", "scope": 0}, "y": {"type": "str", "scope": 1}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(len(symbol_table["scope_stack"]), 2)

    def test_handle_identifier_node_with_extra_fields(self) -> None:
        """Test handling identifier node with additional AST fields."""
        node: AST = {
            "type": "identifier",
            "name": "x",
            "line": 10,
            "column": 5,
            "metadata": {"resolved": False}
        }
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()

        # Should not raise any exception
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is not modified
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])

    def test_handle_identifier_multiple_calls_idempotent(self) -> None:
        """Test that multiple calls to _handle_identifier don't accumulate side effects."""
        node: AST = {"type": "identifier", "name": "x"}
        symbol_table: SymbolTable = self.base_symbol_table.copy()
        symbol_table["variables"] = self.base_symbol_table["variables"].copy()
        symbol_table["scope_stack"] = self.base_symbol_table["scope_stack"].copy()

        # Call multiple times
        _handle_identifier(node, symbol_table)
        _handle_identifier(node, symbol_table)
        _handle_identifier(node, symbol_table)

        # Verify symbol_table is still unchanged
        self.assertEqual(symbol_table["variables"], self.base_symbol_table["variables"])
        self.assertEqual(symbol_table["scope_stack"], self.base_symbol_table["scope_stack"])


if __name__ == "__main__":
    unittest.main()
