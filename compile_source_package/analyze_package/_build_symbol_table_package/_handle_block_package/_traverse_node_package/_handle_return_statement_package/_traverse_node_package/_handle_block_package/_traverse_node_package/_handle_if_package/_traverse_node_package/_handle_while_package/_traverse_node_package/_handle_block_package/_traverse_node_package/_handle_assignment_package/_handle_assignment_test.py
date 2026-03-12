# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of target function ===
from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def _create_ast_node(
        self,
        value: str,
        data_type: str = None,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create AST node for testing."""
        node = {
            "type": "assignment",
            "value": value,
            "line": line,
            "column": column
        }
        if data_type is not None:
            node["data_type"] = data_type
        return node

    def _create_symbol_table(
        self,
        variables: Dict = None,
        errors: list = None
    ) -> Dict[str, Any]:
        """Helper to create symbol table for testing."""
        table = {
            "variables": variables if variables is not None else {},
            "current_scope": 0
        }
        if errors is not None:
            table["errors"] = errors
        return table

    def test_happy_path_declared_variable_no_type_check(self):
        """Test assignment to declared variable without type checking."""
        node = self._create_ast_node("x")
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        )

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_happy_path_declared_variable_type_match(self):
        """Test assignment to declared variable with matching type."""
        node = self._create_ast_node("x", data_type="int")
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        )

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_undeclared_variable_records_error(self):
        """Test that undeclared variable assignment records error."""
        node = self._create_ast_node("y", line=5, column=10)
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        )

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")
        self.assertEqual(errors[0]["line"], 5)
        self.assertEqual(errors[0]["column"], 10)
        self.assertIn("y", errors[0]["message"])

    def test_undeclared_variable_in_empty_variables(self):
        """Test assignment when variables dict is empty."""
        node = self._create_ast_node("z", line=3, column=5)
        symbol_table = self._create_symbol_table(variables={})

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")

    def test_variable_not_declared_flag(self):
        """Test variable exists but is_declared is False."""
        node = self._create_ast_node("w", line=7, column=2)
        symbol_table = self._create_symbol_table(
            variables={
                "w": {
                    "data_type": "char",
                    "is_declared": False,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        )

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")

    def test_type_mismatch_records_error(self):
        """Test that type mismatch records error."""
        node = self._create_ast_node("x", data_type="char", line=10, column=15)
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        )

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "type_mismatch")
        self.assertEqual(errors[0]["line"], 10)
        self.assertEqual(errors[0]["column"], 15)
        self.assertIn("x", errors[0]["message"])

    def test_type_mismatch_after_undeclared_check(self):
        """Test that type mismatch is not checked for undeclared variables."""
        node = self._create_ast_node("y", data_type="int", line=4, column=8)
        symbol_table = self._create_symbol_table(variables={})

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")

    def test_no_type_check_when_node_data_type_is_none(self):
        """Test that type check is skipped when node has no data_type."""
        node = self._create_ast_node("x", data_type=None)
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        )

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_no_type_check_when_declared_type_is_none(self):
        """Test that type check is skipped when declared type is None."""
        node = self._create_ast_node("x", data_type="int")
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "data_type": None,
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        )

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_initializes_errors_list_if_missing(self):
        """Test that errors list is created if not present in symbol_table."""
        node = self._create_ast_node("undef")
        symbol_table = self._create_symbol_table(variables={}, errors=None)
        if "errors" in symbol_table:
            del symbol_table["errors"]

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_appends_to_existing_errors_list(self):
        """Test that errors are appended to existing errors list."""
        node = self._create_ast_node("undef1", line=1, column=1)
        node2 = self._create_ast_node("undef2", line=2, column=2)
        symbol_table = self._create_symbol_table(
            variables={},
            errors=[{"type": "existing_error"}]
        )

        _handle_assignment(node, symbol_table)
        _handle_assignment(node2, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 3)
        self.assertEqual(errors[0]["type"], "existing_error")
        self.assertEqual(errors[1]["type"], "undeclared_variable")
        self.assertEqual(errors[2]["type"], "undeclared_variable")

    def test_multiple_variables_declared_only_one_undefined(self):
        """Test with multiple variables where only one is undefined."""
        node = self._create_ast_node("undefined_var", line=100, column=50)
        symbol_table = self._create_symbol_table(
            variables={
                "a": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
                "b": {"data_type": "char", "is_declared": True, "line": 2, "column": 2, "scope_level": 0},
            }
        )

        _handle_assignment(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "undeclared_variable")


if __name__ == "__main__":
    unittest.main()
