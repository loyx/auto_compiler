# -*- coding: utf-8 -*-
"""
Unit tests for _handle_block function.

Tests cover:
- Happy path: normal block handling
- Edge cases: multiple consecutive calls, initial scope values
- Error conditions: missing required keys in symbol_table
"""

import unittest

# Relative import from the same package
from ._handle_block_src import _handle_block, AST, SymbolTable


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.sample_node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 0
        }
        self.sample_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_handle_block_enters_new_scope(self) -> None:
        """Test that _handle_block increments current_scope and updates scope_stack."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        _handle_block(self.sample_node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [1])

    def test_handle_block_multiple_consecutive_calls(self) -> None:
        """Test multiple consecutive _handle_block calls build nested scopes."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        _handle_block(self.sample_node, symbol_table)
        _handle_block(self.sample_node, symbol_table)
        _handle_block(self.sample_node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 3)
        self.assertEqual(symbol_table["scope_stack"], [1, 2, 3])

    def test_handle_block_with_existing_scope(self) -> None:
        """Test _handle_block with non-zero initial scope."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": [1, 2, 3, 4, 5],
            "current_function": None,
            "errors": []
        }
        
        _handle_block(self.sample_node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 6)
        self.assertEqual(symbol_table["scope_stack"], [1, 2, 3, 4, 5, 6])

    def test_handle_block_preserves_other_symbol_table_fields(self) -> None:
        """Test that _handle_block only modifies scope-related fields."""
        symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int", "scope": 1}},
            "functions": {"main": {"return_type": "void"}},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": "main",
            "errors": ["some error"]
        }
        
        _handle_block(self.sample_node, symbol_table)
        
        self.assertEqual(symbol_table["variables"], {"x": {"type": "int", "scope": 1}})
        self.assertEqual(symbol_table["functions"], {"main": {"return_type": "void"}})
        self.assertEqual(symbol_table["current_function"], "main")
        self.assertEqual(symbol_table["errors"], ["some error"])
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [1])

    def test_handle_block_ignores_node_content(self) -> None:
        """Test that _handle_block does not depend on node content."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        different_node: AST = {
            "type": "block",
            "children": [{"type": "statement"}],
            "value": "some_value",
            "line": 10,
            "column": 5
        }
        
        _handle_block(different_node, symbol_table)
        
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [1])

    def test_handle_block_missing_current_scope_raises_keyerror(self) -> None:
        """Test that missing current_scope key raises KeyError."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        with self.assertRaises(KeyError):
            _handle_block(self.sample_node, symbol_table)

    def test_handle_block_missing_scope_stack_raises_keyerror(self) -> None:
        """Test that missing scope_stack key raises KeyError."""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "current_function": None,
            "errors": []
        }
        
        with self.assertRaises(KeyError):
            _handle_block(self.sample_node, symbol_table)

    def test_handle_block_returns_none(self) -> None:
        """Test that _handle_block returns None."""
        result = _handle_block(self.sample_node, self.sample_symbol_table)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
