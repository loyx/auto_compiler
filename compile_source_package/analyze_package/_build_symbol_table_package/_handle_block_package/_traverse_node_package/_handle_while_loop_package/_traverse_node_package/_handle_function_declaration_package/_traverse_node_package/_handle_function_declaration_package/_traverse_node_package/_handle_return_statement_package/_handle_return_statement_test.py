import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._handle_return_statement_src import _handle_return_statement

# Type aliases
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturnStatement(unittest.TestCase):
    """Test cases for _handle_return_statement function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    def test_return_with_ast_expression(self):
        """Test return statement with AST expression node."""
        node = {
            "type": "return_statement",
            "expression": {
                "type": "binary_operation",
                "left": {"type": "identifier", "name": "x"},
                "right": {"type": "literal", "value": 5}
            },
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was called with the expression
            mock_traverse.assert_called_once_with(
                node["expression"],
                self.symbol_table
            )
    
    def test_return_with_none_expression(self):
        """Test return statement with None expression (return without value)."""
        node = {
            "type": "return_statement",
            "expression": None,
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_return_with_literal_expression(self):
        """Test return statement with literal value (not AST node)."""
        node = {
            "type": "return_statement",
            "expression": 42,
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_return_with_string_literal(self):
        """Test return statement with string literal."""
        node = {
            "type": "return_statement",
            "expression": "hello world",
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_return_with_dict_without_type(self):
        """Test return statement with dict that doesn't have 'type' field."""
        node = {
            "type": "return_statement",
            "expression": {"value": 42, "name": "test"},
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_return_with_empty_dict(self):
        """Test return statement with empty dict (no 'type' field)."""
        node = {
            "type": "return_statement",
            "expression": {},
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_return_with_list_expression(self):
        """Test return statement with list expression."""
        node = {
            "type": "return_statement",
            "expression": [1, 2, 3],
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_symbol_table_not_modified_with_ast_expression(self):
        """Test that symbol_table is not modified when processing AST expression."""
        node = {
            "type": "return_statement",
            "expression": {
                "type": "identifier",
                "name": "x"
            },
            "line": 10,
            "column": 5
        }
        
        original_table = {
            "variables": {"x": {"type": "int"}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }
        symbol_table = {
            "variables": original_table["variables"].copy(),
            "functions": original_table["functions"].copy(),
            "current_scope": original_table["current_scope"],
            "scope_stack": original_table["scope_stack"].copy()
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node"):
            _handle_return_statement(node, symbol_table)
            
            # Verify symbol_table remains unchanged
            self.assertEqual(symbol_table["variables"], original_table["variables"])
            self.assertEqual(symbol_table["functions"], original_table["functions"])
            self.assertEqual(symbol_table["current_scope"], original_table["current_scope"])
            self.assertEqual(symbol_table["scope_stack"], original_table["scope_stack"])
    
    def test_symbol_table_not_modified_with_none_expression(self):
        """Test that symbol_table is not modified when expression is None."""
        node = {
            "type": "return_statement",
            "expression": None,
            "line": 10,
            "column": 5
        }
        
        original_table = {
            "variables": {"x": {"type": "int"}},
            "functions": {"func1": {"params": []}},
            "current_scope": 2,
            "scope_stack": [0, 1, 2]
        }
        symbol_table = {
            "variables": original_table["variables"].copy(),
            "functions": original_table["functions"].copy(),
            "current_scope": original_table["current_scope"],
            "scope_stack": original_table["scope_stack"].copy()
        }
        
        _handle_return_statement(node, symbol_table)
        
        # Verify symbol_table remains unchanged
        self.assertEqual(symbol_table["variables"], original_table["variables"])
        self.assertEqual(symbol_table["functions"], original_table["functions"])
        self.assertEqual(symbol_table["current_scope"], original_table["current_scope"])
        self.assertEqual(symbol_table["scope_stack"], original_table["scope_stack"])
    
    def test_nested_ast_expression(self):
        """Test return statement with deeply nested AST expression."""
        node = {
            "type": "return_statement",
            "expression": {
                "type": "function_call",
                "function": {
                    "type": "identifier",
                    "name": "add"
                },
                "arguments": [
                    {"type": "literal", "value": 1},
                    {"type": "literal", "value": 2}
                ]
            },
            "line": 15,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was called once with the top-level expression
            mock_traverse.assert_called_once_with(
                node["expression"],
                self.symbol_table
            )
    
    def test_node_without_expression_key(self):
        """Test return statement node without expression key."""
        node = {
            "type": "return_statement",
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_zero_as_expression(self):
        """Test return statement with 0 as expression (falsy but not None)."""
        node = {
            "type": "return_statement",
            "expression": 0,
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_false_as_expression(self):
        """Test return statement with False as expression."""
        node = {
            "type": "return_statement",
            "expression": False,
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()
    
    def test_empty_string_as_expression(self):
        """Test return statement with empty string as expression."""
        node = {
            "type": "return_statement",
            "expression": "",
            "line": 10,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_return_statement_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, self.symbol_table)
            
            # Verify _traverse_node was not called
            mock_traverse.assert_not_called()


if __name__ == "__main__":
    unittest.main()
