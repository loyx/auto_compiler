import unittest
from unittest.mock import patch
from typing import Any, Dict

# Import the function under test using relative import
from ._handle_expression_statement_src import _handle_expression_statement

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleExpressionStatement(unittest.TestCase):
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_expression_statement_package._traverse_node_src._traverse_node')
    def test_handle_expression_statement_with_expression(self, mock_traverse_node):
        """Test handling node with expression field"""
        node: AST = {
            "type": "expression_statement",
            "expression": {
                "type": "binary_operation",
                "left": {"type": "identifier", "name": "x"},
                "right": {"type": "literal", "value": 5}
            }
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        _handle_expression_statement(node, symbol_table)
        
        # Verify _traverse_node was called with the expression and symbol_table
        mock_traverse_node.assert_called_once_with(
            node["expression"],
            symbol_table
        )
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_expression_statement_package._traverse_node_src._traverse_node')
    def test_handle_expression_statement_without_expression(self, mock_traverse_node):
        """Test handling node without expression field"""
        node: AST = {
            "type": "expression_statement"
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        _handle_expression_statement(node, symbol_table)
        
        # Verify _traverse_node was not called
        mock_traverse_node.assert_not_called()
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_expression_statement_package._traverse_node_src._traverse_node')
    def test_handle_expression_statement_with_none_expression(self, mock_traverse_node):
        """Test handling node with expression=None"""
        node: AST = {
            "type": "expression_statement",
            "expression": None
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        _handle_expression_statement(node, symbol_table)
        
        # Verify _traverse_node was not called
        mock_traverse_node.assert_not_called()
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_expression_statement_package._traverse_node_src._traverse_node')
    def test_handle_expression_statement_passes_symbol_table(self, mock_traverse_node):
        """Test that symbol_table is passed correctly to _traverse_node"""
        node: AST = {
            "type": "expression_statement",
            "expression": {"type": "identifier", "name": "x"}
        }
        symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int"}},
            "functions": {},
            "current_scope": 1
        }
        
        _handle_expression_statement(node, symbol_table)
        
        # Verify symbol_table is passed as-is (same object reference)
        mock_traverse_node.assert_called_once()
        called_args = mock_traverse_node.call_args
        self.assertIs(called_args[0][1], symbol_table)
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_expression_statement_package._traverse_node_src._traverse_node')
    def test_handle_expression_statement_complex_expression(self, mock_traverse_node):
        """Test handling node with complex nested expression"""
        node: AST = {
            "type": "expression_statement",
            "expression": {
                "type": "function_call",
                "name": "print",
                "args": [
                    {"type": "literal", "value": "hello"},
                    {"type": "identifier", "name": "x"}
                ]
            }
        }
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        _handle_expression_statement(node, symbol_table)
        
        # Verify _traverse_node is called with the complex expression
        mock_traverse_node.assert_called_once_with(
            node["expression"],
            symbol_table
        )
    
    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_expression_statement_package._traverse_node_src._traverse_node')
    def test_handle_expression_statement_empty_node(self, mock_traverse_node):
        """Test handling empty node dict"""
        node: AST = {}
        symbol_table: SymbolTable = {"variables": {}, "functions": {}}
        
        _handle_expression_statement(node, symbol_table)
        
        # Verify _traverse_node was not called (no expression key)
        mock_traverse_node.assert_not_called()


if __name__ == '__main__':
    unittest.main()
