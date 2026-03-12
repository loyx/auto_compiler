import unittest
from unittest.mock import patch, call

# Import the function under test using relative import
from ._traverse_node_src import _traverse_node


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    def test_none_node_silently_returns(self):
        """Test that None node is silently skipped."""
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        # Should not raise any exception
        result = _traverse_node(None, symbol_table)
        self.assertIsNone(result)
    
    def test_empty_dict_node_silently_returns(self):
        """Test that empty dict node is silently skipped."""
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        result = _traverse_node({}, symbol_table)
        self.assertIsNone(result)
    
    def test_missing_type_field_silently_returns(self):
        """Test that node without type field is silently skipped."""
        node = {"children": []}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)
    
    def test_non_string_type_silently_returns(self):
        """Test that node with non-string type is silently skipped."""
        node = {"type": 123}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)
    
    def test_empty_type_string_silently_returns(self):
        """Test that node with empty string type is silently skipped."""
        node = {"type": ""}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        result = _traverse_node(node, symbol_table)
        self.assertIsNone(result)
    
    @patch('_traverse_node_src._handle_block')
    def test_block_node_calls_handler(self, mock_handle_block):
        """Test that block node calls _handle_block handler."""
        node = {"type": "block", "children": []}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        mock_handle_block.assert_called_once_with(node, symbol_table)
    
    @patch('_traverse_node_src._handle_declaration')
    def test_declaration_node_calls_handler(self, mock_handle_declaration):
        """Test that declaration node calls _handle_declaration handler."""
        node = {"type": "declaration", "data_type": "int", "value": 10}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        mock_handle_declaration.assert_called_once_with(node, symbol_table)
    
    @patch('_traverse_node_src._handle_assignment')
    def test_assignment_node_calls_handler(self, mock_handle_assignment):
        """Test that assignment node calls _handle_assignment handler."""
        node = {"type": "assignment", "value": 42}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        mock_handle_assignment.assert_called_once_with(node, symbol_table)
    
    @patch('_traverse_node_src._handle_expression')
    def test_expression_node_calls_handler(self, mock_handle_expression):
        """Test that expression node calls _handle_expression handler."""
        node = {"type": "expression", "value": "x + 1"}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        mock_handle_expression.assert_called_once_with(node, symbol_table)
    
    @patch('_traverse_node_src._handle_block')
    @patch('_traverse_node_src._handle_declaration')
    @patch('_traverse_node_src._handle_assignment')
    @patch('_traverse_node_src._handle_expression')
    def test_unknown_type_with_children_traverses_children(
        self, mock_handle_expression, mock_handle_assignment, 
        mock_handle_declaration, mock_handle_block
    ):
        """Test that unknown node type with children recursively traverses children."""
        child1 = {"type": "declaration", "data_type": "int"}
        child2 = {"type": "assignment", "value": 10}
        node = {"type": "unknown_type", "children": [child1, child2]}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Unknown type handler should not be called
        mock_handle_block.assert_not_called()
        # Children should be traversed
        mock_handle_declaration.assert_called_once_with(child1, symbol_table)
        mock_handle_assignment.assert_called_once_with(child2, symbol_table)
        mock_handle_expression.assert_not_called()
    
    @patch('_traverse_node_src._handle_block')
    @patch('_traverse_node_src._handle_declaration')
    @patch('_traverse_node_src._handle_assignment')
    @patch('_traverse_node_src._handle_expression')
    def test_unknown_type_without_children_silently_skips(
        self, mock_handle_expression, mock_handle_assignment, 
        mock_handle_declaration, mock_handle_block
    ):
        """Test that unknown node type without children is silently skipped."""
        node = {"type": "unknown_type"}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        result = _traverse_node(node, symbol_table)
        
        self.assertIsNone(result)
        # No handlers should be called
        mock_handle_block.assert_not_called()
        mock_handle_declaration.assert_not_called()
        mock_handle_assignment.assert_not_called()
        mock_handle_expression.assert_not_called()
    
    @patch('_traverse_node_src._handle_block')
    def test_block_node_with_full_attributes(self, mock_handle_block):
        """Test block node with all possible attributes."""
        node = {
            "type": "block",
            "children": [
                {"type": "declaration", "data_type": "int"},
                {"type": "assignment", "value": 5}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        mock_handle_block.assert_called_once_with(node, symbol_table)
    
    @patch('_traverse_node_src._handle_block')
    def test_multiple_block_nodes_sequential(self, mock_handle_block):
        """Test multiple block nodes processed sequentially."""
        node1 = {"type": "block", "children": []}
        node2 = {"type": "block", "children": []}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node1, symbol_table)
        _traverse_node(node2, symbol_table)
        
        self.assertEqual(mock_handle_block.call_count, 2)
        mock_handle_block.assert_has_calls([
            call(node1, symbol_table),
            call(node2, symbol_table)
        ])
    
    @patch('_traverse_node_src._handle_block')
    def test_nested_block_nodes(self, mock_handle_block):
        """Test nested block nodes structure."""
        inner_block = {"type": "block", "children": []}
        outer_block = {"type": "block", "children": [inner_block]}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(outer_block, symbol_table)
        
        # Only outer block handler is called directly
        # Inner block would be handled by _handle_block recursively
        mock_handle_block.assert_called_once_with(outer_block, symbol_table)
    
    @patch('_traverse_node_src._handle_block')
    @patch('_traverse_node_src._handle_declaration')
    @patch('_traverse_node_src._handle_assignment')
    @patch('_traverse_node_src._handle_expression')
    def test_all_known_node_types(self, mock_handle_expression, mock_handle_assignment, 
                                   mock_handle_declaration, mock_handle_block):
        """Test all known node types are dispatched correctly."""
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        block_node = {"type": "block", "children": []}
        decl_node = {"type": "declaration", "data_type": "int"}
        assign_node = {"type": "assignment", "value": 10}
        expr_node = {"type": "expression", "value": "x"}
        
        _traverse_node(block_node, symbol_table)
        _traverse_node(decl_node, symbol_table)
        _traverse_node(assign_node, symbol_table)
        _traverse_node(expr_node, symbol_table)
        
        mock_handle_block.assert_called_once_with(block_node, symbol_table)
        mock_handle_declaration.assert_called_once_with(decl_node, symbol_table)
        mock_handle_assignment.assert_called_once_with(assign_node, symbol_table)
        mock_handle_expression.assert_called_once_with(expr_node, symbol_table)
    
    @patch('_traverse_node_src._handle_block')
    @patch('_traverse_node_src._handle_declaration')
    @patch('_traverse_node_src._handle_assignment')
    @patch('_traverse_node_src._handle_expression')
    def test_children_with_mixed_known_unknown_types(
        self, mock_handle_expression, mock_handle_assignment, 
        mock_handle_declaration, mock_handle_block
    ):
        """Test children with mixed known and unknown types."""
        known_child = {"type": "declaration", "data_type": "char"}
        unknown_child = {"type": "weird_type", "children": []}
        node = {"type": "unknown_parent", "children": [known_child, unknown_child]}
        symbol_table = self.sample_symbol_table.copy()
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Known child should be handled
        mock_handle_declaration.assert_called_once_with(known_child, symbol_table)
        # Unknown children should be silently skipped
        mock_handle_block.assert_not_called()
        mock_handle_assignment.assert_not_called()
        mock_handle_expression.assert_not_called()


if __name__ == '__main__':
    unittest.main()
