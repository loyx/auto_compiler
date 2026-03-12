# -*- coding: utf-8 -*-
"""
Unit tests for _handle_block function.
"""

import unittest
from typing import Any, Dict

# Relative import from the same package
from ._handle_block_src import _handle_block

# Type aliases for test clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""

    def _create_symbol_table(self) -> SymbolTable:
        """Helper to create a minimal symbol table for tests."""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_empty_block_returns_void(self):
        """Test that an empty block (no children) returns 'void'."""
        node: AST = {
            "type": "block",
            "children": [],
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        
        result = _handle_block(node, symbol_table)
        
        self.assertEqual(result, "void")

    def test_block_with_no_children_key_returns_void(self):
        """Test that a block without 'children' key returns 'void'."""
        node: AST = {
            "type": "block",
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        
        result = _handle_block(node, symbol_table)
        
        self.assertEqual(result, "void")

    def test_single_child_with_data_type(self):
        """Test block with single child returns child's data_type."""
        node: AST = {
            "type": "block",
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 2,
                    "column": 5
                }
            ],
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        
        result = _handle_block(node, symbol_table)
        
        self.assertEqual(result, "int")

    def test_multiple_children_returns_last_type(self):
        """Test block with multiple children returns last child's data_type."""
        node: AST = {
            "type": "block",
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 2,
                    "column": 5
                },
                {
                    "type": "expression",
                    "data_type": "string",
                    "line": 3,
                    "column": 5
                },
                {
                    "type": "expression",
                    "data_type": "float",
                    "line": 4,
                    "column": 5
                }
            ],
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        
        result = _handle_block(node, symbol_table)
        
        self.assertEqual(result, "float")

    def test_child_without_data_type_returns_void(self):
        """Test that child without data_type field returns 'void'."""
        node: AST = {
            "type": "block",
            "children": [
                {
                    "type": "expression",
                    "line": 2,
                    "column": 5
                    # No data_type field
                }
            ],
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        
        result = _handle_block(node, symbol_table)
        
        self.assertEqual(result, "void")

    def test_mixed_children_last_without_type_returns_void(self):
        """Test block where last child has no data_type returns 'void'."""
        node: AST = {
            "type": "block",
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 2,
                    "column": 5
                },
                {
                    "type": "expression",
                    "line": 3,
                    "column": 5
                    # No data_type field
                }
            ],
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        
        result = _handle_block(node, symbol_table)
        
        self.assertEqual(result, "void")

    def test_symbol_table_not_modified(self):
        """Test that symbol_table is not modified by the function."""
        node: AST = {
            "type": "block",
            "children": [
                {
                    "type": "expression",
                    "data_type": "int",
                    "line": 2,
                    "column": 5
                }
            ],
            "line": 1,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        original_errors_len = len(symbol_table["errors"])
        
        _handle_block(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), original_errors_len)

    def test_various_data_types(self):
        """Test block returns various data types correctly."""
        test_types = ["int", "float", "string", "bool", "void", "array", "object"]
        
        for data_type in test_types:
            with self.subTest(data_type=data_type):
                node: AST = {
                    "type": "block",
                    "children": [
                        {
                            "type": "expression",
                            "data_type": data_type,
                            "line": 2,
                            "column": 5
                        }
                    ],
                    "line": 1,
                    "column": 1
                }
                symbol_table = self._create_symbol_table()
                
                result = _handle_block(node, symbol_table)
                
                self.assertEqual(result, data_type)


if __name__ == "__main__":
    unittest.main()
