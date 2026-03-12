# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._handle_return_statement_src import _handle_return_statement

# === ADT defines ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturnStatement(unittest.TestCase):
    """Test cases for _handle_return_statement function."""

    def test_return_statement_with_value_calls_traverse_node(self):
        """Happy path: return statement with value should call _traverse_node."""
        node: AST = {
            "type": "return_statement",
            "value": {"type": "literal", "value": 42},
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            mock_traverse.assert_called_once()
            call_args = mock_traverse.call_args
            self.assertEqual(call_args[0][0], node["value"])
            self.assertIs(call_args[0][1], symbol_table)

    def test_return_statement_without_value_does_not_call_traverse_node(self):
        """Edge case: return statement without value should not call _traverse_node."""
        node: AST = {
            "type": "return_statement",
            "value": None,
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            mock_traverse.assert_not_called()

    def test_return_statement_missing_value_key_does_not_call_traverse_node(self):
        """Edge case: return statement without 'value' key should not call _traverse_node."""
        node: AST = {
            "type": "return_statement",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            mock_traverse.assert_not_called()

    def test_return_statement_with_complex_expression(self):
        """Test return statement with complex expression tree."""
        complex_value: AST = {
            "type": "binary_expression",
            "operator": "+",
            "left": {"type": "identifier", "name": "x"},
            "right": {"type": "literal", "value": 10}
        }
        node: AST = {
            "type": "return_statement",
            "value": complex_value,
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int", "scope": 1}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            mock_traverse.assert_called_once_with(complex_value, symbol_table)

    def test_return_statement_preserves_symbol_table_reference(self):
        """Verify that the same symbol_table reference is passed to _traverse_node."""
        node: AST = {
            "type": "return_statement",
            "value": {"type": "literal", "value": "hello"},
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            # Verify the exact same object reference is passed
            self.assertIs(mock_traverse.call_args[0][1], symbol_table)

    def test_return_statement_with_empty_dict_value(self):
        """Edge case: return statement with empty dict as value."""
        node: AST = {
            "type": "return_statement",
            "value": {},
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            # Empty dict is not None, so _traverse_node should be called
            mock_traverse.assert_called_once()

    def test_return_statement_with_zero_value(self):
        """Edge case: return statement with 0 as value (falsy but not None)."""
        node: AST = {
            "type": "return_statement",
            "value": 0,
            "line": 30,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            # 0 is not None, so _traverse_node should be called
            mock_traverse.assert_called_once_with(0, symbol_table)

    def test_return_statement_with_false_value(self):
        """Edge case: return statement with False as value (falsy but not None)."""
        node: AST = {
            "type": "return_statement",
            "value": False,
            "line": 35,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            # False is not None, so _traverse_node should be called
            mock_traverse.assert_called_once_with(False, symbol_table)

    def test_return_statement_with_empty_string_value(self):
        """Edge case: return statement with empty string as value."""
        node: AST = {
            "type": "return_statement",
            "value": "",
            "line": 40,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1]
        }

        with patch("._handle_return_statement_package._handle_return_statement_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)

            # Empty string is not None, so _traverse_node should be called
            mock_traverse.assert_called_once_with("", symbol_table)


if __name__ == "__main__":
    unittest.main()
