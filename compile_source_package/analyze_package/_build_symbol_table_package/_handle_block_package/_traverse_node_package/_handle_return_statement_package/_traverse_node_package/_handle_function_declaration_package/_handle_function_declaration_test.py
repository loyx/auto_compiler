# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch, MagicMock

# === sub function imports ===
from ._handle_function_declaration_src import _handle_function_declaration

# === Type aliases for test clarity ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionDeclaration(unittest.TestCase):
    """Test cases for _handle_function_declaration function."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_traverse_node = MagicMock()

    def _create_mock_patch(self):
        """Create patch for _traverse_node dependency."""
        return patch(
            "projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_function_declaration_package._handle_function_declaration_src._traverse_node",
            self.mock_traverse_node
        )

    def test_basic_function_declaration(self):
        """Test basic function declaration with name from value field."""
        node: AST = {
            "type": "function_declaration",
            "value": "myFunction",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        # Verify function registered
        self.assertIn("functions", symbol_table)
        self.assertIn("myFunction", symbol_table["functions"])
        func_info = symbol_table["functions"]["myFunction"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)
        self.assertEqual(func_info["params"], [])
        
        # Verify current_function set
        self.assertEqual(symbol_table["current_function"], "myFunction")
        
        # Verify _traverse_node not called (no block children)
        self.mock_traverse_node.assert_not_called()

    def test_function_name_from_identifier_child(self):
        """Test function name extraction from identifier child when value is empty."""
        node: AST = {
            "type": "function_declaration",
            "value": None,
            "data_type": "char",
            "line": 20,
            "column": 3,
            "children": [
                {"type": "identifier", "value": "funcFromChild"},
                {"type": "other", "value": "ignored"}
            ]
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        # Verify function registered with name from identifier child
        self.assertIn("funcFromChild", symbol_table["functions"])
        func_info = symbol_table["functions"]["funcFromChild"]
        self.assertEqual(func_info["return_type"], "char")

    def test_function_with_parameters(self):
        """Test function declaration with parameters."""
        node: AST = {
            "type": "function_declaration",
            "value": "funcWithParams",
            "data_type": "int",
            "line": 30,
            "column": 1,
            "children": [
                {"type": "parameter", "value": "param1", "data_type": "int"},
                {"type": "parameter", "value": "param2", "data_type": "char"},
                {"type": "other", "value": "ignored"}
            ]
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        func_info = symbol_table["functions"]["funcWithParams"]
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "param1")
        self.assertEqual(func_info["params"][0]["data_type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "param2")
        self.assertEqual(func_info["params"][1]["data_type"], "char")

    def test_function_without_parameters(self):
        """Test function declaration without any parameters."""
        node: AST = {
            "type": "function_declaration",
            "value": "noParams",
            "data_type": "int",
            "line": 40,
            "column": 2,
            "children": [
                {"type": "other", "value": "not_a_param"}
            ]
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        func_info = symbol_table["functions"]["noParams"]
        self.assertEqual(func_info["params"], [])

    def test_duplicate_function_declaration(self):
        """Test duplicate function declaration records error."""
        node1: AST = {
            "type": "function_declaration",
            "value": "duplicateFunc",
            "data_type": "int",
            "line": 50,
            "column": 1,
            "children": []
        }
        node2: AST = {
            "type": "function_declaration",
            "value": "duplicateFunc",
            "data_type": "char",
            "line": 60,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node1, symbol_table)
            _handle_function_declaration(node2, symbol_table)

        # Verify error recorded
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("duplicateFunc", symbol_table["errors"][0])
        self.assertIn("60", symbol_table["errors"][0])
        
        # Verify original function info preserved
        func_info = symbol_table["functions"]["duplicateFunc"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["line"], 50)

    def test_block_children_traversal(self):
        """Test that block children are traversed with _traverse_node."""
        block_child = {"type": "block", "value": "body"}
        node: AST = {
            "type": "function_declaration",
            "value": "funcWithBlock",
            "data_type": "int",
            "line": 70,
            "column": 1,
            "children": [
                {"type": "parameter", "value": "p", "data_type": "int"},
                block_child,
                {"type": "other", "value": "not_block"}
            ]
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        # Verify _traverse_node called once for block child
        self.mock_traverse_node.assert_called_once()
        call_args = self.mock_traverse_node.call_args
        self.assertEqual(call_args[0][0], block_child)
        self.assertEqual(call_args[0][1], symbol_table)

    def test_multiple_block_children_traversal(self):
        """Test that multiple block children are all traversed."""
        node: AST = {
            "type": "function_declaration",
            "value": "multiBlock",
            "data_type": "int",
            "line": 80,
            "column": 1,
            "children": [
                {"type": "block", "value": "block1"},
                {"type": "block", "value": "block2"},
                {"type": "block", "value": "block3"}
            ]
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        # Verify _traverse_node called 3 times
        self.assertEqual(self.mock_traverse_node.call_count, 3)

    def test_default_return_type(self):
        """Test default return type is 'int' when data_type not specified."""
        node: AST = {
            "type": "function_declaration",
            "value": "defaultReturn",
            "line": 90,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        func_info = symbol_table["functions"]["defaultReturn"]
        self.assertEqual(func_info["return_type"], "int")

    def test_default_parameter_type(self):
        """Test default parameter type is 'int' when data_type not specified."""
        node: AST = {
            "type": "function_declaration",
            "value": "defaultParamType",
            "data_type": "int",
            "line": 100,
            "column": 1,
            "children": [
                {"type": "parameter", "value": "p"}
            ]
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        func_info = symbol_table["functions"]["defaultParamType"]
        self.assertEqual(func_info["params"][0]["data_type"], "int")

    def test_existing_functions_dict_preserved(self):
        """Test that existing functions dict is preserved when adding new function."""
        node: AST = {
            "type": "function_declaration",
            "value": "newFunc",
            "data_type": "int",
            "line": 110,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {
            "functions": {
                "existingFunc": {"return_type": "char", "params": [], "line": 1, "column": 1}
            }
        }

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        # Verify both functions exist
        self.assertIn("existingFunc", symbol_table["functions"])
        self.assertIn("newFunc", symbol_table["functions"])

    def test_existing_errors_list_preserved(self):
        """Test that existing errors list is preserved when recording duplicate."""
        node1: AST = {
            "type": "function_declaration",
            "value": "func1",
            "data_type": "int",
            "line": 120,
            "column": 1,
            "children": []
        }
        node2: AST = {
            "type": "function_declaration",
            "value": "func1",
            "data_type": "int",
            "line": 121,
            "column": 2,
            "children": []
        }
        symbol_table: SymbolTable = {
            "errors": ["Pre-existing error"]
        }

        with self._create_mock_patch():
            _handle_function_declaration(node1, symbol_table)
            _handle_function_declaration(node2, symbol_table)

        # Verify both errors exist
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0], "Pre-existing error")
        self.assertIn("func1", symbol_table["errors"][1])

    def test_empty_node_value_and_no_identifier(self):
        """Test function with empty value and no identifier child results in None func_name."""
        node: AST = {
            "type": "function_declaration",
            "value": None,
            "data_type": "int",
            "line": 130,
            "column": 1,
            "children": [
                {"type": "parameter", "value": "p", "data_type": "int"}
            ]
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            # Should not raise exception even with None func_name
            _handle_function_declaration(node, symbol_table)

        # None key should be in functions
        self.assertIn(None, symbol_table["functions"])

    def test_line_column_defaults(self):
        """Test default line and column values when not specified."""
        node: AST = {
            "type": "function_declaration",
            "value": "noLineCol",
            "data_type": "int",
            "children": []
        }
        symbol_table: SymbolTable = {}

        with self._create_mock_patch():
            _handle_function_declaration(node, symbol_table)

        func_info = symbol_table["functions"]["noLineCol"]
        self.assertEqual(func_info["line"], 0)
        self.assertEqual(func_info["column"], 0)


if __name__ == "__main__":
    unittest.main()
