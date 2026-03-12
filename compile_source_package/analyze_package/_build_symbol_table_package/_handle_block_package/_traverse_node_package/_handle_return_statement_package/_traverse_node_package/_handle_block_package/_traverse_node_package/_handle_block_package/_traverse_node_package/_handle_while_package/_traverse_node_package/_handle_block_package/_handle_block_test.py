import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """Tests for _handle_block function"""
    
    def test_empty_block(self):
        """Test handling of empty block with no children"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_block(node, symbol_table)
        
        # Scope should be entered (0->1) then exited (1->0)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_block_with_children(self):
        """Test handling of block with child nodes"""
        child1 = {"type": "var_decl", "name": "x"}
        child2 = {"type": "assignment", "name": "y"}
        node = {"type": "block", "children": [child1, child2]}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)
            
            # Verify _traverse_node was called for each child
            self.assertEqual(mock_traverse.call_count, 2)
            mock_traverse.assert_any_call(child1, symbol_table)
            mock_traverse.assert_any_call(child2, symbol_table)
            
            # Scope should be restored after block
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_scope_management_increment_and_restore(self):
        """Test that scope is properly entered and exited"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 5,
            "scope_stack": [1, 2, 3]
        }
        
        _handle_block(node, symbol_table)
        
        # Scope should be incremented (5->6) then restored to 5
        self.assertEqual(symbol_table["current_scope"], 5)
        # Old scope (5) was pushed, then popped
        self.assertEqual(symbol_table["scope_stack"], [1, 2, 3])
    
    def test_nested_blocks_via_traverse(self):
        """Test handling of nested blocks through _traverse_node"""
        inner_block = {"type": "block", "children": []}
        outer_block = {"type": "block", "children": [inner_block]}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(outer_block, symbol_table)
            
            # _traverse_node should be called for the inner block
            self.assertEqual(mock_traverse.call_count, 1)
            mock_traverse.assert_called_with(inner_block, symbol_table)
            
            # Scope should be restored after outer block completes
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_error_handling_no_exception_thrown(self):
        """Test that errors in children are recorded, not thrown"""
        node = {"type": "block", "children": [{"type": "var_decl"}]}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        # Even if _traverse_node raises an error, _handle_block should not throw
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            mock_traverse.side_effect = Exception("Test error in child")
            
            # Should not raise exception
            _handle_block(node, symbol_table)
            
            # Scope should still be restored despite error
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_missing_scope_fields_initialized(self):
        """Test handling when scope fields are missing from symbol_table"""
        node = {"type": "block", "children": []}
        symbol_table = {}
        
        _handle_block(node, symbol_table)
        
        # Should initialize missing fields via setdefault
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_scope_stack_operations_detailed(self):
        """Test that scope_stack is properly managed with push/pop"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 3,
            "scope_stack": [1, 2]
        }
        
        _handle_block(node, symbol_table)
        
        # Old scope (3) should be pushed, then popped, restoring to 3
        self.assertEqual(symbol_table["current_scope"], 3)
        self.assertEqual(symbol_table["scope_stack"], [1, 2])
    
    def test_multiple_children_order_preserved(self):
        """Test that children are processed in order"""
        child1 = {"type": "var_decl", "name": "x", "order": 1}
        child2 = {"type": "assignment", "name": "y", "order": 2}
        child3 = {"type": "return", "order": 3}
        node = {"type": "block", "children": [child1, child2, child3]}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)
            
            # Verify calls were made in order
            calls = mock_traverse.call_args_list
            self.assertEqual(len(calls), 3)
            self.assertEqual(calls[0][0][0], child1)
            self.assertEqual(calls[1][0][0], child2)
            self.assertEqual(calls[2][0][0], child3)
    
    def test_block_without_children_key(self):
        """Test handling when 'children' key is missing from node"""
        node = {"type": "block"}  # No children key
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_block(node, symbol_table)
        
        # Should use default empty list for missing children
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_scope_stack_empty_pop_safety(self):
        """Test that empty scope_stack is handled safely"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_block(node, symbol_table)
        
        # Should not fail when scope_stack is empty after pop
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_complex_block_with_mixed_children(self):
        """Test block with various types of child nodes"""
        children = [
            {"type": "var_decl", "name": "x", "data_type": "int"},
            {"type": "assignment", "name": "x", "value": 5},
            {"type": "if", "condition": "x > 0", "children": []},
            {"type": "while", "condition": "x < 10", "children": []},
            {"type": "return", "value": "x"}
        ]
        node = {"type": "block", "children": children}
        symbol_table = {
            "current_scope": 1,
            "scope_stack": [0],
            "variables": {},
            "errors": []
        }
        
        with patch('._traverse_node_package._traverse_node_src._traverse_node') as mock_traverse:
            _handle_block(node, symbol_table)
            
            # All children should be traversed
            self.assertEqual(mock_traverse.call_count, 5)
            
            # Scope should be restored
            self.assertEqual(symbol_table["current_scope"], 1)
            self.assertEqual(symbol_table["scope_stack"], [0])


if __name__ == '__main__':
    unittest.main()
