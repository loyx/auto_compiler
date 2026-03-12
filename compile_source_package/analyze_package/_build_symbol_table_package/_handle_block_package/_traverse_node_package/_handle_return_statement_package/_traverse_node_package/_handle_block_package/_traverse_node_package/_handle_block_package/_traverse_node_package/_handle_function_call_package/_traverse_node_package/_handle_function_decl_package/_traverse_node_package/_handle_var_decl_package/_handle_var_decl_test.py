#!/usr/bin/env python3
"""
Unit tests for _handle_var_decl function.
Tests variable declaration handling in symbol table building.
"""

import unittest

# Relative import from the same package
from ._handle_var_decl_src import _handle_var_decl, AST, SymbolTable


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        self.base_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def test_happy_path_basic_var_decl(self) -> None:
        """Test basic variable declaration with all fields present."""
        node: AST = {
            "type": "var_decl",
            "name": "counter",
            "data_type": "int",
            "line": 15,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("counter", symbol_table["variables"])
        var_info = symbol_table["variables"]["counter"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["is_declared"], True)
        self.assertEqual(var_info["line"], 15)
        self.assertEqual(var_info["column"], 3)
        self.assertEqual(var_info["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_char_type(self) -> None:
        """Test variable declaration with char data type."""
        node: AST = {
            "type": "var_decl",
            "name": "ch",
            "data_type": "char",
            "line": 20,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["ch"]["data_type"], "char")

    def test_fallback_to_value_for_var_name(self) -> None:
        """Test that var_name falls back to 'value' field when 'name' is missing."""
        node: AST = {
            "type": "var_decl",
            "value": "temp_var",
            "data_type": "int",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("temp_var", symbol_table["variables"])

    def test_default_data_type_when_missing(self) -> None:
        """Test that data_type defaults to 'int' when not specified."""
        node: AST = {
            "type": "var_decl",
            "name": "default_type",
            "line": 30,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["default_type"]["data_type"], "int")

    def test_default_position_when_missing(self) -> None:
        """Test that line and column default to 0 when not specified."""
        node: AST = {
            "type": "var_decl",
            "name": "no_position"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["no_position"]
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_duplicate_declaration_same_scope(self) -> None:
        """Test that duplicate declaration in same scope records an error."""
        symbol_table: SymbolTable = {
            "variables": {
                "duplicate": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "name": "duplicate",
            "data_type": "int",
            "line": 10,
            "column": 5
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "duplicate_declaration")
        self.assertEqual(error["variable"], "duplicate")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        self.assertIn("already declared at line 5", error["message"])

    def test_same_name_different_scope_allowed(self) -> None:
        """Test that same variable name in different scope is allowed."""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "current_scope": 1,
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "char",
            "line": 15,
            "column": 8
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 15)

    def test_initializes_errors_if_missing(self) -> None:
        """Test that errors list is initialized if not present in symbol_table."""
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0
        }
        node: AST = {
            "type": "var_decl",
            "name": "test",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_initializes_variables_if_missing(self) -> None:
        """Test that variables dict is initialized if not present in symbol_table."""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "name": "new_var",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("new_var", symbol_table["variables"])

    def test_default_current_scope(self) -> None:
        """Test that current_scope defaults to 0 if not present."""
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "name": "scope_test",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["scope_test"]["scope_level"], 0)

    def test_multiple_variables_different_names(self) -> None:
        """Test declaring multiple variables with different names."""
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        node1: AST = {"type": "var_decl", "name": "a", "data_type": "int", "line": 1, "column": 1}
        node2: AST = {"type": "var_decl", "name": "b", "data_type": "char", "line": 2, "column": 2}
        node3: AST = {"type": "var_decl", "name": "c", "data_type": "int", "line": 3, "column": 3}

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_duplicate_then_new_var(self) -> None:
        """Test that after duplicate error, new variables can still be added."""
        symbol_table: SymbolTable = {
            "variables": {
                "existing": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }

        dup_node: AST = {"type": "var_decl", "name": "existing", "data_type": "int", "line": 5, "column": 5}
        new_node: AST = {"type": "var_decl", "name": "new_one", "data_type": "char", "line": 6, "column": 6}

        _handle_var_decl(dup_node, symbol_table)
        _handle_var_decl(new_node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("new_one", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["new_one"]["data_type"], "char")

    def test_empty_node_dict(self) -> None:
        """Test handling of empty node dictionary."""
        node: AST = {}
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_none_name_and_value(self) -> None:
        """Test when both name and value are None."""
        node: AST = {
            "type": "var_decl",
            "name": None,
            "value": None,
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 0)


class TestHandleVarDeclEdgeCases(unittest.TestCase):
    """Edge case tests for _handle_var_decl function."""

    def test_special_characters_in_var_name(self) -> None:
        """Test variable names with special characters."""
        node: AST = {
            "type": "var_decl",
            "name": "_private_var",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("_private_var", symbol_table["variables"])

    def test_numeric_var_name(self) -> None:
        """Test variable name that starts with number (edge case)."""
        node: AST = {
            "type": "var_decl",
            "name": "var123",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("var123", symbol_table["variables"])

    def test_high_scope_level(self) -> None:
        """Test variable declaration at high scope level."""
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 100,
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "name": "deep_var",
            "data_type": "int",
            "line": 50,
            "column": 10
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["deep_var"]["scope_level"], 100)

    def test_large_line_column_numbers(self) -> None:
        """Test with large line and column numbers."""
        node: AST = {
            "type": "var_decl",
            "name": "large_pos",
            "data_type": "int",
            "line": 99999,
            "column": 88888
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["large_pos"]["line"], 99999)
        self.assertEqual(symbol_table["variables"]["large_pos"]["column"], 88888)

    def test_duplicate_at_boundary_scope(self) -> None:
        """Test duplicate detection at scope boundary (scope 0 vs scope 1)."""
        symbol_table: SymbolTable = {
            "variables": {
                "boundary": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "current_scope": 1,
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "name": "boundary",
            "data_type": "char",
            "line": 10,
            "column": 5
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)
        self.assertEqual(symbol_table["variables"]["boundary"]["scope_level"], 1)


if __name__ == "__main__":
    unittest.main()
