import unittest

from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""
    
    def test_variable_exists_no_error(self):
        """Test when variable exists in symbol table - no error should be recorded."""
        node = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5
        }
        
        symbol_table = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 1
                }
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_variable_not_declared_error_recorded(self):
        """Test when variable is not declared - error should be recorded."""
        node = {
            "type": "assignment",
            "value": "y",
            "line": 15,
            "column": 8
        }
        
        symbol_table = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 1
                }
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "undeclared_variable_assignment")
        self.assertIn("y", error["message"])
        self.assertEqual(error["variable"], "y")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
    
    def test_errors_list_created_if_missing(self):
        """Test that errors list is created if not present in symbol_table."""
        node = {
            "type": "assignment",
            "value": "z",
            "line": 20,
            "column": 3
        }
        
        symbol_table = {
            "variables": {}
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_variables_dict_missing_treated_as_empty(self):
        """Test when variables dict is missing - should be treated as empty."""
        node = {
            "type": "assignment",
            "value": "a",
            "line": 25,
            "column": 10
        }
        
        symbol_table = {
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["variable"], "a")
    
    def test_node_missing_line_uses_default(self):
        """Test when node is missing line field - should use default value 0."""
        node = {
            "type": "assignment",
            "value": "b",
            "column": 7
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
    
    def test_node_missing_column_uses_default(self):
        """Test when node is missing column field - should use default value 0."""
        node = {
            "type": "assignment",
            "value": "c",
            "line": 30
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(symbol_table["errors"][0]["column"], 0)
    
    def test_node_missing_value_uses_none(self):
        """Test when node is missing value field - should use None as variable name."""
        node = {
            "type": "assignment",
            "line": 35,
            "column": 12
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIsNone(symbol_table["errors"][0]["variable"])
        self.assertIn("None", symbol_table["errors"][0]["message"])
    
    def test_empty_variable_name(self):
        """Test when variable name is empty string."""
        node = {
            "type": "assignment",
            "value": "",
            "line": 40,
            "column": 1
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["variable"], "")
    
    def test_multiple_undeclared_variables(self):
        """Test multiple assignments to undeclared variables - all errors recorded."""
        node1 = {
            "type": "assignment",
            "value": "x",
            "line": 45,
            "column": 1
        }
        
        node2 = {
            "type": "assignment",
            "value": "y",
            "line": 46,
            "column": 2
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["variable"], "x")
        self.assertEqual(symbol_table["errors"][1]["variable"], "y")
    
    def test_mixed_declared_and_undeclared(self):
        """Test mix of declared and undeclared variables."""
        node1 = {
            "type": "assignment",
            "value": "declared_var",
            "line": 50,
            "column": 1
        }
        
        node2 = {
            "type": "assignment",
            "value": "undeclared_var",
            "line": 51,
            "column": 2
        }
        
        symbol_table = {
            "variables": {
                "declared_var": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 1
                }
            },
            "errors": []
        }
        
        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["variable"], "undeclared_var")
    
    def test_symbol_table_not_modified_when_variable_exists(self):
        """Test that symbol_table variables dict is not modified when variable exists."""
        node = {
            "type": "assignment",
            "value": "existing",
            "line": 55,
            "column": 5
        }
        
        original_var_info = {
            "data_type": "char",
            "is_declared": True,
            "line": 10,
            "column": 1,
            "scope_level": 1
        }
        
        symbol_table = {
            "variables": {
                "existing": original_var_info.copy()
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["existing"], original_var_info)
    
    def test_complete_symbol_table_structure(self):
        """Test with complete symbol_table structure including all optional fields."""
        node = {
            "type": "assignment",
            "value": "test_var",
            "line": 60,
            "column": 10
        }
        
        symbol_table = {
            "variables": {
                "test_var": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 1
                }
            },
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [0],
            "current_function": "main",
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["current_function"], "main")


if __name__ == "__main__":
    unittest.main()
