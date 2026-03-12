import unittest
from typing import Any, Dict

from ._handle_var_decl_src import _handle_var_decl


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
    
    def test_new_variable_declaration_int(self):
        """Test declaring a new integer variable."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 5
        }
        
        _handle_var_decl(node, self.symbol_table)
        
        self.assertIn("x", self.symbol_table["variables"])
        var_info = self.symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 1)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_new_variable_declaration_char(self):
        """Test declaring a new char variable."""
        node: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "char",
            "line": 3,
            "column": 10
        }
        
        _handle_var_decl(node, self.symbol_table)
        
        self.assertIn("c", self.symbol_table["variables"])
        var_info = self.symbol_table["variables"]["c"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 3)
        self.assertEqual(var_info["column"], 10)
    
    def test_duplicate_variable_declaration(self):
        """Test that duplicate variable declaration records an error."""
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 5
        }
        node2: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 5,
            "column": 8
        }
        
        _handle_var_decl(node1, self.symbol_table)
        _handle_var_decl(node2, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("变量重复声明", self.symbol_table["errors"][0])
        self.assertIn("行 5", self.symbol_table["errors"][0])
        self.assertIn("列 8", self.symbol_table["errors"][0])
        self.assertEqual(len(self.symbol_table["variables"]), 1)
    
    def test_missing_errors_list_in_symbol_table(self):
        """Test that errors list is created if missing."""
        symbol_table_no_errors: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 5
        }
        node2: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 2,
            "column": 5
        }
        
        _handle_var_decl(node1, symbol_table_no_errors)
        _handle_var_decl(node2, symbol_table_no_errors)
        
        self.assertIn("errors", symbol_table_no_errors)
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)
    
    def test_variable_declaration_with_scope_level(self):
        """Test variable declaration records correct scope level."""
        self.symbol_table["current_scope"] = 2
        
        node: AST = {
            "type": "var_decl",
            "value": "y",
            "data_type": "int",
            "line": 10,
            "column": 3
        }
        
        _handle_var_decl(node, self.symbol_table)
        
        var_info = self.symbol_table["variables"]["y"]
        self.assertEqual(var_info["scope_level"], 2)
    
    def test_missing_current_scope_defaults_to_zero(self):
        """Test that missing current_scope defaults to 0."""
        symbol_table_no_scope: SymbolTable = {
            "variables": {},
            "functions": {},
            "scope_stack": [],
            "errors": []
        }
        
        node: AST = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        
        _handle_var_decl(node, symbol_table_no_scope)
        
        var_info = symbol_table_no_scope["variables"]["z"]
        self.assertEqual(var_info["scope_level"], 0)
    
    def test_multiple_different_variables(self):
        """Test declaring multiple different variables."""
        node1: AST = {
            "type": "var_decl",
            "value": "a",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        node2: AST = {
            "type": "var_decl",
            "value": "b",
            "data_type": "char",
            "line": 2,
            "column": 2
        }
        node3: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "int",
            "line": 3,
            "column": 3
        }
        
        _handle_var_decl(node1, self.symbol_table)
        _handle_var_decl(node2, self.symbol_table)
        _handle_var_decl(node3, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["variables"]), 3)
        self.assertIn("a", self.symbol_table["variables"])
        self.assertIn("b", self.symbol_table["variables"])
        self.assertIn("c", self.symbol_table["variables"])
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_duplicate_after_multiple_declarations(self):
        """Test duplicate declaration after multiple successful declarations."""
        node1: AST = {
            "type": "var_decl",
            "value": "a",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        node2: AST = {
            "type": "var_decl",
            "value": "b",
            "data_type": "char",
            "line": 2,
            "column": 2
        }
        node3: AST = {
            "type": "var_decl",
            "value": "a",
            "data_type": "int",
            "line": 3,
            "column": 3
        }
        
        _handle_var_decl(node1, self.symbol_table)
        _handle_var_decl(node2, self.symbol_table)
        _handle_var_decl(node3, self.symbol_table)
        
        self.assertEqual(len(self.symbol_table["variables"]), 2)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("变量重复声明", self.symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()
