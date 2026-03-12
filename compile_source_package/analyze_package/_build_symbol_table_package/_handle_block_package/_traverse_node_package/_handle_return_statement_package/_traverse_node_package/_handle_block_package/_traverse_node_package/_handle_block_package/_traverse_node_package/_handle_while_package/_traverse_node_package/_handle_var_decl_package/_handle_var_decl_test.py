# === imports ===
import unittest
from typing import Any, Dict

# === relative import for UUT ===
from ._handle_var_decl_src import _handle_var_decl


# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


# === test class ===
class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""

    def test_new_variable_declaration(self):
        """Happy path: declare a new variable, should be added to symbol_table."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_duplicate_variable_declaration(self):
        """Duplicate declaration: should record error, not add variable again."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 3,
                    "scope_level": 0
                }
            },
            "errors": [],
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        # Variable should remain unchanged (original declaration)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 3)
        # Error should be recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "duplicate_declaration")
        self.assertIn("x", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)

    def test_char_data_type(self):
        """Test variable declaration with char data type."""
        node: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "char",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")
        self.assertTrue(symbol_table["variables"]["c"]["is_declared"])

    def test_different_scope_level(self):
        """Test variable declaration at different scope level."""
        node: AST = {
            "type": "var_decl",
            "value": "y",
            "data_type": "int",
            "line": 20,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 2
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["y"]["scope_level"], 2)

    def test_empty_symbol_table_initialization(self):
        """Test with empty symbol_table - should initialize variables and errors."""
        node: AST = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_node_fields_defaults(self):
        """Test with missing node fields - should use defaults."""
        node: AST = {
            "type": "var_decl",
            "value": "a"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("a", symbol_table["variables"])
        self.assertIsNone(symbol_table["variables"]["a"]["data_type"])
        self.assertEqual(symbol_table["variables"]["a"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["a"]["column"], 0)

    def test_multiple_variables_same_scope(self):
        """Test declaring multiple variables in the same scope."""
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
            "current_scope": 1
        }

        node1: AST = {"type": "var_decl", "value": "var1", "data_type": "int", "line": 1, "column": 1}
        node2: AST = {"type": "var_decl", "value": "var2", "data_type": "char", "line": 2, "column": 2}
        node3: AST = {"type": "var_decl", "value": "var1", "data_type": "int", "line": 3, "column": 3}

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 2)
        self.assertIn("var1", symbol_table["variables"])
        self.assertIn("var2", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "duplicate_declaration")

    def test_no_exceptions_thrown(self):
        """Ensure function never throws exceptions even with edge cases."""
        node: AST = {}
        symbol_table: SymbolTable = {}

        try:
            _handle_var_decl(node, symbol_table)
        except Exception as e:
            self.fail(f"_handle_var_decl raised unexpected exception: {e}")


# === test runner ===
if __name__ == "__main__":
    unittest.main()
