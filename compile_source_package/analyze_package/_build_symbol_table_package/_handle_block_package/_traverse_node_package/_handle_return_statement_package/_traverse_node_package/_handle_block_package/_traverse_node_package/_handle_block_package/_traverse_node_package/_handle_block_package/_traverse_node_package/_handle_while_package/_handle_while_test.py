import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._handle_while_src import _handle_while


class TestHandleWhile(unittest.TestCase):
    """Test cases for _handle_while function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_with_condition_and_body(self, mock_traverse):
        """Test handling while node with both condition and body."""
        node = {
            "type": "while",
            "condition": {"type": "binary_op", "value": "x < 10"},
            "body": {"type": "block", "children": []}
        }
        
        _handle_while(node, self.symbol_table)
        
        # Verify _traverse_node was called twice
        self.assertEqual(mock_traverse.call_count, 2)
        
        # Verify first call with condition
        mock_traverse.assert_any_call(node["condition"], self.symbol_table)
        
        # Verify second call with body
        mock_traverse.assert_any_call(node["body"], self.symbol_table)
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_with_only_condition(self, mock_traverse):
        """Test handling while node with only condition (no body)."""
        node = {
            "type": "while",
            "condition": {"type": "binary_op", "value": "x < 10"}
        }
        
        _handle_while(node, self.symbol_table)
        
        # Verify _traverse_node was called once with condition
        mock_traverse.assert_called_once_with(node["condition"], self.symbol_table)
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_with_only_body(self, mock_traverse):
        """Test handling while node with only body (no condition)."""
        node = {
            "type": "while",
            "body": {"type": "block", "children": []}
        }
        
        _handle_while(node, self.symbol_table)
        
        # Verify _traverse_node was called once with body
        mock_traverse.assert_called_once_with(node["body"], self.symbol_table)
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_with_no_condition_and_no_body(self, mock_traverse):
        """Test handling while node with neither condition nor body."""
        node = {
            "type": "while"
        }
        
        _handle_while(node, self.symbol_table)
        
        # Verify _traverse_node was not called
        mock_traverse.assert_not_called()
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_with_empty_node(self, mock_traverse):
        """Test handling empty node dict."""
        node = {}
        
        _handle_while(node, self.symbol_table)
        
        # Verify _traverse_node was not called
        mock_traverse.assert_not_called()
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_with_none_values(self, mock_traverse):
        """Test handling while node with explicit None values."""
        node = {
            "type": "while",
            "condition": None,
            "body": None
        }
        
        _handle_while(node, self.symbol_table)
        
        # Verify _traverse_node was not called
        mock_traverse.assert_not_called()
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_preserves_symbol_table(self, mock_traverse):
        """Test that symbol_table is passed correctly to _traverse_node."""
        node = {
            "type": "while",
            "condition": {"type": "binary_op"},
            "body": {"type": "block"}
        }
        
        _handle_while(node, self.symbol_table)
        
        # Verify the same symbol_table instance is passed
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][1], self.symbol_table)
        self.assertEqual(calls[1][0][1], self.symbol_table)
    
    @patch('._handle_while_package._handle_while_src._traverse_node')
    def test_handle_while_complex_condition_and_body(self, mock_traverse):
        """Test handling while node with complex condition and body structures."""
        node = {
            "type": "while",
            "condition": {
                "type": "binary_op",
                "left": {"type": "identifier", "value": "x"},
                "operator": "<",
                "right": {"type": "literal", "value": 10}
            },
            "body": {
                "type": "block",
                "children": [
                    {"type": "assignment", "target": "x", "value": {"type": "literal", "value": 1}},
                    {"type": "print", "argument": {"type": "identifier", "value": "x"}}
                ]
            }
        }
        
        _handle_while(node, self.symbol_table)
        
        # Verify _traverse_node was called twice
        self.assertEqual(mock_traverse.call_count, 2)
        
        # Verify calls with correct arguments
        mock_traverse.assert_any_call(node["condition"], self.symbol_table)
        mock_traverse.assert_any_call(node["body"], self.symbol_table)


if __name__ == '__main__':
    unittest.main()
