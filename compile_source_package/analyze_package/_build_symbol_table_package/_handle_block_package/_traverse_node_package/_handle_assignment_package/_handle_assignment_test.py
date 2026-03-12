"""
Unit tests for _handle_assignment function.
Tests variable assignment handling and undeclared variable error recording.
"""

import unittest
from typing import Any, Dict

from ._handle_assignment_src import (
    _handle_assignment,
    _extract_variable_name,
    _record_undeclared_error,
)


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_variable_declared_no_error(self):
        """When variable is declared, no error should be recorded."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "target": "x",
            "line": 10,
            "column": 5,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
        }

        _handle_assignment(node, symbol_table)

        self.assertNotIn("errors", symbol_table)

    def test_variable_not_declared_records_error(self):
        """When variable is not declared, error should be recorded."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "target": "y",
            "line": 15,
            "column": 8,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
        }

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["error_type"], "undeclared_variable")
        self.assertEqual(error["variable_name"], "y")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertIn("y", error["message"])

    def test_variable_not_declared_appends_to_existing_errors(self):
        """When errors list already exists, new error should be appended."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "target": "z",
            "line": 20,
            "column": 3,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "errors": [
                {"error_type": "other_error", "message": "Previous error", "line": 1, "column": 1}
            ],
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][1]["variable_name"], "z")

    def test_empty_variables_dict_records_error(self):
        """When variables dict is empty, error should be recorded."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "target": "var",
            "line": 5,
            "column": 2,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
        }

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_missing_variables_key_records_error(self):
        """When variables key is missing, error should still be recorded."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "target": "var",
            "line": 5,
            "column": 2,
        }
        symbol_table: Dict[str, Any] = {
            "functions": {},
        }

        _handle_assignment(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_missing_line_column_defaults_to_zero(self):
        """When line/column missing, they should default to 0."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "target": "var",
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
        }

        _handle_assignment(node, symbol_table)

        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)

    def test_no_variable_name_silent_return(self):
        """When cannot extract variable name, function returns silently."""
        node: Dict[str, Any] = {
            "type": "assignment",
            "line": 10,
            "column": 5,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
        }

        _handle_assignment(node, symbol_table)

        self.assertNotIn("errors", symbol_table)


class TestExtractVariableName(unittest.TestCase):
    """Test cases for _extract_variable_name helper function."""

    def test_extract_from_target_string(self):
        """Extract variable name from target field as string."""
        node: Dict[str, Any] = {"target": "myvar"}
        result = _extract_variable_name(node)
        self.assertEqual(result, "myvar")

    def test_extract_from_target_dict(self):
        """Extract variable name from target field as dict."""
        node: Dict[str, Any] = {"target": {"name": "myvar"}}
        result = _extract_variable_name(node)
        self.assertEqual(result, "myvar")

    def test_extract_from_target_dict_value(self):
        """Extract variable name from target dict value field."""
        node: Dict[str, Any] = {"target": {"value": "myvar"}}
        result = _extract_variable_name(node)
        self.assertEqual(result, "myvar")

    def test_extract_from_name_field(self):
        """Extract variable name from name field."""
        node: Dict[str, Any] = {"name": "myvar"}
        result = _extract_variable_name(node)
        self.assertEqual(result, "myvar")

    def test_extract_from_value_string(self):
        """Extract variable name from value field as string."""
        node: Dict[str, Any] = {"value": "myvar"}
        result = _extract_variable_name(node)
        self.assertEqual(result, "myvar")

    def test_extract_from_value_dict(self):
        """Extract variable name from value field as dict."""
        node: Dict[str, Any] = {"value": {"name": "myvar"}}
        result = _extract_variable_name(node)
        self.assertEqual(result, "myvar")

    def test_extract_from_value_dict_value(self):
        """Extract variable name from value dict value field."""
        node: Dict[str, Any] = {"value": {"value": "myvar"}}
        result = _extract_variable_name(node)
        self.assertEqual(result, "myvar")

    def test_target_takes_precedence(self):
        """Target field takes precedence over name and value."""
        node: Dict[str, Any] = {
            "target": "target_var",
            "name": "name_var",
            "value": "value_var",
        }
        result = _extract_variable_name(node)
        self.assertEqual(result, "target_var")

    def test_name_takes_precedence_over_value(self):
        """Name field takes precedence over value when target absent."""
        node: Dict[str, Any] = {
            "name": "name_var",
            "value": "value_var",
        }
        result = _extract_variable_name(node)
        self.assertEqual(result, "name_var")

    def test_returns_none_for_empty_node(self):
        """Return None when node has no relevant fields."""
        node: Dict[str, Any] = {"type": "assignment"}
        result = _extract_variable_name(node)
        self.assertIsNone(result)

    def test_returns_none_for_non_string_target(self):
        """Return None when target is not string or dict."""
        node: Dict[str, Any] = {"target": 123}
        result = _extract_variable_name(node)
        self.assertIsNone(result)

    def test_returns_none_for_nested_dict_no_name(self):
        """Return None when nested dict has no name or value."""
        node: Dict[str, Any] = {"target": {"other": "data"}}
        result = _extract_variable_name(node)
        self.assertIsNone(result)


class TestRecordUndeclaredError(unittest.TestCase):
    """Test cases for _record_undeclared_error helper function."""

    def test_creates_errors_list_when_missing(self):
        """Create errors list in symbol_table when it doesn't exist."""
        symbol_table: Dict[str, Any] = {"variables": {}}

        _record_undeclared_error(symbol_table, "test_var", 10, 5)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_appends_to_existing_errors_list(self):
        """Append error to existing errors list."""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "errors": [{"error_type": "existing"}],
        }

        _record_undeclared_error(symbol_table, "test_var", 10, 5)

        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_error_info_structure(self):
        """Error info should have correct structure."""
        symbol_table: Dict[str, Any] = {"variables": {}}

        _record_undeclared_error(symbol_table, "myvar", 15, 8)

        error = symbol_table["errors"][0]
        self.assertEqual(error["error_type"], "undeclared_variable")
        self.assertEqual(error["variable_name"], "myvar")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertIn("myvar", error["message"])
        self.assertIn("before declaration", error["message"])

    def test_multiple_errors_recorded(self):
        """Multiple calls should record multiple errors."""
        symbol_table: Dict[str, Any] = {"variables": {}}

        _record_undeclared_error(symbol_table, "var1", 10, 1)
        _record_undeclared_error(symbol_table, "var2", 20, 2)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["variable_name"], "var1")
        self.assertEqual(symbol_table["errors"][1]["variable_name"], "var2")


if __name__ == "__main__":
    unittest.main()
