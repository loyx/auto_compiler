import unittest
from unittest.mock import patch


class TestTraverseNode(unittest.TestCase):
    """Tests for _traverse_node function."""

    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    @patch('_traverse_node_src._handle_if')
    def test_dispatch_if_node(self, mock_handle_if):
        """Test that if nodes are dispatched to _handle_if."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "if",
            "line": 1,
            "column": 0,
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_if.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_while')
    def test_dispatch_while_node(self, mock_handle_while):
        """Test that while nodes are dispatched to _handle_while."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "while",
            "line": 2,
            "column": 0,
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_while.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_block')
    def test_dispatch_block_node(self, mock_handle_block):
        """Test that block nodes are dispatched to _handle_block."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "block",
            "line": 3,
            "column": 0,
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_block.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_var_decl')
    def test_dispatch_var_decl_node(self, mock_handle_var_decl):
        """Test that var_decl nodes are dispatched to _handle_var_decl."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "var_decl",
            "line": 4,
            "column": 0,
            "value": "x",
            "data_type": "int"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_var_decl.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_assignment')
    def test_dispatch_assignment_node(self, mock_handle_assignment):
        """Test that assignment nodes are dispatched to _handle_assignment."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "assignment",
            "line": 5,
            "column": 0,
            "value": "x",
            "data_type": "int"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_assignment.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_function_call')
    def test_dispatch_function_call_node(self, mock_handle_function_call):
        """Test that function_call nodes are dispatched to _handle_function_call."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "function_call",
            "line": 6,
            "column": 0,
            "value": "print"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_function_call.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_function_decl')
    def test_dispatch_function_decl_node(self, mock_handle_function_decl):
        """Test that function_decl nodes are dispatched to _handle_function_decl."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "function_decl",
            "line": 7,
            "column": 0,
            "value": "main"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_function_decl.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_return')
    def test_dispatch_return_node(self, mock_handle_return):
        """Test that return nodes are dispatched to _handle_return."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "return",
            "line": 8,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_return.assert_called_once_with(node, self.symbol_table)

    @patch('_traverse_node_src._handle_if')
    @patch('_traverse_node_src._handle_while')
    @patch('_traverse_node_src._handle_block')
    @patch('_traverse_node_src._handle_var_decl')
    @patch('_traverse_node_src._handle_assignment')
    @patch('_traverse_node_src._handle_function_call')
    @patch('_traverse_node_src._handle_function_decl')
    @patch('_traverse_node_src._handle_return')
    def test_unknown_type_recurse_children(self, mock_return, mock_func_decl, mock_func_call, 
                                             mock_assignment, mock_var_decl, mock_block,
                                             mock_while, mock_if):
        """Test that unknown node types recursively process children."""
        from ._traverse_node_src import _traverse_node
        
        child1 = {"type": "var_decl", "line": 1, "column": 0}
        child2 = {"type": "assignment", "line": 2, "column": 0}
        node = {
            "type": "unknown_type",
            "children": [child1, child2]
        }
        
        _traverse_node(node, self.symbol_table)
        
        # Should NOT call any handler for unknown type
        mock_if.assert_not_called()
        mock_while.assert_not_called()
        mock_block.assert_not_called()
        mock_var_decl.assert_not_called()
        mock_assignment.assert_not_called()
        mock_func_call.assert_not_called()
        mock_func_decl.assert_not_called()
        mock_return.assert_not_called()

    @patch('_traverse_node_src._handle_var_decl')
    def test_node_without_type_field(self, mock_handle_var_decl):
        """Test handling of node without type field defaults to unknown type."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "line": 1,
            "column": 0,
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        # Should not call any specific handler
        mock_handle_var_decl.assert_not_called()

    @patch('_traverse_node_src._handle_var_decl')
    def test_empty_children_list(self, mock_handle_var_decl):
        """Test that empty children list is handled correctly."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "unknown",
            "children": []
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_var_decl.assert_not_called()

    @patch('_traverse_node_src._handle_var_decl')
    def test_missing_children_field(self, mock_handle_var_decl):
        """Test that missing children field defaults to empty list."""
        from ._traverse_node_src import _traverse_node
        
        node = {
            "type": "unknown",
            "line": 1,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handle_var_decl.assert_not_called()

    @patch('_traverse_node_src._handle_if')
    def test_handler_exception_propagation(self, mock_handle_if):
        """Test that exceptions from handlers propagate correctly."""
        from ._traverse_node_src import _traverse_node
        
        node = {"type": "if", "line": 1, "column": 0}
        mock_handle_if.side_effect = ValueError("Test error")
        
        with self.assertRaises(ValueError):
            _traverse_node(node, self.symbol_table)

    @patch('_traverse_node_src._handle_var_decl')
    @patch('_traverse_node_src._handle_assignment')
    def test_nested_unknown_types(self, mock_assignment, mock_var_decl):
        """Test recursive traversal of nested unknown types."""
        from ._traverse_node_src import _traverse_node
        
        grandchild = {"type": "var_decl", "line": 3, "column": 0}
        child = {
            "type": "unknown1",
            "children": [grandchild]
        }
        node = {
            "type": "unknown2",
            "children": [child]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_var_decl.assert_called_once_with(grandchild, self.symbol_table)
        mock_assignment.assert_not_called()

    @patch('_traverse_node_src._traverse_node')
    @patch('_traverse_node_src._handle_var_decl')
    def test_recursive_call_invocation(self, mock_handle_var_decl, mock_traverse):
        """Test that recursive calls are made for children of unknown types."""
        from ._traverse_node_src import _traverse_node
        
        child = {"type": "var_decl", "line": 1, "column": 0}
        node = {
            "type": "unknown",
            "children": [child]
        }
        
        # Mock the recursive call to avoid infinite recursion
        mock_traverse.side_effect = lambda n, st: None
        
        _traverse_node(node, self.symbol_table)
        
        # Verify recursive call was made for the child
        mock_traverse.assert_called_once_with(child, self.symbol_table)

    @patch('_traverse_node_src._handle_if')
    @patch('_traverse_node_src._handle_while')
    def test_multiple_children_processed(self, mock_while, mock_if):
        """Test that multiple children are all processed."""
        from ._traverse_node_src import _traverse_node
        
        child1 = {"type": "if", "line": 1, "column": 0}
        child2 = {"type": "while", "line": 2, "column": 0}
        node = {
            "type": "unknown",
            "children": [child1, child2]
        }
        
        _traverse_node(node, self.symbol_table)
        
        # Both handlers should be called
        self.assertEqual(mock_if.call_count, 1)
        self.assertEqual(mock_while.call_count, 1)
        mock_if.assert_called_with(child1, self.symbol_table)
        mock_while.assert_called_with(child2, self.symbol_table)

    def test_symbol_table_not_modified_for_known_types(self):
        """Test that symbol_table is not directly modified by _traverse_node for known types."""
        from ._traverse_node_src import _traverse_node
        
        original_errors = []
        self.symbol_table["errors"] = original_errors
        
        node = {"type": "if", "line": 1, "column": 0}
        
        with patch('_traverse_node_src._handle_if') as mock_handle_if:
            _traverse_node(node, self.symbol_table)
        
        # _traverse_node itself should not modify errors list
        self.assertIs(self.symbol_table["errors"], original_errors)

    def test_empty_node(self):
        """Test handling of completely empty node."""
        from ._traverse_node_src import _traverse_node
        
        node = {}
        
        with patch('_traverse_node_src._handle_var_decl') as mock_var_decl:
            _traverse_node(node, self.symbol_table)
            
            # Empty node has type "" which is unknown, should not call handlers
            mock_var_decl.assert_not_called()


if __name__ == '__main__':
    unittest.main()
