import unittest
from typing import Any, Dict

# Import the function to test using relative import
from ._handle_var_decl_src import _handle_var_decl

# Type aliases for clarity
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""
    
    def test_new_variable_declaration(self):
        """Test declaring a new variable adds it to symbol table."""
        node = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
    
    def test_duplicate_variable_declaration(self):
        """Test duplicate declaration adds error but doesn't modify variable."""
        node = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }
        
        _handle_var_decl(node, symbol_table)
        
        # Should not change the original variable
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        
        # Should add error
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 15)
        self.assertEqual(symbol_table["errors"][0]["column"], 8)
        self.assertIn("duplicate variable declaration: x", symbol_table["errors"][0]["message"])
    
    def test_initializes_missing_variables_dict(self):
        """Test that missing 'variables' key is initialized."""
        node = {
            "type": "var_decl",
            "value": "y",
            "data_type": "char",
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "current_scope": 1
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["scope_level"], 1)
    
    def test_initializes_missing_errors_list(self):
        """Test that missing 'errors' key is initialized."""
        node = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 5,
            "column": 3
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
    
    def test_char_data_type(self):
        """Test variable declaration with char data type."""
        node = {
            "type": "var_decl",
            "value": "c",
            "data_type": "char",
            "line": 20,
            "column": 10
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")
    
    def test_different_scope_levels(self):
        """Test variable declaration at different scope levels."""
        node = {
            "type": "var_decl",
            "value": "local_var",
            "data_type": "int",
            "line": 30,
            "column": 15
        }
        symbol_table = {
            "variables": {},
            "current_scope": 2
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["local_var"]["scope_level"], 2)
    
    def test_missing_line_column_defaults(self):
        """Test that missing line/column default to 0."""
        node = {
            "type": "var_decl",
            "value": "no_pos",
            "data_type": "int"
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["no_pos"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["no_pos"]["column"], 0)
    
    def test_empty_symbol_table(self):
        """Test with completely empty symbol table."""
        node = {
            "type": "var_decl",
            "value": "first_var",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table = {}
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("first_var", symbol_table["variables"])
    
    def test_multiple_variables_same_scope(self):
        """Test declaring multiple variables in the same scope."""
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }
        
        node1 = {
            "type": "var_decl",
            "value": "a",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        node2 = {
            "type": "var_decl",
            "value": "b",
            "data_type": "char",
            "line": 2,
            "column": 1
        }
        
        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_duplicate_after_multiple_declarations(self):
        """Test duplicate detection after multiple successful declarations."""
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }
        
        # Declare two variables
        _handle_var_decl({
            "type": "var_decl",
            "value": "var1",
            "data_type": "int",
            "line": 1,
            "column": 1
        }, symbol_table)
        
        _handle_var_decl({
            "type": "var_decl",
            "value": "var2",
            "data_type": "int",
            "line": 2,
            "column": 1
        }, symbol_table)
        
        # Try to duplicate var1
        _handle_var_decl({
            "type": "var_decl",
            "value": "var1",
            "data_type": "int",
            "line": 3,
            "column": 1
        }, symbol_table)
        
        self.assertEqual(len(symbol_table["variables"]), 2)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("duplicate variable declaration: var1", symbol_table["errors"][0]["message"])


if __name__ == "__main__":
    unittest.main()
