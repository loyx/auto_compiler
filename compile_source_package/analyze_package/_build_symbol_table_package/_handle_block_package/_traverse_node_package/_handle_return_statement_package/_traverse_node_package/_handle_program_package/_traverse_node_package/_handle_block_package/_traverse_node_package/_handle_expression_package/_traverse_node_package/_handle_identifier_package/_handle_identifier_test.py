import unittest

# Relative import from the current package
from ._handle_identifier_src import _handle_identifier


class TestHandleIdentifier(unittest.TestCase):
    """Test cases for _handle_identifier function."""
    
    def test_variable_declared_no_error(self):
        """Test that no error is added when variable is declared."""
        node = {
            "type": "identifier",
            "value": "myVar",
            "line": 10,
            "column": 5
        }
        
        symbol_table = {
            "variables": {
                "myVar": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }
        
        _handle_identifier(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_variable_not_declared_error_added(self):
        """Test that error is added when variable is not declared."""
        node = {
            "type": "identifier",
            "value": "undefinedVar",
            "line": 10,
            "column": 5
        }
        
        symbol_table = {
            "variables": {
                "otherVar": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }
        
        _handle_identifier(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "undefined_variable")
        self.assertIn("undefinedVar", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        self.assertEqual(error["node_type"], "identifier")
    
    def test_empty_var_name_early_return(self):
        """Test that function returns early when var_name is empty."""
        node = {
            "type": "identifier",
            "value": "",
            "line": 10,
            "column": 5
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_identifier(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_none_var_name_early_return(self):
        """Test that function returns early when var_name is None."""
        node = {
            "type": "identifier",
            "value": None,
            "line": 10,
            "column": 5
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_identifier(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_missing_errors_list_creates_it(self):
        """Test that errors list is created if missing from symbol_table."""
        node = {
            "type": "identifier",
            "value": "undefinedVar",
            "line": 10,
            "column": 5
        }
        
        symbol_table = {
            "variables": {}
        }
        
        _handle_identifier(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_missing_variables_dict_creates_it(self):
        """Test that variables dict is created if missing from symbol_table."""
        node = {
            "type": "identifier",
            "value": "undefinedVar",
            "line": 10,
            "column": 5
        }
        
        symbol_table = {
            "errors": []
        }
        
        _handle_identifier(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_missing_both_errors_and_variables(self):
        """Test handling when both errors and variables are missing."""
        node = {
            "type": "identifier",
            "value": "undefinedVar",
            "line": 10,
            "column": 5
        }
        
        symbol_table = {}
        
        _handle_identifier(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertIn("variables", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_error_record_structure(self):
        """Test that error record has correct structure."""
        node = {
            "type": "identifier",
            "value": "testVar",
            "line": 25,
            "column": 12
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_identifier(node, symbol_table)
        
        error = symbol_table["errors"][0]
        
        self.assertIn("type", error)
        self.assertIn("message", error)
        self.assertIn("line", error)
        self.assertIn("column", error)
        self.assertIn("node_type", error)
        
        self.assertEqual(error["type"], "undefined_variable")
        self.assertEqual(error["line"], 25)
        self.assertEqual(error["column"], 12)
        self.assertEqual(error["node_type"], "identifier")
    
    def test_multiple_undefined_variables(self):
        """Test that multiple undefined variables add multiple errors."""
        node1 = {
            "type": "identifier",
            "value": "var1",
            "line": 10,
            "column": 5
        }
        
        node2 = {
            "type": "identifier",
            "value": "var2",
            "line": 11,
            "column": 8
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_identifier(node1, symbol_table)
        _handle_identifier(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertIn("var1", symbol_table["errors"][0]["message"])
        self.assertIn("var2", symbol_table["errors"][1]["message"])
    
    def test_mixed_declared_and_undefined(self):
        """Test mix of declared and undefined variables."""
        node1 = {
            "type": "identifier",
            "value": "declaredVar",
            "line": 10,
            "column": 5
        }
        
        node2 = {
            "type": "identifier",
            "value": "undefinedVar",
            "line": 11,
            "column": 8
        }
        
        symbol_table = {
            "variables": {
                "declaredVar": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }
        
        _handle_identifier(node1, symbol_table)
        _handle_identifier(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("undefinedVar", symbol_table["errors"][0]["message"])
    
    def test_missing_line_column_in_node(self):
        """Test handling when line/column are missing from node."""
        node = {
            "type": "identifier",
            "value": "undefinedVar"
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_identifier(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)


if __name__ == "__main__":
    unittest.main()
