import unittest

# Relative import from the same package
from ._handle_variable_declaration_src import _handle_variable_declaration


class TestHandleVariableDeclaration(unittest.TestCase):
    """Test cases for _handle_variable_declaration function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_node = {
            "type": "variable_declaration",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 5
        }
        self.base_symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "current_function": None,
            "errors": []
        }
    
    def test_register_new_variable(self):
        """Test successful registration of a new variable."""
        node = self.base_node.copy()
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        _handle_variable_declaration(node, symbol_table)
        
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_duplicate_variable_same_scope(self):
        """Test duplicate variable detection at same scope level."""
        node1 = self.base_node.copy()
        node2 = self.base_node.copy()
        node2["line"] = 5
        
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        _handle_variable_declaration(node1, symbol_table)
        _handle_variable_declaration(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("already declared", symbol_table["errors"][0])
        self.assertIn("line 1", symbol_table["errors"][0])
        self.assertIn("column 5", symbol_table["errors"][0])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)
    
    def test_same_variable_different_scope(self):
        """Test same variable name allowed at different scope levels."""
        node1 = self.base_node.copy()
        node2 = self.base_node.copy()
        node2["line"] = 10
        
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        symbol_table["current_scope"] = 0
        
        _handle_variable_declaration(node1, symbol_table)
        
        symbol_table["current_scope"] = 1
        _handle_variable_declaration(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
    
    def test_extract_name_from_value_field(self):
        """Test variable name extraction from 'value' field when 'name' is missing."""
        node = {
            "type": "variable_declaration",
            "value": "y",
            "data_type": "string",
            "line": 3,
            "column": 10
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        _handle_variable_declaration(node, symbol_table)
        
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "string")
    
    def test_missing_node_fields(self):
        """Test handling of node with missing optional fields."""
        node = {
            "type": "variable_declaration",
            "name": "z"
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        _handle_variable_declaration(node, symbol_table)
        
        self.assertIn("z", symbol_table["variables"])
        self.assertIsNone(symbol_table["variables"]["z"]["data_type"])
        self.assertEqual(symbol_table["variables"]["z"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["z"]["column"], 0)
    
    def test_missing_symbol_table_fields(self):
        """Test handling when symbol_table is missing required fields."""
        node = self.base_node.copy()
        symbol_table = {}
        
        _handle_variable_declaration(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("x", symbol_table["variables"])
    
    def test_is_declared_flag(self):
        """Test that is_declared flag is set to True."""
        node = self.base_node.copy()
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        _handle_variable_declaration(node, symbol_table)
        
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
    
    def test_error_message_format(self):
        """Test the format of duplicate declaration error message."""
        node1 = self.base_node.copy()
        node2 = self.base_node.copy()
        node2["line"] = 15
        
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        _handle_variable_declaration(node1, symbol_table)
        _handle_variable_declaration(node2, symbol_table)
        
        error_msg = symbol_table["errors"][0]
        self.assertIn("Error:", error_msg)
        self.assertIn("'x'", error_msg)
        self.assertIn("line 1", error_msg)
        self.assertIn("column 5", error_msg)
    
    def test_multiple_variables_different_names(self):
        """Test registering multiple variables with different names."""
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        node1 = self.base_node.copy()
        node1["name"] = "a"
        
        node2 = self.base_node.copy()
        node2["name"] = "b"
        node2["line"] = 2
        
        node3 = self.base_node.copy()
        node3["name"] = "c"
        node3["line"] = 3
        
        _handle_variable_declaration(node1, symbol_table)
        _handle_variable_declaration(node2, symbol_table)
        _handle_variable_declaration(node3, symbol_table)
        
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_no_side_effects_on_error(self):
        """Test that duplicate declaration doesn't modify existing variable."""
        node1 = self.base_node.copy()
        node1["data_type"] = "int"
        
        node2 = self.base_node.copy()
        node2["data_type"] = "float"
        node2["line"] = 10
        
        symbol_table = self.base_symbol_table.copy()
        symbol_table["variables"] = {}
        symbol_table["errors"] = []
        
        _handle_variable_declaration(node1, symbol_table)
        
        _handle_variable_declaration(node2, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)
        self.assertEqual(len(symbol_table["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
