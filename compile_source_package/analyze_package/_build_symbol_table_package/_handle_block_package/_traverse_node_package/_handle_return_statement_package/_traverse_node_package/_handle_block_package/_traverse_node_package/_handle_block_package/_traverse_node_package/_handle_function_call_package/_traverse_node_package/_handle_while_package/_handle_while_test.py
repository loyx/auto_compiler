import unittest
from unittest.mock import patch, call
from typing import Any, Dict

# Relative import for the function under test
from _handle_while_package._handle_while_src import _handle_while

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhile(unittest.TestCase):
    """Test cases for _handle_while function"""
    
    @patch('_handle_while_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_valid_node(self, mock_traverse_node):
        """Test handling a valid while node with condition and body"""
        # Setup
        condition_node = {"type": "binary_op", "value": ">", "line": 1, "column": 5}
        body_node = {"type": "block", "children": [], "line": 1, "column": 10}
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 1,
            "column": 0
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        # Execute
        _handle_while(node, symbol_table)
        
        # Verify
        self.assertEqual(mock_traverse_node.call_count, 2)
        mock_traverse_node.assert_has_calls([
            call(condition_node, symbol_table),
            call(body_node, symbol_table)
        ])
    
    @patch('._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_empty_children(self, mock_traverse_node):
        """Test handling while node with empty children list"""
        # Setup
        node = {
            "type": "while",
            "children": [],
            "line": 1,
            "column": 0
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        # Execute
        _handle_while(node, symbol_table)
        
        # Verify - should return early without calling _traverse_node
        mock_traverse_node.assert_not_called()
    
    @patch('._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_only_condition(self, mock_traverse_node):
        """Test handling while node with only condition (missing body)"""
        # Setup
        condition_node = {"type": "binary_op", "value": ">", "line": 1, "column": 5}
        node = {
            "type": "while",
            "children": [condition_node],
            "line": 1,
            "column": 0
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        # Execute
        _handle_while(node, symbol_table)
        
        # Verify - should return early without calling _traverse_node
        mock_traverse_node.assert_not_called()
    
    @patch('._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_no_children_key(self, mock_traverse_node):
        """Test handling while node without children key"""
        # Setup
        node = {
            "type": "while",
            "line": 1,
            "column": 0
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        # Execute
        _handle_while(node, symbol_table)
        
        # Verify - should use default [] and return early
        mock_traverse_node.assert_not_called()
    
    @patch('._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_symbol_table_passed_correctly(self, mock_traverse_node):
        """Test that symbol_table is passed correctly to _traverse_node"""
        # Setup
        condition_node = {"type": "identifier", "value": "x", "line": 1, "column": 5}
        body_node = {"type": "block", "children": [], "line": 1, "column": 10}
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {"x": {"data_type": "int", "is_declared": True}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0],
            "errors": []
        }
        
        # Execute
        _handle_while(node, symbol_table)
        
        # Verify symbol_table is passed to both calls
        calls = mock_traverse_node.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][1], symbol_table)
        self.assertEqual(calls[1][0][1], symbol_table)
    
    @patch('._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_complex_body(self, mock_traverse_node):
        """Test handling while node with complex body containing nested statements"""
        # Setup
        condition_node = {
            "type": "binary_op",
            "operator": "<",
            "left": {"type": "identifier", "value": "i"},
            "right": {"type": "literal", "value": 10},
            "line": 1,
            "column": 5
        }
        body_node = {
            "type": "block",
            "children": [
                {"type": "assignment", "target": "i", "value": {"type": "binary_op", "operator": "+", "left": {"type": "identifier", "value": "i"}, "right": {"type": "literal", "value": 1}}},
                {"type": "function_call", "name": "print", "args": [{"type": "identifier", "value": "i"}]}
            ],
            "line": 1,
            "column": 10
        }
        node = {
            "type": "while",
            "children": [condition_node, body_node],
            "line": 1,
            "column": 0
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        # Execute
        _handle_while(node, symbol_table)
        
        # Verify
        self.assertEqual(mock_traverse_node.call_count, 2)
        mock_traverse_node.assert_has_calls([
            call(condition_node, symbol_table),
            call(body_node, symbol_table)
        ])
    
    @patch('._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_three_children(self, mock_traverse_node):
        """Test handling while node with more than 2 children (should only process first 2)"""
        # Setup
        condition_node = {"type": "binary_op", "value": ">", "line": 1, "column": 5}
        body_node = {"type": "block", "children": [], "line": 1, "column": 10}
        extra_node = {"type": "comment", "value": "extra", "line": 1, "column": 15}
        node = {
            "type": "while",
            "children": [condition_node, body_node, extra_node],
            "line": 1,
            "column": 0
        }
        symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        
        # Execute
        _handle_while(node, symbol_table)
        
        # Verify - should only process first 2 children
        self.assertEqual(mock_traverse_node.call_count, 2)
        mock_traverse_node.assert_has_calls([
            call(condition_node, symbol_table),
            call(body_node, symbol_table)
        ])
        # Verify extra_node was not processed
        calls = mock_traverse_node.call_args_list
        for call_args in calls:
            self.assertNotEqual(call_args[0][0], extra_node)


if __name__ == '__main__':
    unittest.main()
