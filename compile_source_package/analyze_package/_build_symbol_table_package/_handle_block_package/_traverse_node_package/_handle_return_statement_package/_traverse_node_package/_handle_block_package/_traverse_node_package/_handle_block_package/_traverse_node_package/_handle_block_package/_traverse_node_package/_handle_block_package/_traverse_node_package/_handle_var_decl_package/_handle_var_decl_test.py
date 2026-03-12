import unittest

# Relative import from the same package
from ._handle_var_decl_src import _handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""
    
    def test_happy_path_new_variable(self):
        """Test successful registration of a new variable declaration."""
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
    
    def test_duplicate_declaration(self):
        """Test that duplicate variable declaration records an error."""
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
        
        # Variable should not be overwritten
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        
        # Error should be recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "duplicate_declaration")
        self.assertIn("x", error["message"])
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertEqual(error["variable"], "x")
    
    def test_missing_variables_key_in_symbol_table(self):
        """Test that function creates variables key if missing."""
        node = {
            "type": "var_decl",
            "value": "y",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table = {
            "current_scope": 1
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "char")
    
    def test_missing_errors_key_in_symbol_table(self):
        """Test that function creates errors key if missing (for duplicate case)."""
        node = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 25,
            "column": 10
        }
        symbol_table = {
            "variables": {
                "z": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_custom_scope_level(self):
        """Test variable registration with custom scope level."""
        node = {
            "type": "var_decl",
            "value": "local_var",
            "data_type": "int",
            "line": 30,
            "column": 7
        }
        symbol_table = {
            "variables": {},
            "current_scope": 3
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["local_var"]["scope_level"], 3)
    
    def test_node_missing_optional_fields(self):
        """Test handling of node with missing optional fields."""
        node = {
            "type": "var_decl",
            "value": "incomplete"
            # Missing data_type, line, column
        }
        symbol_table = {
            "variables": {},
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("incomplete", symbol_table["variables"])
        self.assertIsNone(symbol_table["variables"]["incomplete"]["data_type"])
        self.assertIsNone(symbol_table["variables"]["incomplete"]["line"])
        self.assertIsNone(symbol_table["variables"]["incomplete"]["column"])
    
    def test_multiple_variables_same_scope(self):
        """Test registering multiple variables in the same scope."""
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
    
    def test_default_scope_level(self):
        """Test that default scope level is 0 when current_scope is missing."""
        node = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {}
            # Missing current_scope
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)


if __name__ == "__main__":
    unittest.main()
