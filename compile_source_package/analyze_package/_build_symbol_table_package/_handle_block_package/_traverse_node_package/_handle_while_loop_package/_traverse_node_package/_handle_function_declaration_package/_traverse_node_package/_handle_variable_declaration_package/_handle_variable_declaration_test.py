import unittest
from unittest.mock import patch, MagicMock
import sys

# Pre-mock the circular dependency before any imports
# This prevents the actual import chain that causes circular import
sys.modules['main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src'] = MagicMock()

# Relative import from the same package
from ._handle_variable_declaration_src import _handle_variable_declaration


class TestHandleVariableDeclaration(unittest.TestCase):
    
    def test_happy_path_with_initial_value(self):
        """Test variable declaration with initial value - should register and traverse"""
        node = {
            "type": "variable_declaration",
            "name": "x",
            "var_type": "int",
            "initial_value": {"type": "literal", "value": 42},
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        with patch("._handle_variable_declaration_src._traverse_node") as mock_traverse:
            _handle_variable_declaration(node, symbol_table)
        
        # Verify variable was registered
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["initial_value"], {"type": "literal", "value": 42})
        
        # Verify _traverse_node was called with initial_value
        mock_traverse.assert_called_once_with({"type": "literal", "value": 42}, symbol_table)
    
    def test_without_initial_value(self):
        """Test variable declaration without initial value - should not traverse"""
        node = {
            "type": "variable_declaration",
            "name": "y",
            "var_type": "str",
            "initial_value": None,
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        with patch("._handle_variable_declaration_src._traverse_node") as mock_traverse:
            _handle_variable_declaration(node, symbol_table)
        
        # Verify variable was registered
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["type"], "str")
        self.assertEqual(symbol_table["variables"]["y"]["line"], 15)
        self.assertEqual(symbol_table["variables"]["y"]["column"], 8)
        self.assertIsNone(symbol_table["variables"]["y"]["initial_value"])
        
        # Verify _traverse_node was NOT called
        mock_traverse.assert_not_called()
    
    def test_creates_variables_dict_if_missing(self):
        """Test that variables dict is created if not present in symbol_table"""
        node = {
            "type": "variable_declaration",
            "name": "z",
            "var_type": "float",
            "initial_value": None,
            "line": 20,
            "column": 3
        }
        symbol_table = {
            "functions": {},
            "current_scope": 0
        }
        
        _handle_variable_declaration(node, symbol_table)
        
        # Verify variables dict was created
        self.assertIn("variables", symbol_table)
        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["z"]["type"], "float")
    
    def test_multiple_variables_sequential(self):
        """Test registering multiple variables sequentially"""
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        node1 = {
            "type": "variable_declaration",
            "name": "a",
            "var_type": "int",
            "initial_value": None,
            "line": 1,
            "column": 1
        }
        node2 = {
            "type": "variable_declaration",
            "name": "b",
            "var_type": "str",
            "initial_value": None,
            "line": 2,
            "column": 2
        }
        
        with patch("._handle_variable_declaration_src._traverse_node"):
            _handle_variable_declaration(node1, symbol_table)
            _handle_variable_declaration(node2, symbol_table)
        
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertEqual(len(symbol_table["variables"]), 2)
        self.assertEqual(symbol_table["variables"]["a"]["type"], "int")
        self.assertEqual(symbol_table["variables"]["b"]["type"], "str")
    
    def test_minimal_node_fields(self):
        """Test with minimal required fields only (name and var_type)"""
        node = {
            "name": "minimal",
            "var_type": "any"
        }
        symbol_table = {"variables": {}}
        
        _handle_variable_declaration(node, symbol_table)
        
        self.assertIn("minimal", symbol_table["variables"])
        self.assertIsNone(symbol_table["variables"]["minimal"]["line"])
        self.assertIsNone(symbol_table["variables"]["minimal"]["column"])
        self.assertIsNone(symbol_table["variables"]["minimal"]["initial_value"])
    
    def test_complex_initial_value_expression(self):
        """Test with complex initial value expression - should traverse recursively"""
        node = {
            "type": "variable_declaration",
            "name": "result",
            "var_type": "int",
            "initial_value": {
                "type": "binary_op",
                "operator": "+",
                "left": {"type": "literal", "value": 10},
                "right": {"type": "literal", "value": 20}
            },
            "line": 5,
            "column": 10
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        with patch("._handle_variable_declaration_src._traverse_node") as mock_traverse:
            _handle_variable_declaration(node, symbol_table)
        
        # Verify variable registration
        self.assertIn("result", symbol_table["variables"])
        
        # Verify _traverse_node was called with the complex expression
        mock_traverse.assert_called_once()
        call_args = mock_traverse.call_args
        self.assertEqual(call_args[0][0]["type"], "binary_op")
        self.assertEqual(call_args[0][0]["operator"], "+")
    
    def test_variable_overwrite(self):
        """Test that declaring same variable twice overwrites the first"""
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        
        node1 = {
            "type": "variable_declaration",
            "name": "x",
            "var_type": "int",
            "initial_value": None,
            "line": 1,
            "column": 1
        }
        node2 = {
            "type": "variable_declaration",
            "name": "x",
            "var_type": "str",
            "initial_value": None,
            "line": 5,
            "column": 5
        }
        
        with patch("._handle_variable_declaration_src._traverse_node"):
            _handle_variable_declaration(node1, symbol_table)
            _handle_variable_declaration(node2, symbol_table)
        
        # Second declaration should overwrite
        self.assertEqual(symbol_table["variables"]["x"]["type"], "str")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
    
    def test_traverse_node_exception_propagation(self):
        """Test that exceptions from _traverse_node propagate correctly"""
        node = {
            "type": "variable_declaration",
            "name": "x",
            "var_type": "int",
            "initial_value": {"type": "invalid"},
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}}
        
        with patch("._handle_variable_declaration_src._traverse_node") as mock_traverse:
            mock_traverse.side_effect = ValueError("Invalid expression")
            
            with self.assertRaises(ValueError) as context:
                _handle_variable_declaration(node, symbol_table)
            
            self.assertEqual(str(context.exception), "Invalid expression")
        
        # Variable should still be registered before exception
        self.assertIn("x", symbol_table["variables"])


if __name__ == "__main__":
    unittest.main()
