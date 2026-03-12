# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === relative import from the same package ===
from ._traverse_node_src import _traverse_node

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """Test cases for _traverse_node AST dispatcher function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    @patch('._handle_function_decl_package._handle_function_decl_src._handle_function_decl')
    def test_function_decl_node(self, mock_handler):
        """Test function_decl node type dispatches to _handle_function_decl."""
        node = {
            "type": "function_decl",
            "value": "main",
            "data_type": "int",
            "line": 1,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl')
    def test_var_decl_node(self, mock_handler):
        """Test var_decl node type dispatches to _handle_var_decl."""
        node = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 2,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._handle_assignment_package._handle_assignment_src._handle_assignment')
    def test_assignment_node(self, mock_handler):
        """Test assignment node type dispatches to _handle_assignment."""
        node = {
            "type": "assignment",
            "value": "x",
            "line": 3,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._handle_if_package._handle_if_src._handle_if')
    def test_if_node(self, mock_handler):
        """Test if node type dispatches to _handle_if."""
        node = {
            "type": "if",
            "children": [],
            "line": 4,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._handle_while_package._handle_while_src._handle_while')
    def test_while_node(self, mock_handler):
        """Test while node type dispatches to _handle_while."""
        node = {
            "type": "while",
            "children": [],
            "line": 5,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._handle_return_package._handle_return_src._handle_return')
    def test_return_node(self, mock_handler):
        """Test return node type dispatches to _handle_return."""
        node = {
            "type": "return",
            "value": 42,
            "line": 6,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._handle_function_call_package._handle_function_call_src._handle_function_call')
    def test_function_call_node(self, mock_handler):
        """Test function_call node type dispatches to _handle_function_call."""
        node = {
            "type": "function_call",
            "value": "printf",
            "line": 7,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)
    
    @patch('._handle_function_decl_package._handle_function_decl_src._handle_function_decl')
    @patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl')
    def test_block_node_recurses_children(self, mock_var_decl, mock_func_decl):
        """Test block node recursively processes all children."""
        child1 = {"type": "var_decl", "value": "a", "data_type": "int", "line": 1, "column": 0}
        child2 = {"type": "var_decl", "value": "b", "data_type": "int", "line": 2, "column": 0}
        node = {
            "type": "block",
            "children": [child1, child2]
        }
        
        _traverse_node(node, self.symbol_table)
        
        # Should call var_decl handler twice (once for each child)
        self.assertEqual(mock_var_decl.call_count, 2)
        mock_func_decl.assert_not_called()
    
    @patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl')
    def test_param_list_node_recurses_children(self, mock_handler):
        """Test param_list node recursively processes all children."""
        child1 = {"type": "var_decl", "value": "param1", "data_type": "int", "line": 1, "column": 0}
        child2 = {"type": "var_decl", "value": "param2", "data_type": "int", "line": 1, "column": 10}
        node = {
            "type": "param_list",
            "children": [child1, child2]
        }
        
        _traverse_node(node, self.symbol_table)
        
        # Should call handler twice (once for each child)
        self.assertEqual(mock_handler.call_count, 2)
    
    @patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl')
    def test_unknown_node_type_recurses_children(self, mock_handler):
        """Test unknown node type defaults to recursing children."""
        child1 = {"type": "var_decl", "value": "x", "data_type": "int", "line": 1, "column": 0}
        node = {
            "type": "unknown_type",
            "children": [child1]
        }
        
        _traverse_node(node, self.symbol_table)
        
        # Should still recurse and call handler for child
        mock_handler.assert_called_once_with(child1, self.symbol_table)
    
    def test_initializes_errors_field(self):
        """Test that errors field is initialized if not present."""
        symbol_table_no_errors = {
            "variables": {},
            "functions": {}
        }
        
        node = {"type": "unknown", "children": []}
        _traverse_node(node, symbol_table_no_errors)
        
        self.assertIn("errors", symbol_table_no_errors)
        self.assertEqual(symbol_table_no_errors["errors"], [])
    
    def test_preserves_existing_errors_field(self):
        """Test that existing errors field is preserved."""
        symbol_table_with_errors = {
            "variables": {},
            "functions": {},
            "errors": [{"message": "existing error"}]
        }
        
        node = {"type": "unknown", "children": []}
        _traverse_node(node, symbol_table_with_errors)
        
        self.assertEqual(symbol_table_with_errors["errors"], [{"message": "existing error"}])
    
    def test_node_without_children_field(self):
        """Test node without 'children' field uses default empty list."""
        node = {"type": "unknown"}
        
        # Should not raise error
        _traverse_node(node, self.symbol_table)
    
    def test_node_without_type_field(self):
        """Test node without 'type' field defaults to empty string (unknown type)."""
        node = {"children": []}
        
        # Should not raise error, treats as unknown type
        _traverse_node(node, self.symbol_table)
    
    @patch('._handle_function_decl_package._handle_function_decl_src._handle_function_decl')
    @patch('._handle_var_decl_package._handle_var_decl_src._handle_var_decl')
    @patch('._handle_assignment_package._handle_assignment_src._handle_assignment')
    def test_mixed_children_in_block(self, mock_assignment, mock_var_decl, mock_func_decl):
        """Test block with mixed node types in children."""
        child1 = {"type": "var_decl", "value": "x", "data_type": "int", "line": 1, "column": 0}
        child2 = {"type": "assignment", "value": "x", "line": 2, "column": 0}
        child3 = {"type": "var_decl", "value": "y", "data_type": "char", "line": 3, "column": 0}
        node = {
            "type": "block",
            "children": [child1, child2, child3]
        }
        
        _traverse_node(node, self.symbol_table)
        
        self.assertEqual(mock_var_decl.call_count, 2)
        self.assertEqual(mock_assignment.call_count, 1)
        mock_func_decl.assert_not_called()
    
    def test_empty_block_node(self):
        """Test block node with empty children list."""
        node = {
            "type": "block",
            "children": []
        }
        
        # Should not raise error
        _traverse_node(node, self.symbol_table)
    
    @patch('._handle_return_package._handle_return_src._handle_return')
    def test_return_with_none_value(self, mock_handler):
        """Test return node with None value (void return)."""
        node = {
            "type": "return",
            "value": None,
            "line": 10,
            "column": 0
        }
        
        _traverse_node(node, self.symbol_table)
        
        mock_handler.assert_called_once_with(node, self.symbol_table)


if __name__ == '__main__':
    unittest.main()
