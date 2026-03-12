import unittest
from unittest.mock import patch
from typing import Dict, Any

# Import the function under test using relative import
from ._traverse_node_src import _traverse_node

# Type aliases for clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    @patch('._traverse_node_src._handle_while_loop')
    def test_while_loop_dispatch(self, mock_handler):
        """Test that while_loop nodes are dispatched to _handle_while_loop."""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "binary_operation"},
            "body": {"type": "assignment"}
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_variable_declaration')
    def test_variable_declaration_dispatch(self, mock_handler):
        """Test that variable_declaration nodes are dispatched to _handle_variable_declaration."""
        node: AST = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "value": {"type": "literal"}
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_function_declaration')
    def test_function_declaration_dispatch(self, mock_handler):
        """Test that function_declaration nodes are dispatched to _handle_function_declaration."""
        node: AST = {
            "type": "function_declaration",
            "name": "foo",
            "params": [],
            "body": {"type": "return_statement"},
            "return_type": "int"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_function_call')
    def test_function_call_dispatch(self, mock_handler):
        """Test that function_call nodes are dispatched to _handle_function_call."""
        node: AST = {
            "type": "function_call",
            "name": "print",
            "arguments": [{"type": "literal"}]
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_assignment')
    def test_assignment_dispatch(self, mock_handler):
        """Test that assignment nodes are dispatched to _handle_assignment."""
        node: AST = {
            "type": "assignment",
            "target": {"type": "identifier"},
            "value": {"type": "literal"}
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_if_statement')
    def test_if_statement_dispatch(self, mock_handler):
        """Test that if_statement nodes are dispatched to _handle_if_statement."""
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_operation"},
            "then_body": {"type": "assignment"},
            "else_body": {"type": "return_statement"}
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_return_statement')
    def test_return_statement_dispatch(self, mock_handler):
        """Test that return_statement nodes are dispatched to _handle_return_statement."""
        node: AST = {
            "type": "return_statement",
            "value": {"type": "identifier"}
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_binary_operation')
    def test_binary_operation_dispatch(self, mock_handler):
        """Test that binary_operation nodes are dispatched to _handle_binary_operation."""
        node: AST = {
            "type": "binary_operation",
            "left": {"type": "identifier"},
            "right": {"type": "literal"},
            "operator": "+"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_identifier')
    def test_identifier_dispatch(self, mock_handler):
        """Test that identifier nodes are dispatched to _handle_identifier."""
        node: AST = {
            "type": "identifier",
            "name": "x"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._traverse_node_src._handle_literal')
    def test_literal_dispatch(self, mock_handler):
        """Test that literal nodes are dispatched to _handle_literal."""
        node: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int"
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    def test_none_type_returns_early(self):
        """Test that nodes with None type return early without calling any handler."""
        node: AST = {
            "type": None,
            "value": 42
        }
        
        # Should not raise any error and should not call any handlers
        result = _traverse_node(node, self.symbol_table)
        
        # Function should return None
        self.assertIsNone(result)
    
    def test_unknown_type_skipped(self):
        """Test that unknown node types are silently skipped."""
        node: AST = {
            "type": "unknown_type",
            "value": "something"
        }
        
        # Should not raise any error
        result = _traverse_node(node, self.symbol_table)
        
        # Function should return None
        self.assertIsNone(result)
    
    def test_missing_type_key(self):
        """Test that nodes without 'type' key are handled (get returns None)."""
        node: AST = {
            "value": 42
        }
        
        # Should not raise any error
        result = _traverse_node(node, self.symbol_table)
        
        # Function should return None
        self.assertIsNone(result)
    
    @patch('._traverse_node_src._handle_while_loop')
    @patch('._traverse_node_src._handle_variable_declaration')
    def test_only_correct_handler_called(self, mock_var_handler, mock_while_handler):
        """Test that only the correct handler is called for a given node type."""
        node: AST = {
            "type": "while_loop",
            "condition": {},
            "body": {}
        }
        
        _traverse_node(node, self.symbol_table)
        
        # Only while_loop handler should be called
        mock_while_handler.assert_called_once_with(node, self.symbol_table)
        mock_var_handler.assert_not_called()


if __name__ == '__main__':
    unittest.main()
