import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import of the function under test
from ._traverse_node_src import _traverse_node

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""
    
    def _create_empty_symbol_table(self) -> SymbolTable:
        """Helper to create a standard empty symbol table."""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
    
    def test_none_node_returns_early(self):
        """Test that None node causes early return without any handler calls."""
        symbol_table = self._create_empty_symbol_table()
        
        # Should not raise any exception
        _traverse_node(None, symbol_table)
        
        # No assertions needed - just verifying no exception
    
    @patch('._handle_while_package._handle_while_src._handle_while')
    def test_while_node_calls_handler(self, mock_handle_while):
        """Test that while node type dispatches to _handle_while."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "while"}
        _traverse_node(node, symbol_table)
        
        mock_handle_while.assert_called_once_with(node, symbol_table)
    
    @patch('._handle_if_package._handle_if_src._handle_if')
    def test_if_node_calls_handler(self, mock_handle_if):
        """Test that if node type dispatches to _handle_if."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "if"}
        _traverse_node(node, symbol_table)
        
        mock_handle_if.assert_called_once_with(node, symbol_table)
    
    @patch('._handle_block_package._handle_block_src._handle_block')
    def test_block_node_calls_handler(self, mock_handle_block):
        """Test that block node type dispatches to _handle_block."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "block"}
        _traverse_node(node, symbol_table)
        
        mock_handle_block.assert_called_once_with(node, symbol_table)
    
    @patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl')
    def test_var_decl_node_calls_handler(self, mock_handle_var_decl):
        """Test that var_decl node type dispatches to _handle_var_decl."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "var_decl"}
        _traverse_node(node, symbol_table)
        
        mock_handle_var_decl.assert_called_once_with(node, symbol_table)
    
    @patch('._handle_assignment_package._handle_assignment_src._handle_assignment')
    def test_assignment_node_calls_handler(self, mock_handle_assignment):
        """Test that assignment node type dispatches to _handle_assignment."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "assignment"}
        _traverse_node(node, symbol_table)
        
        mock_handle_assignment.assert_called_once_with(node, symbol_table)
    
    @patch('._handle_binary_op_package._handle_binary_op_src._handle_binary_op')
    def test_binary_op_node_calls_handler(self, mock_handle_binary_op):
        """Test that binary_op node type dispatches to _handle_binary_op."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "binary_op"}
        _traverse_node(node, symbol_table)
        
        mock_handle_binary_op.assert_called_once_with(node, symbol_table)
    
    def test_unknown_node_type_ignored(self):
        """Test that unknown node types are silently ignored."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "unknown_type"}
        
        # Should not raise any exception
        _traverse_node(node, symbol_table)
    
    def test_node_without_type_field(self):
        """Test that nodes without 'type' field are handled (defaults to empty string)."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"value": 42}  # No 'type' field
        
        # Should not raise any exception
        _traverse_node(node, symbol_table)
    
    @patch('._handle_while_package._handle_while_src._handle_while')
    @patch('._handle_if_package._handle_if_src._handle_if')
    def test_multiple_node_types(self, mock_handle_if, mock_handle_while):
        """Test dispatching multiple different node types."""
        symbol_table = self._create_empty_symbol_table()
        
        while_node: AST = {"type": "while"}
        if_node: AST = {"type": "if"}
        
        _traverse_node(while_node, symbol_table)
        _traverse_node(if_node, symbol_table)
        
        mock_handle_while.assert_called_once_with(while_node, symbol_table)
        mock_handle_if.assert_called_once_with(if_node, symbol_table)
    
    @patch('._handle_while_package._handle_while_src._handle_while')
    def test_handler_exception_not_caught(self, mock_handle_while):
        """Test that handler exceptions propagate (function doesn't catch exceptions)."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {"type": "while"}
        mock_handle_while.side_effect = ValueError("Test exception")
        
        with self.assertRaises(ValueError):
            _traverse_node(node, symbol_table)
    
    @patch('._handle_while_package._handle_while_src._handle_while')
    def test_node_with_additional_fields(self, mock_handle_while):
        """Test that nodes with additional fields are passed correctly."""
        symbol_table = self._create_empty_symbol_table()
        
        node: AST = {
            "type": "while",
            "children": [{"type": "binary_op"}],
            "line": 10,
            "column": 5
        }
        
        _traverse_node(node, symbol_table)
        
        mock_handle_while.assert_called_once_with(node, symbol_table)
    
    @patch('._handle_block_package._handle_block_src._handle_block')
    def test_symbol_table_passed_unchanged(self, mock_handle_block):
        """Test that symbol_table is passed to handler without modification by _traverse_node."""
        symbol_table = self._create_empty_symbol_table()
        original_id = id(symbol_table)
        
        node: AST = {"type": "block"}
        _traverse_node(node, symbol_table)
        
        # Verify same object is passed (handlers may modify it)
        mock_handle_block.assert_called_once()
        called_symbol_table = mock_handle_block.call_args[0][1]
        self.assertEqual(id(called_symbol_table), original_id)


if __name__ == '__main__':
    unittest.main()
