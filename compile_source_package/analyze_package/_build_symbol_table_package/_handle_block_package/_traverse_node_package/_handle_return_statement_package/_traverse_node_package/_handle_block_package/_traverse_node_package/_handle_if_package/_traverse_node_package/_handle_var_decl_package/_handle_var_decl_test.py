import unittest
from unittest.mock import patch

from ._handle_var_decl_src import _handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""

    def test_normal_variable_declaration(self):
        """Test normal variable declaration without initialization."""
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 10,
            "column": 5,
            "data_type": "int"
        }
        symbol_table = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    def test_duplicate_declaration_same_scope(self):
        """Test duplicate variable declaration in same scope records error."""
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 20,
            "column": 5,
            "data_type": "int"
        }
        symbol_table = {
            "current_scope": 0,
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Variable 'x' already declared at line 10", symbol_table["errors"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)

    def test_declaration_different_scope_allowed(self):
        """Test variable declaration in different scope is allowed."""
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 20,
            "column": 5,
            "data_type": "int"
        }
        symbol_table = {
            "current_scope": 1,
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 20)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)

    @patch("_handle_var_decl_package._handle_var_decl_src._traverse_node")
    def test_variable_with_initialization_expression(self, mock_traverse):
        """Test variable declaration with initialization expression."""
        init_expr = {"type": "literal", "value": 42}
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 10,
            "column": 5,
            "data_type": "int",
            "children": [init_expr]
        }
        symbol_table = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        mock_traverse.assert_called_once_with(init_expr, symbol_table)

    @patch("_handle_var_decl_package._traverse_node_src._traverse_node")
    def test_variable_without_initialization(self, mock_traverse):
        """Test variable declaration without initialization expression."""
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 10,
            "column": 5,
            "data_type": "int"
        }
        symbol_table = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        mock_traverse.assert_not_called()

    def test_minimal_node_fields(self):
        """Test variable declaration with minimal node fields."""
        node = {
            "type": "var_decl",
            "value": "x"
        }
        symbol_table = {
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 0)
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")

    def test_default_data_type(self):
        """Test default data_type is 'int' when not specified."""
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")

    def test_errors_list_initialized_if_missing(self):
        """Test errors list is initialized if not present in symbol_table."""
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 10,
            "column": 5,
            "data_type": "int"
        }
        symbol_table = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_char_data_type(self):
        """Test variable declaration with char data type."""
        node = {
            "type": "var_decl",
            "value": "c",
            "line": 15,
            "column": 10,
            "data_type": "char"
        }
        symbol_table = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")

    def test_default_current_scope(self):
        """Test default current_scope is 0 when not specified."""
        node = {
            "type": "var_decl",
            "value": "x",
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)


if __name__ == "__main__":
    unittest.main()
