import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._handle_function_declaration_src import _handle_function_declaration

# Type aliases matching the source
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionDeclaration(unittest.TestCase):
    """Test cases for _handle_function_declaration function"""

    def _create_symbol_table(self) -> SymbolTable:
        """Helper to create a fresh symbol table"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_function_declaration_with_parameters(self):
        """Test handling normal function declaration with parameters"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "foo"},
                {"type": "parameter", "value": "x", "data_type": "int"},
                {"type": "parameter", "value": "y", "data_type": "char"}
            ]
        }

        symbol_table = self._create_symbol_table()

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        # Verify function registered
        self.assertIn("foo", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["foo"]["return_type"], "int")
        self.assertEqual(len(symbol_table["functions"]["foo"]["params"]), 2)
        self.assertEqual(symbol_table["functions"]["foo"]["params"][0]["name"], "x")
        self.assertEqual(symbol_table["functions"]["foo"]["params"][1]["name"], "y")

        # Verify scope management
        self.assertEqual(symbol_table["current_scope"], 0)  # Restored
        self.assertEqual(len(symbol_table["scope_stack"]), 0)  # Restored
        self.assertIsNone(symbol_table["current_function"])  # Restored

        # Verify parameters in variables
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "char")

        # Verify _traverse_node called for all children
        self.assertEqual(mock_traverse.call_count, 3)

    def test_function_declaration_without_parameters(self):
        """Test handling function declaration without parameters"""
        node = {
            "type": "function_declaration",
            "data_type": "char",
            "line": 5,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "main"}
            ]
        }

        symbol_table = self._create_symbol_table()

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        # Verify function registered
        self.assertIn("main", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["main"]["return_type"], "char")
        self.assertEqual(symbol_table["functions"]["main"]["params"], [])

        # Verify scope management
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(len(symbol_table["scope_stack"]), 0)
        self.assertIsNone(symbol_table["current_function"])

        # Verify _traverse_node called
        self.assertEqual(mock_traverse.call_count, 1)

    def test_duplicate_function_declaration(self):
        """Test handling duplicate function declaration"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 10,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "foo"}
            ]
        }

        symbol_table = self._create_symbol_table()
        # Pre-register the function
        symbol_table["functions"]["foo"] = {
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 1
        }

        _handle_function_declaration(node, symbol_table)

        # Verify error added
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "duplicate_function")
        self.assertIn("foo", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 1)

        # Verify function info not overwritten
        self.assertEqual(symbol_table["functions"]["foo"]["line"], 1)

        # Verify scope unchanged
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(len(symbol_table["scope_stack"]), 0)

    def test_missing_function_name(self):
        """Test handling node without identifier child"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 15,
            "column": 1,
            "children": [
                {"type": "other_type", "value": "something"}
            ]
        }

        symbol_table = self._create_symbol_table()
        initial_scope = symbol_table["current_scope"]

        _handle_function_declaration(node, symbol_table)

        # Verify no function registered
        self.assertEqual(len(symbol_table["functions"]), 0)
        # Verify scope unchanged
        self.assertEqual(symbol_table["current_scope"], initial_scope)
        # Verify no errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_traverse_node_called_for_children(self):
        """Test that _traverse_node is called for all children"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 20,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "bar"},
                {"type": "parameter", "value": "x", "data_type": "int"},
                {"type": "block", "value": None}
            ]
        }

        symbol_table = self._create_symbol_table()

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_declaration(node, symbol_table)

        # _traverse_node should be called for each child
        self.assertEqual(mock_traverse.call_count, 3)

    def test_scope_management(self):
        """Test scope stack management"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 25,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "scoped_func"}
            ]
        }

        symbol_table = self._create_symbol_table()
        initial_scope = symbol_table["current_scope"]
        initial_stack = list(symbol_table["scope_stack"])

        _handle_function_declaration(node, symbol_table)

        # Verify scope restored
        self.assertEqual(symbol_table["current_scope"], initial_scope)
        self.assertEqual(symbol_table["scope_stack"], initial_stack)

    def test_current_function_restoration(self):
        """Test current_function is restored after processing"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 30,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "temp_func"}
            ]
        }

        symbol_table = self._create_symbol_table()
        symbol_table["current_function"] = "outer_func"

        _handle_function_declaration(node, symbol_table)

        # Verify current_function restored to previous value
        self.assertEqual(symbol_table["current_function"], "outer_func")

    def test_parameter_variable_registration(self):
        """Test parameters are registered in variables"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 35,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "param_func"},
                {"type": "parameter", "value": "a", "data_type": "int"},
                {"type": "parameter", "value": "b", "data_type": "char"}
            ]
        }

        symbol_table = self._create_symbol_table()

        _handle_function_declaration(node, symbol_table)

        # Verify parameters in variables
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["a"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["b"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["a"]["is_declared"], True)
        self.assertEqual(symbol_table["variables"]["a"]["scope_level"], 1)

    def test_multiple_parameters(self):
        """Test function with multiple parameters"""
        node = {
            "type": "function_declaration",
            "data_type": "void",
            "line": 40,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "multi_param"},
                {"type": "parameter", "value": "x", "data_type": "int"},
                {"type": "parameter", "value": "y", "data_type": "int"},
                {"type": "parameter", "value": "z", "data_type": "char"}
            ]
        }

        symbol_table = self._create_symbol_table()

        _handle_function_declaration(node, symbol_table)

        # Verify all parameters registered
        params = symbol_table["functions"]["multi_param"]["params"]
        self.assertEqual(len(params), 3)
        self.assertEqual(params[0]["name"], "x")
        self.assertEqual(params[1]["name"], "y")
        self.assertEqual(params[2]["name"], "z")

    def test_line_column_preserved(self):
        """Test that line and column information is preserved"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 100,
            "column": 25,
            "children": [
                {"type": "identifier", "value": "positioned_func"}
            ]
        }

        symbol_table = self._create_symbol_table()

        _handle_function_declaration(node, symbol_table)

        # Verify line and column in function info
        self.assertEqual(symbol_table["functions"]["positioned_func"]["line"], 100)
        self.assertEqual(symbol_table["functions"]["positioned_func"]["column"], 25)

    def test_default_return_type(self):
        """Test default return type when data_type not specified"""
        node = {
            "type": "function_declaration",
            "line": 45,
            "column": 1,
            "children": [
                {"type": "identifier", "value": "default_type_func"}
            ]
        }

        symbol_table = self._create_symbol_table()

        _handle_function_declaration(node, symbol_table)

        # Verify default return type is "int"
        self.assertEqual(symbol_table["functions"]["default_type_func"]["return_type"], "int")

    def test_empty_children_list(self):
        """Test handling node with empty children list"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 50,
            "column": 1,
            "children": []
        }

        symbol_table = self._create_symbol_table()

        _handle_function_declaration(node, symbol_table)

        # No function name, should return early
        self.assertEqual(len(symbol_table["functions"]), 0)


if __name__ == "__main__":
    unittest.main()
