import unittest
from unittest.mock import patch, call
from typing import Dict, Any

# Relative import for the function under test
from ._handle_while_statement_src import _handle_while_statement


class TestHandleWhileStatement(unittest.TestCase):
    """Test cases for _handle_while_statement function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._handle_while_statement_src._traverse_node')
    def test_handle_while_statement_with_condition_and_body(self, mock_traverse_node):
        """Test handling while statement with both condition and body."""
        node = {
            "type": "while_statement",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": {"type": "block", "children": []}
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called twice (once for condition, once for body)
        self.assertEqual(mock_traverse_node.call_count, 2)
        
        # Verify calls were made with correct arguments
        expected_calls = [
            call(node["condition"], self.symbol_table),
            call(node["body"], self.symbol_table)
        ]
        mock_traverse_node.assert_has_calls(expected_calls)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._handle_while_statement_src._traverse_node')
    def test_handle_while_statement_with_only_condition(self, mock_traverse_node):
        """Test handling while statement with only condition (no body)."""
        node = {
            "type": "while_statement",
            "condition": {"type": "expression", "value": "x < 10"}
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called once (only for condition)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["condition"], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._handle_while_statement_src._traverse_node')
    def test_handle_while_statement_with_only_body(self, mock_traverse_node):
        """Test handling while statement with only body (no condition)."""
        node = {
            "type": "while_statement",
            "body": {"type": "block", "children": []}
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called once (only for body)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["body"], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._handle_while_statement_src._traverse_node')
    def test_handle_while_statement_with_neither_condition_nor_body(self, mock_traverse_node):
        """Test handling while statement with neither condition nor body."""
        node = {
            "type": "while_statement"
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was not called
        self.assertEqual(mock_traverse_node.call_count, 0)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_statement_with_none_condition(self, mock_traverse_node):
        """Test handling while statement with None condition."""
        node = {
            "type": "while_statement",
            "condition": None,
            "body": {"type": "block", "children": []}
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called once (only for body, not for None condition)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["body"], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_statement_with_none_body(self, mock_traverse_node):
        """Test handling while statement with None body."""
        node = {
            "type": "while_statement",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": None
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called once (only for condition, not for None body)
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["condition"], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_statement_symbol_table_passed_correctly(self, mock_traverse_node):
        """Test that symbol_table is passed correctly to _traverse_node."""
        node = {
            "type": "while_statement",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": {"type": "block", "children": []}
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify symbol_table is passed to both calls
        calls = mock_traverse_node.call_args_list
        self.assertEqual(len(calls), 2)
        
        # Check first call (condition)
        self.assertEqual(calls[0][0][1], self.symbol_table)
        
        # Check second call (body)
        self.assertEqual(calls[1][0][1], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_statement_complex_condition_and_body(self, mock_traverse_node):
        """Test handling while statement with complex condition and body."""
        node = {
            "type": "while_statement",
            "condition": {
                "type": "binary_expression",
                "left": {"type": "identifier", "value": "x"},
                "operator": "<",
                "right": {"type": "literal", "value": 10}
            },
            "body": {
                "type": "block",
                "children": [
                    {"type": "assignment", "variable": "x", "value": {"type": "literal", "value": 5}}
                ]
            }
        }
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called twice
        self.assertEqual(mock_traverse_node.call_count, 2)
        
        # Verify calls with complex structures
        mock_traverse_node.assert_any_call(node["condition"], self.symbol_table)
        mock_traverse_node.assert_any_call(node["body"], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_statement_preserves_symbol_table_state(self, mock_traverse_node):
        """Test that symbol_table structure is preserved after handling."""
        node = {
            "type": "while_statement",
            "condition": {"type": "expression", "value": "x < 10"},
            "body": {"type": "block", "children": []}
        }
        
        original_keys = set(self.symbol_table.keys())
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify symbol_table keys are preserved (function doesn't modify structure directly)
        self.assertEqual(set(self.symbol_table.keys()), original_keys)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_while_statement_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_while_statement_empty_node(self, mock_traverse_node):
        """Test handling empty node dictionary."""
        node = {}
        
        _handle_while_statement(node, self.symbol_table)
        
        # Verify _traverse_node was not called for empty node
        self.assertEqual(mock_traverse_node.call_count, 0)


if __name__ == '__main__':
    unittest.main()
