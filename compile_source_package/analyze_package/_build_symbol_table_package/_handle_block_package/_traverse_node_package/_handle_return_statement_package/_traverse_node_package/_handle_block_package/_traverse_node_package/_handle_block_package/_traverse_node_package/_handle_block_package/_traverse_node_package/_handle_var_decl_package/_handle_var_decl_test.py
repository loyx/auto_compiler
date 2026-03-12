import unittest

# Relative import from the same package
from ._handle_var_decl_src import _handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""
    
    def test_happy_path_with_name_field(self):
        """Test normal variable declaration with name field."""
        node = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["is_declared"], True)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
    
    def test_happy_path_with_value_field(self):
        """Test variable declaration with value field as fallback."""
        node = {
            "type": "var_decl",
            "value": "y",
            "data_type": "char",
            "line": 15,
            "column": 3
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["y"]["line"], 15)
    
    def test_extract_name_from_children(self):
        """Test variable name extraction from children[0]."""
        node = {
            "type": "var_decl",
            "children": [
                {"value": "z", "name": "z"}
            ],
            "data_type": "int",
            "line": 20,
            "column": 1
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["z"]["data_type"], "int")
    
    def test_extract_name_from_children_name_field(self):
        """Test variable name extraction from children[0] name field."""
        node = {
            "type": "var_decl",
            "children": [
                {"name": "w"}
            ],
            "data_type": "int",
            "line": 20,
            "column": 1
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("w", symbol_table["variables"])
    
    def test_invalid_var_name_error(self):
        """Test error when variable name cannot be extracted."""
        node = {
            "type": "var_decl",
            "data_type": "int",
            "line": 25,
            "column": 10
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "invalid_var_decl")
        self.assertEqual(symbol_table["errors"][0]["message"], "无法提取变量名")
        self.assertEqual(symbol_table["errors"][0]["line"], 25)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
        self.assertNotIn("variables", symbol_table)
    
    def test_invalid_data_type_defaults_to_int(self):
        """Test that invalid data type defaults to int."""
        node = {
            "type": "var_decl",
            "name": "a",
            "data_type": "float",
            "line": 30,
            "column": 2
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["a"]["data_type"], "int")
    
    def test_duplicate_declaration_error(self):
        """Test error when variable is declared twice in same scope."""
        node1 = {
            "type": "var_decl",
            "name": "dup",
            "data_type": "int",
            "line": 35,
            "column": 1
        }
        node2 = {
            "type": "var_decl",
            "name": "dup",
            "data_type": "int",
            "line": 36,
            "column": 1
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "duplicate_declaration")
        self.assertEqual(symbol_table["errors"][0]["message"], "变量 'dup' 已在当前作用域声明")
        self.assertIn("dup", symbol_table["variables"])
    
    def test_same_var_different_scope_allowed(self):
        """Test that same variable name in different scope is allowed."""
        node1 = {
            "type": "var_decl",
            "name": "scope_var",
            "data_type": "int",
            "line": 40,
            "column": 1
        }
        node2 = {
            "type": "var_decl",
            "name": "scope_var",
            "data_type": "char",
            "line": 45,
            "column": 1
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node1, symbol_table)
        symbol_table["current_scope"] = 1
        _handle_var_decl(node2, symbol_table)
        
        self.assertEqual(len(symbol_table.get("errors", [])), 0)
        self.assertEqual(symbol_table["variables"]["scope_var"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["scope_var"]["scope_level"], 1)
    
    def test_missing_symbol_table_fields_created(self):
        """Test that missing symbol_table fields are created."""
        node = {
            "type": "var_decl",
            "name": "new_var",
            "data_type": "int",
            "line": 50,
            "column": 1
        }
        symbol_table = {}
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("new_var", symbol_table["variables"])
    
    def test_missing_line_column_defaults_to_zero(self):
        """Test that missing line/column default to 0."""
        node = {
            "type": "var_decl",
            "name": "no_pos"
        }
        symbol_table = {}
        
        _handle_var_decl(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["no_pos"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["no_pos"]["column"], 0)
    
    def test_missing_current_scope_defaults_to_zero(self):
        """Test that missing current_scope defaults to 0."""
        node = {
            "type": "var_decl",
            "name": "no_scope",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table = {}
        
        _handle_var_decl(node, symbol_table)
        
        self.assertEqual(symbol_table["variables"]["no_scope"]["scope_level"], 0)
    
    def test_children_empty_list(self):
        """Test when children is empty list."""
        node = {
            "type": "var_decl",
            "children": [],
            "data_type": "int",
            "line": 55,
            "column": 1
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["errors"][0]["type"], "invalid_var_decl")
    
    def test_children_first_not_dict(self):
        """Test when children[0] is not a dict."""
        node = {
            "type": "var_decl",
            "children": ["not_a_dict"],
            "data_type": "int",
            "line": 60,
            "column": 1
        }
        symbol_table = {
            "current_scope": 0
        }
        
        _handle_var_decl(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(symbol_table["errors"][0]["type"], "invalid_var_decl")


if __name__ == "__main__":
    unittest.main()
