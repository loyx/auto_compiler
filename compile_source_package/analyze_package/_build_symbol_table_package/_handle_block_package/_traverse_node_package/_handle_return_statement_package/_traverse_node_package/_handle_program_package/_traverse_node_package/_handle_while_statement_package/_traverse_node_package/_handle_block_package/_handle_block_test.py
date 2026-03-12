#!/usr/bin/env python3
"""
Unit tests for _handle_block function.
"""

import unittest
from unittest.mock import patch, call

# Relative import for the function under test
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""
    
    def test_handle_block_normal_with_children(self):
        """Test handling a normal block with children nodes."""
        # Setup
        node = {
            "type": "block",
            "children": [
                {"type": "statement1", "value": "stmt1"},
                {"type": "statement2", "value": "stmt2"},
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        # Mock _traverse_node where it's used (in _handle_block_src module)
        with patch("._handle_block_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # Execute
            _handle_block(node, symbol_table)
            
            # Verify scope changes - should return to original
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])
            
            # Verify _traverse_node was called for each child
            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_has_calls([
                call({"type": "statement1", "value": "stmt1"}, symbol_table),
                call({"type": "statement2", "value": "stmt2"}, symbol_table),
            ])
    
    def test_handle_block_empty_block(self):
        """Test handling an empty block with no children."""
        # Setup
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        # Execute
        _handle_block(node, symbol_table)
        
        # Verify scope changes - should return to original
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_missing_children_key(self):
        """Test handling a block node without a children key."""
        # Setup
        node = {
            "type": "block"
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        # Execute
        _handle_block(node, symbol_table)
        
        # Verify scope changes - should return to original
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_existing_scope(self):
        """Test handling a block when already in a non-zero scope."""
        # Setup
        node = {
            "type": "block",
            "children": [{"type": "statement"}]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 2,
            "scope_stack": [1, 2],
            "current_function": None,
            "errors": []
        }
        
        # Mock _traverse_node
        with patch("._handle_block_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # Execute
            _handle_block(node, symbol_table)
            
            # Verify scope changes - should return to original
            self.assertEqual(symbol_table["current_scope"], 2)
            self.assertEqual(symbol_table["scope_stack"], [1, 2])
            
            # Verify _traverse_node was called
            mock_traverse.assert_called_once()
    
    def test_handle_block_scope_management_during_execution(self):
        """Test that scope is properly managed during block execution."""
        # Setup
        node = {
            "type": "block",
            "children": [{"type": "statement"}]
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
        
        # Mock _traverse_node to capture scope state during execution
        def capture_scope(child, st):
            # During execution, scope should be incremented
            self.assertEqual(st["current_scope"], 1)
            self.assertEqual(st["scope_stack"], [1])
        
        with patch("._handle_block_package._traverse_node_package._traverse_node_src._traverse_node", side_effect=capture_scope):
            # Execute
            _handle_block(node, symbol_table)
            
            # After execution, scope should be back to original
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_deeply_nested_scope(self):
        """Test handling a block when starting from a deeply nested scope."""
        # Setup
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 5,
            "scope_stack": [1, 2, 3, 4, 5],
            "current_function": None,
            "errors": []
        }
        
        # Execute
        _handle_block(node, symbol_table)
        
        # Verify scope changes - should return to original
        self.assertEqual(symbol_table["current_scope"], 5)
        self.assertEqual(symbol_table["scope_stack"], [1, 2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
