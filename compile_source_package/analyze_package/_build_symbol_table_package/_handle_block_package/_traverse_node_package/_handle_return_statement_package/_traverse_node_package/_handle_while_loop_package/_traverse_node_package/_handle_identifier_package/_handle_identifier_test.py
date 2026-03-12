import unittest
from typing import Any, Dict

from ._handle_identifier_src import _handle_identifier

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIdentifier(unittest.TestCase):
    """Test cases for _handle_identifier function."""

    def test_variable_declared_no_error(self):
        """When variable is already declared, no error should be added."""
        node: AST = {
            "type": "identifier",
            "name": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
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
        """When variable is not declared, an error should be recorded."""
        node: AST = {
            "type": "identifier",
            "name": "y",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
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
        self.assertEqual(error["error_type"], "undeclared_variable")
        self.assertEqual(error["var_name"], "y")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertIn("y", error["message"])

    def test_errors_none_initialized(self):
        """When errors is None, it should be initialized to empty list."""
        node: AST = {
            "type": "identifier",
            "name": "z",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": None
        }

        _handle_identifier(node, symbol_table)

        self.assertIsNotNone(symbol_table["errors"])
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_variables_missing_handled(self):
        """When variables key is missing, should handle gracefully."""
        node: AST = {
            "type": "identifier",
            "name": "w",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "errors": []
        }

        _handle_identifier(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["var_name"], "w")

    def test_error_structure_correct(self):
        """Verify the error structure has all required fields."""
        node: AST = {
            "type": "identifier",
            "name": "test_var",
            "line": 30,
            "column": 12
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_identifier(node, symbol_table)

        error = symbol_table["errors"][0]
        self.assertIn("error_type", error)
        self.assertIn("var_name", error)
        self.assertIn("line", error)
        self.assertIn("column", error)
        self.assertIn("message", error)
        self.assertEqual(error["error_type"], "undeclared_variable")
        self.assertEqual(error["var_name"], "test_var")
        self.assertEqual(error["line"], 30)
        self.assertEqual(error["column"], 12)

    def test_multiple_undeclared_variables(self):
        """Multiple undeclared variables should each add an error."""
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        node1: AST = {"type": "identifier", "name": "a", "line": 1, "column": 1}
        node2: AST = {"type": "identifier", "name": "b", "line": 2, "column": 2}

        _handle_identifier(node1, symbol_table)
        _handle_identifier(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["var_name"], "a")
        self.assertEqual(symbol_table["errors"][1]["var_name"], "b")

    def test_empty_symbol_table(self):
        """Empty symbol table should handle undeclared variable."""
        node: AST = {
            "type": "identifier",
            "name": "empty_test",
            "line": 5,
            "column": 5
        }
        symbol_table: SymbolTable = {}

        _handle_identifier(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["var_name"], "empty_test")


if __name__ == "__main__":
    unittest.main()
