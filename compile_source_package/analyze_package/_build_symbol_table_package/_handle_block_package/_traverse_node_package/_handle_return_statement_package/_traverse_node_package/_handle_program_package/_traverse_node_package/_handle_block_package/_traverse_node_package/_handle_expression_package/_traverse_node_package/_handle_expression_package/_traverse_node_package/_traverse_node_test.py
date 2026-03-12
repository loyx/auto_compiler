import unittest
from unittest.mock import patch

# Relative import from the same package
from ._traverse_node_src import _traverse_node


class TestTraverseNode(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }
    
    def test_expression_node_delegates_to_handle_expression(self):
        """Test that expression nodes are delegated to _handle_expression"""
        with patch('._traverse_node_src._handle_expression') as mock_handle:
            node = {"type": "expression", "value": "x + 1"}
            symbol_table = self.base_symbol_table.copy()
            symbol_table["errors"] = []
            
            _traverse_node(node, symbol_table)
            
            mock_handle.assert_called_once_with(node, symbol_table)
    
    def test_block_node_manages_scope(self):
        """Test that block nodes properly manage scope"""
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["current_scope"] = 0
        symbol_table["scope_stack"] = []
        
        _traverse_node(node, symbol_table)
        
        # Scope should return to original after exiting block
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_block_node_with_nested_children(self):
        """Test block node with nested children traverses all"""
        child_node = {"type": "identifier", "value": "x", "children": []}
        node = {
            "type": "block",
            "children": [child_node]
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["current_scope"] = 0
        symbol_table["scope_stack"] = []
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Scope should return to original
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        # Should have error for undefined variable
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_identifier_node_checks_variable_declaration(self):
        """Test that identifier nodes check if variables are declared"""
        node = {
            "type": "identifier",
            "value": "undefined_var",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Should add an error for undefined variable
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "UNDEFINED_VARIABLE")
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)
    
    def test_identifier_node_with_defined_variable(self):
        """Test that defined identifiers don't add errors"""
        node = {
            "type": "identifier",
            "value": "defined_var",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["variables"] = {
            "defined_var": {"data_type": "int", "is_declared": True}
        }
        
        _traverse_node(node, symbol_table)
        
        # Should not add any errors
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_function_call_node_checks_function_declaration(self):
        """Test that function_call nodes check if functions are declared"""
        node = {
            "type": "function_call",
            "value": "undefined_func",
            "line": 15,
            "column": 10,
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["functions"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Should add an error for undefined function
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "UNDEFINED_FUNCTION")
        self.assertEqual(symbol_table["errors"][0]["line"], 15)
    
    def test_function_call_node_with_defined_function(self):
        """Test that defined function calls don't add errors"""
        node = {
            "type": "function_call",
            "value": "defined_func",
            "line": 15,
            "column": 10,
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["functions"] = {
            "defined_func": {"return_type": "int", "params": []}
        }
        
        _traverse_node(node, symbol_table)
        
        # Should not add any errors
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_function_declaration_node_registers_function(self):
        """Test that function_declaration nodes register functions"""
        node = {
            "type": "function_declaration",
            "value": "my_func",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["functions"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Should register the function
        self.assertIn("my_func", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["my_func"]["return_type"], "int")
        self.assertEqual(symbol_table["functions"]["my_func"]["line"], 1)
    
    def test_function_declaration_duplicate(self):
        """Test that duplicate function declarations add errors"""
        node = {
            "type": "function_declaration",
            "value": "my_func",
            "data_type": "int",
            "line": 5,
            "column": 0,
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["functions"] = {
            "my_func": {"return_type": "int", "params": []}
        }
        
        _traverse_node(node, symbol_table)
        
        # Should add duplicate function error
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "DUPLICATE_FUNCTION")
        # Should not overwrite existing function
        self.assertIn("my_func", symbol_table["functions"])
    
    def test_assignment_node_traverses_children(self):
        """Test that assignment nodes traverse all children"""
        child_node = {"type": "identifier", "value": "x", "children": []}
        node = {
            "type": "assignment",
            "children": [child_node]
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Should traverse children and add error for undefined variable
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_program_node_traverses_children(self):
        """Test that program nodes (default case) traverse children"""
        child_node = {"type": "identifier", "value": "x", "children": []}
        node = {
            "type": "program",
            "children": [child_node]
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Should traverse children
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_ensures_errors_list_exists(self):
        """Test that function ensures errors list exists in symbol_table"""
        node = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {}
        }
        
        _traverse_node(node, symbol_table)
        
        # Should create errors list
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
    
    def test_node_with_empty_children(self):
        """Test node with empty children list"""
        node = {
            "type": "block",
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["current_scope"] = 0
        symbol_table["scope_stack"] = []
        
        _traverse_node(node, symbol_table)
        
        # Should handle gracefully
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
    
    def test_node_missing_type_field(self):
        """Test node without type field defaults to empty string"""
        node = {
            "children": []
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        
        _traverse_node(node, symbol_table)
        
        # Should handle gracefully (treat as default case)
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_identifier_with_children_traverses_them(self):
        """Test that identifier nodes also traverse their children"""
        child_node = {"type": "identifier", "value": "nested_var", "children": []}
        node = {
            "type": "identifier",
            "value": "parent_var",
            "children": [child_node]
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Should add errors for both undefined variables
        self.assertEqual(len(symbol_table["errors"]), 2)
    
    def test_function_call_with_argument_expressions(self):
        """Test that function_call traverses argument expression children"""
        arg_node = {"type": "identifier", "value": "arg_var", "children": []}
        node = {
            "type": "function_call",
            "value": "my_func",
            "children": [arg_node]
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []
        symbol_table["functions"] = {"my_func": {"return_type": "int"}}
        symbol_table["variables"] = {}
        
        _traverse_node(node, symbol_table)
        
        # Function is defined, but arg_var is not
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "UNDEFINED_VARIABLE")


if __name__ == '__main__':
    unittest.main()
