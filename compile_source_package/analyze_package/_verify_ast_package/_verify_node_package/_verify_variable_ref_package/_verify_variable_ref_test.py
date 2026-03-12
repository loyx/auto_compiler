# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of UUT ===
from ._verify_variable_ref_src import _verify_variable_ref


class TestVerifyVariableRef(unittest.TestCase):
    """Test cases for _verify_variable_ref function."""

    def _create_node(self, name: str, line: int = 10, column: int = 5) -> Dict[str, Any]:
        """Helper to create a variable reference node."""
        return {
            "type": "variable_ref",
            "name": name,
            "line": line,
            "column": column
        }

    def _create_symbol_table(
        self,
        variables: Dict[str, Dict],
        current_scope: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a symbol table."""
        return {
            "variables": variables,
            "current_scope": current_scope
        }

    def test_happy_path_variable_exists_and_visible(self) -> None:
        """Test successful variable reference with visible declared variable."""
        node = self._create_node("x")
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "is_declared": True,
                    "scope_level": 1,
                    "data_type": "int"
                }
            },
            current_scope=1
        )
        filename = "test.py"

        _verify_variable_ref(node, symbol_table, filename)

        self.assertEqual(node["data_type"], "int")

    def test_happy_path_variable_from_outer_scope(self) -> None:
        """Test variable reference to variable from outer scope (lower scope_level)."""
        node = self._create_node("y")
        symbol_table = self._create_symbol_table(
            variables={
                "y": {
                    "is_declared": True,
                    "scope_level": 0,
                    "data_type": "str"
                }
            },
            current_scope=2
        )
        filename = "test.py"

        _verify_variable_ref(node, symbol_table, filename)

        self.assertEqual(node["data_type"], "str")

    def test_variable_not_in_symbol_table(self) -> None:
        """Test error when variable is not declared in symbol table."""
        node = self._create_node("undefined_var", line=15, column=8)
        symbol_table = self._create_symbol_table(
            variables={
                "x": {
                    "is_declared": True,
                    "scope_level": 1,
                    "data_type": "int"
                }
            },
            current_scope=1
        )
        filename = "missing.py"

        with self.assertRaises(ValueError) as context:
            _verify_variable_ref(node, symbol_table, filename)

        self.assertIn("missing.py:15:8", str(context.exception))
        self.assertIn("variable 'undefined_var' was not declared in this scope", str(context.exception))

    def test_variable_not_declared_flag_false(self) -> None:
        """Test error when variable exists but is_declared is False."""
        node = self._create_node("z", line=20, column=3)
        symbol_table = self._create_symbol_table(
            variables={
                "z": {
                    "is_declared": False,
                    "scope_level": 1,
                    "data_type": "float"
                }
            },
            current_scope=1
        )
        filename = "undeclared.py"

        with self.assertRaises(ValueError) as context:
            _verify_variable_ref(node, symbol_table, filename)

        self.assertIn("undeclared.py:20:3", str(context.exception))
        self.assertIn("variable 'z' was not declared in this scope", str(context.exception))

    def test_variable_scope_level_too_high(self) -> None:
        """Test error when variable scope_level > current_scope."""
        node = self._create_node("inner_var", line=25, column=10)
        symbol_table = self._create_symbol_table(
            variables={
                "inner_var": {
                    "is_declared": True,
                    "scope_level": 5,
                    "data_type": "bool"
                }
            },
            current_scope=3
        )
        filename = "scope.py"

        with self.assertRaises(ValueError) as context:
            _verify_variable_ref(node, symbol_table, filename)

        self.assertIn("scope.py:25:10", str(context.exception))
        self.assertIn("variable 'inner_var' was not declared in this scope", str(context.exception))

    def test_empty_variables_dict(self) -> None:
        """Test error when variables dict is empty."""
        node = self._create_node("any_var", line=1, column=1)
        symbol_table = self._create_symbol_table(
            variables={},
            current_scope=1
        )
        filename = "empty.py"

        with self.assertRaises(ValueError) as context:
            _verify_variable_ref(node, symbol_table, filename)

        self.assertIn("empty.py:1:1", str(context.exception))

    def test_boundary_scope_level_equal(self) -> None:
        """Test variable with scope_level exactly equal to current_scope."""
        node = self._create_node("boundary_var")
        symbol_table = self._create_symbol_table(
            variables={
                "boundary_var": {
                    "is_declared": True,
                    "scope_level": 3,
                    "data_type": "list"
                }
            },
            current_scope=3
        )
        filename = "boundary.py"

        _verify_variable_ref(node, symbol_table, filename)

        self.assertEqual(node["data_type"], "list")

    def test_missing_is_declared_key_defaults_to_false(self) -> None:
        """Test that missing is_declared key is treated as False."""
        node = self._create_node("missing_flag", line=30, column=7)
        symbol_table = self._create_symbol_table(
            variables={
                "missing_flag": {
                    "scope_level": 1,
                    "data_type": "dict"
                }
            },
            current_scope=1
        )
        filename = "missing_flag.py"

        with self.assertRaises(ValueError) as context:
            _verify_variable_ref(node, symbol_table, filename)

        self.assertIn("missing_flag.py:30:7", str(context.exception))

    def test_multiple_variables_only_target_checked(self) -> None:
        """Test that only the target variable is checked, not others."""
        node = self._create_node("target")
        symbol_table = self._create_symbol_table(
            variables={
                "other1": {
                    "is_declared": False,
                    "scope_level": 1,
                    "data_type": "int"
                },
                "target": {
                    "is_declared": True,
                    "scope_level": 1,
                    "data_type": "str"
                },
                "other2": {
                    "is_declared": True,
                    "scope_level": 10,
                    "data_type": "float"
                }
            },
            current_scope=1
        )
        filename = "multi.py"

        _verify_variable_ref(node, symbol_table, filename)

        self.assertEqual(node["data_type"], "str")


if __name__ == "__main__":
    unittest.main()
