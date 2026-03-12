# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import for UUT ===
from ._handle_assignment_src import _handle_assignment

# === type aliases (matching UUT) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_valid_assignment_matching_types(self):
        """Happy path: valid assignment with matching types should not produce errors."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 10, "column": 5},
                {"type": "expression", "value": 42, "data_type": "int", "line": 10, "column": 9}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 5, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_undeclared_variable(self):
        """Assignment to undeclared variable should record an error."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "y", "line": 15, "column": 3},
                {"type": "expression", "value": 100, "data_type": "int", "line": 15, "column": 7}
            ],
            "line": 15,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "undeclared_variable")
        self.assertIn("y", error["message"])
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 3)
        self.assertEqual(error["variable"], "y")

    def test_type_mismatch(self):
        """Type mismatch should record an error."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "ch", "line": 20, "column": 2},
                {"type": "expression", "value": 42, "data_type": "int", "line": 20, "column": 6}
            ],
            "line": 20,
            "column": 2
        }
        symbol_table: SymbolTable = {
            "variables": {
                "ch": {"data_type": "char", "is_declared": True, "line": 8, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_mismatch")
        self.assertIn("int", error["message"])
        self.assertIn("char", error["message"])
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 2)
        self.assertEqual(error["variable"], "ch")
        self.assertEqual(error["expected_type"], "char")
        self.assertEqual(error["actual_type"], "int")

    def test_variable_exists_but_not_declared(self):
        """Variable in symbol table but is_declared=False should record undeclared error."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z", "line": 25, "column": 4},
                {"type": "expression", "value": "a", "data_type": "char", "line": 25, "column": 8}
            ],
            "line": 25,
            "column": 4
        }
        symbol_table: SymbolTable = {
            "variables": {
                "z": {"data_type": "char", "is_declared": False, "line": 12, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "undeclared_variable")

    def test_missing_errors_list_in_symbol_table(self):
        """Symbol table without errors list should have it created."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "a", "line": 30, "column": 1},
                {"type": "expression", "value": 1, "data_type": "int", "line": 30, "column": 5}
            ],
            "line": 30,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_insufficient_children(self):
        """Assignment node with less than 2 children should return without error."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 35, "column": 1}
            ],
            "line": 35,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_variable_name(self):
        """Assignment with missing variable name should return without error."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": None, "line": 40, "column": 1},
                {"type": "expression", "value": 5, "data_type": "int", "line": 40, "column": 5}
            ],
            "line": 40,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_no_children_key(self):
        """Assignment node without children key should return without error."""
        node: AST = {
            "type": "assignment",
            "line": 45,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_type_match_char_to_char(self):
        """Char to char assignment should not produce errors."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "c", "line": 50, "column": 1},
                {"type": "expression", "value": "a", "data_type": "char", "line": 50, "column": 5}
            ],
            "line": 50,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 20, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_right_value_without_data_type(self):
        """Right value without data_type should not produce type mismatch error."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 55, "column": 1},
                {"type": "expression", "value": 10, "line": 55, "column": 5}
            ],
            "line": 55,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 25, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_errors_accumulated(self):
        """Multiple assignment errors should accumulate in errors list."""
        node1: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "undef1", "line": 60, "column": 1},
                {"type": "expression", "value": 1, "data_type": "int", "line": 60, "column": 10}
            ],
            "line": 60,
            "column": 1
        }
        node2: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "undef2", "line": 61, "column": 1},
                {"type": "expression", "value": 2, "data_type": "int", "line": 61, "column": 10}
            ],
            "line": 61,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["variable"], "undef1")
        self.assertEqual(symbol_table["errors"][1]["variable"], "undef2")


if __name__ == "__main__":
    unittest.main()
