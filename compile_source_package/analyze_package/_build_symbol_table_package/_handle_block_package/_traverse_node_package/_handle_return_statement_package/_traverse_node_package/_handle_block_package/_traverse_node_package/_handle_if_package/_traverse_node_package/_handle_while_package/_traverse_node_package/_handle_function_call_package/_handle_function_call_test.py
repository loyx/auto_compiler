import unittest

# Relative import from the same package
from ._handle_function_call_src import _handle_function_call


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""
    
    def test_function_declared_no_error(self):
        """Test that no error is recorded when function is declared."""
        node = {
            "type": "function_call",
            "value": "my_function",
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "functions": {
                "my_function": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_function_not_declared_error_recorded(self):
        """Test that error is recorded when function is not declared."""
        node = {
            "type": "function_call",
            "value": "undefined_function",
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "functions": {},
            "errors": []
        }
        
        _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertIn("undefined_function", error["message"])
    
    def test_symbol_table_missing_errors_key(self):
        """Test that errors list is created if not present."""
        node = {
            "type": "function_call",
            "value": "test_func",
            "line": 5,
            "column": 2
        }
        symbol_table = {
            "functions": {}
        }
        
        _handle_function_call(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_symbol_table_missing_functions_key(self):
        """Test that functions dict is created if not present."""
        node = {
            "type": "function_call",
            "value": "another_func",
            "line": 7,
            "column": 3
        }
        symbol_table = {}
        
        _handle_function_call(node, symbol_table)
        
        self.assertIn("functions", symbol_table)
        self.assertIsInstance(symbol_table["functions"], dict)
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_node_missing_line_column_defaults_to_zero(self):
        """Test that line and column default to 0 when not present."""
        node = {
            "type": "function_call",
            "value": "missing_coords"
        }
        symbol_table = {
            "functions": {}
        }
        
        _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)
    
    def test_node_missing_value_none_func_name(self):
        """Test behavior when node has no value (func_name is None)."""
        node = {
            "type": "function_call",
            "line": 12,
            "column": 4
        }
        symbol_table = {
            "functions": {}
        }
        
        _handle_function_call(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 12)
        self.assertEqual(error["column"], 4)
        self.assertIn("None", error["message"])
    
    def test_multiple_undeclared_functions_multiple_errors(self):
        """Test that multiple undeclared function calls create multiple errors."""
        symbol_table = {
            "functions": {}
        }
        
        node1 = {
            "type": "function_call",
            "value": "func1",
            "line": 1,
            "column": 1
        }
        node2 = {
            "type": "function_call",
            "value": "func2",
            "line": 2,
            "column": 2
        }
        
        _handle_function_call(node1, symbol_table)
        _handle_function_call(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["line"], 1)
        self.assertEqual(symbol_table["errors"][1]["line"], 2)


if __name__ == "__main__":
    unittest.main()
