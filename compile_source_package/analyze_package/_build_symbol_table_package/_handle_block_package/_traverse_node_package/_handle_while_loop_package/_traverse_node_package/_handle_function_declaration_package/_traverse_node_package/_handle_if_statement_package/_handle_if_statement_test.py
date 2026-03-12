import unittest
from unittest.mock import patch, call
from typing import Dict, Any

# Relative import for the function under test
from ._handle_if_statement_src import _handle_if_statement

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIfStatement(unittest.TestCase):
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._handle_if_statement_src._traverse_node')
    def test_handle_if_statement_with_all_branches(self, mock_traverse):
        """Test if statement with condition, then_branch, and else_branch"""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_branch": {"type": "assignment", "target": "y", "value": "1"},
            "else_branch": {"type": "assignment", "target": "y", "value": "0"}
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_if_statement(node, symbol_table)
        
        # Verify _traverse_node was called for condition, then_branch, and else_branch
        self.assertEqual(mock_traverse.call_count, 3)
        mock_traverse.assert_has_calls([
            call({"type": "binary_op", "left": "x", "op": ">", "right": "0"}, symbol_table),
            call({"type": "assignment", "target": "y", "value": "1"}, symbol_table),
            call({"type": "assignment", "target": "y", "value": "0"}, symbol_table)
        ])
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._handle_if_statement_src._traverse_node')
    def test_handle_if_statement_without_else(self, mock_traverse):
        """Test if statement without else_branch (else_branch is None)"""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_branch": {"type": "assignment", "target": "y", "value": "1"},
            "else_branch": None
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_if_statement(node, symbol_table)
        
        # Verify _traverse_node was called only for condition and then_branch
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call({"type": "binary_op", "left": "x", "op": ">", "right": "0"}, symbol_table),
            call({"type": "assignment", "target": "y", "value": "1"}, symbol_table)
        ])
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._handle_if_statement_src._traverse_node')
    def test_handle_if_statement_without_else_branch_key(self, mock_traverse):
        """Test if statement when else_branch key is missing from node"""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_branch": {"type": "assignment", "target": "y", "value": "1"}
            # else_branch key is missing
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_if_statement(node, symbol_table)
        
        # Verify _traverse_node was called only for condition and then_branch
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call({"type": "binary_op", "left": "x", "op": ">", "right": "0"}, symbol_table),
            call({"type": "assignment", "target": "y", "value": "1"}, symbol_table)
        ])
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._handle_if_statement_src._traverse_node')
    def test_handle_if_statement_condition_none(self, mock_traverse):
        """Test if statement when condition is None"""
        node = {
            "type": "if_statement",
            "condition": None,
            "then_branch": {"type": "assignment", "target": "y", "value": "1"},
            "else_branch": {"type": "assignment", "target": "z", "value": "2"}
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_if_statement(node, symbol_table)
        
        # Verify _traverse_node was called only for then_branch and else_branch
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call({"type": "assignment", "target": "y", "value": "1"}, symbol_table),
            call({"type": "assignment", "target": "z", "value": "2"}, symbol_table)
        ])
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._handle_if_statement_src._traverse_node')
    def test_handle_if_statement_then_branch_none(self, mock_traverse):
        """Test if statement when then_branch is None"""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_branch": None,
            "else_branch": {"type": "assignment", "target": "z", "value": "2"}
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_if_statement(node, symbol_table)
        
        # Verify _traverse_node was called only for condition and else_branch
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call({"type": "binary_op", "left": "x", "op": ">", "right": "0"}, symbol_table),
            call({"type": "assignment", "target": "z", "value": "2"}, symbol_table)
        ])
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._handle_if_statement_src._traverse_node')
    def test_handle_if_statement_empty_node(self, mock_traverse):
        """Test if statement with empty node"""
        node = {}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_if_statement(node, symbol_table)
        
        # Verify _traverse_node was not called
        self.assertEqual(mock_traverse.call_count, 0)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_if_statement_package._handle_if_statement_src._traverse_node')
    def test_handle_if_statement_symbol_table_modification(self, mock_traverse):
        """Test that symbol_table is modified by _traverse_node calls"""
        node = {
            "type": "if_statement",
            "condition": {"type": "binary_op", "left": "x", "op": ">", "right": "0"},
            "then_branch": {"type": "assignment", "target": "y", "value": "1"},
            "else_branch": None
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        # Configure mock to modify symbol_table
        def side_effect(node_arg, sym_table):
            if node_arg.get("type") == "binary_op":
                sym_table["variables"]["x"] = {"type": "int", "scope": 0}
            elif node_arg.get("type") == "assignment":
                sym_table["variables"]["y"] = {"type": "int", "scope": 0}
        
        mock_traverse.side_effect = side_effect
        
        _handle_if_statement(node, symbol_table)
        
        # Verify symbol_table was modified
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(mock_traverse.call_count, 2)


if __name__ == '__main__':
    unittest.main()
