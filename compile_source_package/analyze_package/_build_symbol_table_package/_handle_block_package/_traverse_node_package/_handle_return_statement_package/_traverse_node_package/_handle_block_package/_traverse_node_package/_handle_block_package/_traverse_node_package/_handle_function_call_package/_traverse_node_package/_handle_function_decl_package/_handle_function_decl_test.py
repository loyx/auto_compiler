# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === sub function imports ===
from ._handle_function_decl_src import _handle_function_decl

# === Type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFunctionDecl(unittest.TestCase):
    """Test cases for _handle_function_decl function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_simple_function_decl_no_params(self) -> None:
        """Test handling a simple function declaration without parameters."""
        node: AST = {
            "type": "function_decl",
            "value": "my_function",
            "data_type": "void",
            "line": 10,
            "column": 5,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        # Verify function info recorded
        self.assertIn("my_function", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["my_function"]
        self.assertEqual(func_info["return_type"], "void")
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)

        # Verify current_function restored to None
        self.assertIsNone(self.symbol_table["current_function"])

    def test_function_decl_with_params(self) -> None:
        """Test handling a function declaration with parameters."""
        node: AST = {
            "type": "function_decl",
            "value": "add",
            "data_type": "int",
            "line": 20,
            "column": 3,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "a",
                            "data_type": "int",
                            "line": 21,
                            "column": 10
                        },
                        {
                            "type": "param",
                            "value": "b",
                            "data_type": "int",
                            "line": 21,
                            "column": 15
                        }
                    ]
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        # Verify function info recorded
        self.assertIn("add", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["add"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "a")
        self.assertEqual(func_info["params"][0]["data_type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "b")
        self.assertEqual(func_info["params"][1]["data_type"], "int")

    def test_function_decl_with_block_body(self) -> None:
        """Test handling a function declaration with a block body."""
        block_node: AST = {
            "type": "block",
            "children": []
        }
        node: AST = {
            "type": "function_decl",
            "value": "main",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [block_node]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_decl(node, self.symbol_table)

            # Verify _traverse_node was called with the block
            mock_traverse.assert_called_once_with(block_node, self.symbol_table)

        # Verify current_function was set during traversal
        self.assertIsNone(self.symbol_table["current_function"])

    def test_function_decl_current_function_context(self) -> None:
        """Test that current_function context is properly managed."""
        node: AST = {
            "type": "function_decl",
            "value": "test_func",
            "data_type": "void",
            "line": 5,
            "column": 2,
            "children": []
        }

        # Set initial current_function
        self.symbol_table["current_function"] = "outer_func"

        _handle_function_decl(node, self.symbol_table)

        # Verify current_function is restored
        self.assertEqual(self.symbol_table["current_function"], "outer_func")

    def test_function_decl_default_return_type(self) -> None:
        """Test that default return type is 'void' when not specified."""
        node: AST = {
            "type": "function_decl",
            "value": "no_return_type",
            "line": 15,
            "column": 8,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["no_return_type"]
        self.assertEqual(func_info["return_type"], "void")

    def test_function_decl_default_param_type(self) -> None:
        """Test that default parameter type is 'int' when not specified."""
        node: AST = {
            "type": "function_decl",
            "value": "func_with_param",
            "data_type": "void",
            "line": 25,
            "column": 4,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "x",
                            "line": 26,
                            "column": 12
                        }
                    ]
                }
            ]
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["func_with_param"]
        self.assertEqual(func_info["params"][0]["data_type"], "int")

    def test_function_decl_multiple_children_no_block(self) -> None:
        """Test handling function with multiple children but no block."""
        node: AST = {
            "type": "function_decl",
            "value": "multi_child",
            "data_type": "char",
            "line": 30,
            "column": 6,
            "children": [
                {
                    "type": "param_list",
                    "children": []
                },
                {
                    "type": "other_node",
                    "value": "something"
                }
            ]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_decl(node, self.symbol_table)

            # _traverse_node should not be called since there's no block
            mock_traverse.assert_not_called()

        # Function info should still be recorded
        self.assertIn("multi_child", self.symbol_table["functions"])

    def test_function_decl_empty_children_list(self) -> None:
        """Test handling function with empty children list."""
        node: AST = {
            "type": "function_decl",
            "value": "empty_children",
            "data_type": "void",
            "line": 35,
            "column": 7,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["empty_children"]
        self.assertEqual(func_info["params"], [])

    def test_function_decl_missing_children_key(self) -> None:
        """Test handling function node without children key."""
        node: AST = {
            "type": "function_decl",
            "value": "no_children_key",
            "data_type": "void",
            "line": 40,
            "column": 9
        }

        _handle_function_decl(node, self.symbol_table)

        # Should not raise, function info should be recorded
        self.assertIn("no_children_key", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["no_children_key"]
        self.assertEqual(func_info["params"], [])

    def test_function_decl_first_child_not_param_list(self) -> None:
        """Test handling function where first child is not param_list."""
        node: AST = {
            "type": "function_decl",
            "value": "wrong_first_child",
            "data_type": "void",
            "line": 45,
            "column": 10,
            "children": [
                {
                    "type": "block",
                    "children": []
                }
            ]
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_function_decl(node, self.symbol_table)

            # Should still traverse the block
            mock_traverse.assert_called_once()

        # Params should be empty since first child wasn't param_list
        func_info = self.symbol_table["functions"]["wrong_first_child"]
        self.assertEqual(func_info["params"], [])

    def test_function_decl_preserves_existing_functions(self) -> None:
        """Test that existing functions in symbol_table are preserved."""
        # Pre-populate symbol_table with an existing function
        self.symbol_table["functions"]["existing_func"] = {
            "return_type": "int",
            "params": [],
            "line": 1,
            "column": 1
        }

        node: AST = {
            "type": "function_decl",
            "value": "new_func",
            "data_type": "void",
            "line": 50,
            "column": 11,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        # Both functions should exist
        self.assertIn("existing_func", self.symbol_table["functions"])
        self.assertIn("new_func", self.symbol_table["functions"])

    def test_function_decl_char_return_type(self) -> None:
        """Test handling function with char return type."""
        node: AST = {
            "type": "function_decl",
            "value": "get_char",
            "data_type": "char",
            "line": 55,
            "column": 12,
            "children": []
        }

        _handle_function_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["get_char"]
        self.assertEqual(func_info["return_type"], "char")


if __name__ == "__main__":
    unittest.main()
