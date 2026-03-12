#!/usr/bin/env python3
"""Unit tests for _handle_block function."""

import sys
import unittest
from unittest.mock import patch, call, MagicMock

# Register mock module in sys.modules before importing _handle_block
# This bypasses the circular import issue in _traverse_node_src
_mock_traverse_node_module = MagicMock()
_mock_traverse_node = MagicMock()
_mock_traverse_node_module._traverse_node = _mock_traverse_node
sys.modules['main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._traverse_node_src'] = _mock_traverse_node_module

# Relative imports from the same package
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""

    def test_handle_block_with_children(self):
        """Test block processing with child nodes."""
        node = {
            "type": "block",
            "children": [
                {"type": "statement", "value": "stmt1"},
                {"type": "statement", "value": "stmt2"},
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        # Reset mock call history
        _mock_traverse_node.reset_mock()
        
        _handle_block(node, symbol_table)
        
        # Verify scope changes: enter block (0->1), process children, exit block (1->0)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [0])
        
        # Verify _traverse_node called for each child
        self.assertEqual(_mock_traverse_node.call_count, 2)
        _mock_traverse_node.assert_has_calls([
            call({"type": "statement", "value": "stmt1"}, symbol_table),
            call({"type": "statement", "value": "stmt2"}, symbol_table),
        ])
            _handle_block(node, symbol_table)
            
            # Verify scope changes: enter block (0->1), process children, exit block (1->0)
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [0])
            
            # Verify _traverse_node called for each child
            self.assertEqual(mock_traverse_node.call_count, 2)
            mock_traverse_node.assert_has_calls([
                call({"type": "statement", "value": "stmt1"}, symbol_table),
                call({"type": "statement", "value": "stmt2"}, symbol_table),
            ])

    def test_handle_block_empty_children(self):
        """Test block processing with no children."""
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse_node:
            _handle_block(node, symbol_table)
            
            # Verify scope changes: enter block (0->1), no children, exit block (1->0)
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [0])
            
            # Verify _traverse_node not called
            mock_traverse_node.assert_not_called()

    def test_handle_block_nested_scope_level(self):
        """Test block processing when already in nested scope."""
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse_node:
            _handle_block(node, symbol_table)
            
            # Verify scope changes: enter block (1->2), no children, exit block (2->1)
            self.assertEqual(symbol_table["current_scope"], 1)
            self.assertEqual(symbol_table["scope_stack"], [0, 1])
            
            mock_traverse_node.assert_not_called()

    def test_handle_block_first_block_empty_stack(self):
        """Test first block when scope_stack is initially empty."""
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse_node:
            _handle_block(node, symbol_table)
            
            # After entering and leaving block with empty initial stack
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])
            
            mock_traverse_node.assert_not_called()

    def test_handle_block_missing_children_key(self):
        """Test block with missing children key (uses default empty list)."""
        node = {
            "type": "block"
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse_node:
            _handle_block(node, symbol_table)
            
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [0])
            
            mock_traverse_node.assert_not_called()

    def test_handle_block_multiple_children(self):
        """Test block with multiple child nodes."""
        node = {
            "type": "block",
            "children": [
                {"type": "declaration", "value": "var1"},
                {"type": "assignment", "value": "var2"},
                {"type": "expression", "value": "expr1"},
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse_node:
            _handle_block(node, symbol_table)
            
            self.assertEqual(symbol_table["current_scope"], 1)
            self.assertEqual(symbol_table["scope_stack"], [0, 1])
            
            self.assertEqual(mock_traverse_node.call_count, 3)

    def test_handle_block_deeply_nested_scopes(self):
        """Test block processing with deeply nested scope levels."""
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": [0, 1, 2, 3, 4, 5]
        }
        
        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse_node:
            _handle_block(node, symbol_table)
            
            # Verify scope restored correctly after deep nesting
            self.assertEqual(symbol_table["current_scope"], 5)
            self.assertEqual(symbol_table["scope_stack"], [0, 1, 2, 3, 4, 5])
            
            mock_traverse_node.assert_not_called()


if __name__ == "__main__":
    unittest.main()
