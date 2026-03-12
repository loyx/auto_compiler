"""
Unit tests for _handle_if_statement function.
Tests the handling of if_statement AST nodes.
"""
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# Import the function under test using relative import
from ._handle_if_statement_src import _handle_if_statement

# Type aliases for clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIfStatement(unittest.TestCase):
    """Test cases for _handle_if_statement function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_with_all_branches(self, mock_traverse: MagicMock):
        """Test if statement with condition, then_branch, and else_branch."""
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "line": 1, "column": 1},
            "then_branch": {"type": "block", "line": 1, "column": 10},
            "else_branch": {"type": "block", "line": 2, "column": 1},
            "line": 1,
            "column": 1
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called 3 times
        self.assertEqual(mock_traverse.call_count, 3)
        
        # Verify calls were made in correct order
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "binary_op")  # condition
        self.assertEqual(calls[1][0][0]["type"], "block")  # then_branch
        self.assertEqual(calls[2][0][0]["type"], "block")  # else_branch
        
        # Verify symbol_table was passed to each call
        for call in calls:
            self.assertIs(call[0][1], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_without_else(self, mock_traverse: MagicMock):
        """Test if statement with only then_branch (no else)."""
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "line": 1, "column": 1},
            "then_branch": {"type": "block", "line": 1, "column": 10},
            "else_branch": None,
            "line": 1,
            "column": 1
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called 2 times (condition and then_branch only)
        self.assertEqual(mock_traverse.call_count, 2)
        
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "binary_op")  # condition
        self.assertEqual(calls[1][0][0]["type"], "block")  # then_branch
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_with_none_condition(self, mock_traverse: MagicMock):
        """Test if statement with None condition."""
        node: AST = {
            "type": "if_statement",
            "condition": None,
            "then_branch": {"type": "block", "line": 1, "column": 10},
            "else_branch": {"type": "block", "line": 2, "column": 1},
            "line": 1,
            "column": 1
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called 2 times (then_branch and else_branch only)
        self.assertEqual(mock_traverse.call_count, 2)
        
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "block")  # then_branch
        self.assertEqual(calls[1][0][0]["type"], "block")  # else_branch
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_with_none_then_branch(self, mock_traverse: MagicMock):
        """Test if statement with condition and else_branch but no then_branch."""
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "line": 1, "column": 1},
            "then_branch": None,
            "else_branch": {"type": "block", "line": 2, "column": 1},
            "line": 1,
            "column": 1
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify _traverse_node was called 2 times (condition and else_branch only)
        self.assertEqual(mock_traverse.call_count, 2)
        
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "binary_op")  # condition
        self.assertEqual(calls[1][0][0]["type"], "block")  # else_branch
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_with_empty_dict(self, mock_traverse: MagicMock):
        """Test if statement node with empty dictionary (no branches)."""
        node: AST = {
            "type": "if_statement",
            "line": 1,
            "column": 1
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Should not call _traverse_node at all
        self.assertEqual(mock_traverse.call_count, 0)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_preserves_symbol_table(self, mock_traverse: MagicMock):
        """Test that symbol_table is passed unchanged to _traverse_node."""
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op"},
            "then_branch": {"type": "block"},
            "else_branch": {"type": "block"}
        }
        
        # Make a copy to compare later
        original_symbol_table = self.symbol_table.copy()
        
        _handle_if_statement(node, self.symbol_table)
        
        # Verify symbol_table wasn't modified
        self.assertEqual(self.symbol_table, original_symbol_table)
        
        # Verify it was passed to each call
        for call in mock_traverse.call_args_list:
            self.assertIs(call[0][1], self.symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_with_nested_if(self, mock_traverse: MagicMock):
        """Test if statement containing nested if statements."""
        nested_if: AST = {
            "type": "if_statement",
            "condition": {"type": "comparison"},
            "then_branch": {"type": "assignment"},
            "else_branch": None
        }
        
        node: AST = {
            "type": "if_statement",
            "condition": {"type": "binary_op"},
            "then_branch": nested_if,
            "else_branch": {"type": "block"}
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Should call for condition, then_branch (nested if), and else_branch
        self.assertEqual(mock_traverse.call_count, 3)
        
        # Verify nested_if was passed as then_branch
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[1][0][0]["type"], "if_statement")
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node')
    def test_handle_if_statement_with_complex_condition(self, mock_traverse: MagicMock):
        """Test if statement with complex nested condition."""
        complex_condition: AST = {
            "type": "logical_and",
            "left": {"type": "comparison", "operator": ">", "left": {"type": "identifier", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "right": {"type": "comparison", "operator": "<", "left": {"type": "identifier", "name": "x"}, "right": {"type": "literal", "value": 10}}
        }
        
        node: AST = {
            "type": "if_statement",
            "condition": complex_condition,
            "then_branch": {"type": "block", "statements": []},
            "else_branch": None
        }
        
        _handle_if_statement(node, self.symbol_table)
        
        # Should call for condition and then_branch
        self.assertEqual(mock_traverse.call_count, 2)
        
        # Verify complex condition was passed
        calls = mock_traverse.call_args_list
        self.assertEqual(calls[0][0][0]["type"], "logical_and")


if __name__ == '__main__':
    unittest.main()
