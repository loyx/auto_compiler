import unittest
from unittest.mock import patch, call

# Import the function under test using relative import
from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function"""
    
    def test_handle_block_empty_block(self):
        """Test handling a block with no children"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_block(node, symbol_table)
        
        # Scope should return to original value after block
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_with_children(self):
        """Test handling a block with children nodes"""
        node = {
            "type": "block",
            "children": [
                {"type": "statement", "value": "stmt1"},
                {"type": "statement", "value": "stmt2"}
            ]
        }
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            # Verify _traverse_node was called for each child
            self.assertEqual(mock_traverse.call_count, 2)
            # Scope should return to original value
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_scope_increment_during_execution(self):
        """Test that scope is incremented during block execution"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 2,
            "scope_stack": []
        }
        
        _handle_block(node, symbol_table)
        
        # After block, scope should return to original value (2)
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_missing_scope_stack(self):
        """Test handling when scope_stack doesn't exist"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_block(node, symbol_table)
        
        # scope_stack should be created and empty after
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_missing_current_scope(self):
        """Test handling when current_scope doesn't exist"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "scope_stack": []
        }
        
        _handle_block(node, symbol_table)
        
        # current_scope should be created and be 0 after
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_missing_both_fields(self):
        """Test handling when both scope_stack and current_scope don't exist"""
        node = {"type": "block", "children": []}
        symbol_table = {}
        
        _handle_block(node, symbol_table)
        
        # Both fields should be created with proper values
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_nested_scopes(self):
        """Test handling nested blocks with pre-existing scope stack"""
        node = {"type": "block", "children": []}
        symbol_table = {
            "current_scope": 2,
            "scope_stack": [0, 1]  # Pre-existing stack
        }
        
        _handle_block(node, symbol_table)
        
        # Should restore to previous scope (1)
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [0])
    
    def test_handle_block_traverse_node_called_with_correct_args(self):
        """Test that _traverse_node is called with correct arguments"""
        child1 = {"type": "statement", "value": "stmt1"}
        child2 = {"type": "expression", "value": "expr1"}
        node = {
            "type": "block",
            "children": [child1, child2]
        }
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            # Verify calls with correct arguments
            expected_calls = [
                call(child1, symbol_table),
                call(child2, symbol_table)
            ]
            mock_traverse.assert_has_calls(expected_calls)
    
    def test_handle_block_traverse_node_called_with_same_symbol_table(self):
        """Test that _traverse_node receives the same symbol_table reference"""
        child = {"type": "statement", "value": "stmt1"}
        node = {
            "type": "block",
            "children": [child]
        }
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            # Verify the same symbol_table object is passed
            mock_traverse.assert_called_once_with(child, symbol_table)
            # Verify it's the same object reference
            called_symbol_table = mock_traverse.call_args[0][1]
            self.assertIs(called_symbol_table, symbol_table)
    
    def test_handle_block_scope_stack_operations(self):
        """Test that scope stack operations happen in correct order"""
        child = {"type": "statement", "value": "stmt1"}
        node = {
            "type": "block",
            "children": [child]
        }
        symbol_table = {
            "current_scope": 5,
            "scope_stack": [1, 2, 3]
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            # Track scope values during execution
            original_scope = symbol_table["current_scope"]
            
            _handle_block(node, symbol_table)
            
            # Verify stack operations: push original, then pop to restore
            # Before: scope=5, stack=[1,2,3]
            # During: scope=6, stack=[1,2,3,5]
            # After: scope=5, stack=[1,2,3]
            self.assertEqual(symbol_table["current_scope"], original_scope)
            self.assertEqual(symbol_table["scope_stack"], [1, 2, 3])
    
    def test_handle_block_no_children_key(self):
        """Test handling when 'children' key is missing from node"""
        node = {"type": "block"}
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_block(node, symbol_table)
        
        # Should handle missing children gracefully (default to empty list)
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_handle_block_multiple_children(self):
        """Test handling block with multiple children"""
        children = [{"type": "stmt", "id": i} for i in range(5)]
        node = {
            "type": "block",
            "children": children
        }
        symbol_table = {
            "current_scope": 0,
            "scope_stack": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            # Verify _traverse_node was called for each child
            self.assertEqual(mock_traverse.call_count, 5)


if __name__ == '__main__':
    unittest.main()
