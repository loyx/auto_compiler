#!/usr/bin/env python3
"""
Unit tests for _handle_identifier function.
Tests variable lookup in symbol table, error handling for undefined variables.
"""

import unittest
from typing import Dict, Any

# Relative import from the same package
from ._handle_identifier_src import _handle_identifier


class TestHandleIdentifier(unittest.TestCase):
    """Test cases for _handle_identifier function."""

    def test_variable_exists_returns_data_type(self):
        """Happy path: variable exists in symbol_table, returns correct data_type."""
        node = {
            "type": "identifier",
            "name": "myVar",
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {
                "myVar": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        result = _handle_identifier(node, symbol_table)

        self.assertEqual(result, "int")
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_variable_not_defined_returns_void_and_adds_error(self):
        """Edge case: variable not defined, returns 'void' and adds error."""
        node = {
            "type": "identifier",
            "name": "undefinedVar",
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "variables": {
                "existingVar": {
                    "data_type": "string",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        result = _handle_identifier(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("undefined variable 'undefinedVar'", symbol_table["errors"][0])
        self.assertIn("line 15", symbol_table["errors"][0])

    def test_variable_exists_with_different_data_types(self):
        """Test various data types returned correctly."""
        test_cases = [
            ("intVar", "int"),
            ("floatVar", "float"),
            ("stringVar", "string"),
            ("boolVar", "bool"),
            ("arrayVar", "array"),
            ("voidVar", "void"),
        ]

        for var_name, expected_type in test_cases:
            with self.subTest(var_name=var_name, expected_type=expected_type):
                node = {
                    "type": "identifier",
                    "name": var_name,
                    "line": 1,
                    "column": 1
                }
                symbol_table = {
                    "variables": {
                        var_name: {
                            "data_type": expected_type,
                            "is_declared": True,
                            "line": 1,
                            "column": 1,
                            "scope_level": 0
                        }
                    },
                    "errors": []
                }

                result = _handle_identifier(node, symbol_table)
                self.assertEqual(result, expected_type)

    def test_missing_variables_key_in_symbol_table(self):
        """Edge case: symbol_table missing 'variables' key."""
        node = {
            "type": "identifier",
            "name": "anyVar",
            "line": 5,
            "column": 3
        }
        symbol_table = {
            "errors": []
        }

        result = _handle_identifier(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_missing_line_in_node(self):
        """Edge case: node missing 'line' field, defaults to 0."""
        node = {
            "type": "identifier",
            "name": "noLineVar",
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        result = _handle_identifier(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 0", symbol_table["errors"][0])

    def test_missing_errors_key_creates_it(self):
        """Edge case: symbol_table missing 'errors' key, function creates it."""
        node = {
            "type": "identifier",
            "name": "missingErrorsVar",
            "line": 20,
            "column": 10
        }
        symbol_table = {
            "variables": {}
        }

        result = _handle_identifier(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_empty_symbol_table(self):
        """Edge case: completely empty symbol_table."""
        node = {
            "type": "identifier",
            "name": "emptyTableVar",
            "line": 1,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {}

        result = _handle_identifier(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_variable_with_missing_data_type(self):
        """Edge case: variable exists but missing 'data_type' field."""
        node = {
            "type": "identifier",
            "name": "noDataTypeVar",
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "variables": {
                "noDataTypeVar": {
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        result = _handle_identifier(node, symbol_table)

        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_undefined_variables_add_multiple_errors(self):
        """Test: multiple calls with undefined variables add multiple errors."""
        symbol_table = {
            "variables": {},
            "errors": []
        }

        for i in range(3):
            node = {
                "type": "identifier",
                "name": f"undefinedVar{i}",
                "line": 10 + i,
                "column": 5
            }
            result = _handle_identifier(node, symbol_table)
            self.assertEqual(result, "void")

        self.assertEqual(len(symbol_table["errors"]), 3)

    def test_mixed_defined_and_undefined_variables(self):
        """Test: mix of defined and undefined variables in sequence."""
        symbol_table = {
            "variables": {
                "definedVar": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        # First call: defined variable
        node1 = {"type": "identifier", "name": "definedVar", "line": 5, "column": 1}
        result1 = _handle_identifier(node1, symbol_table)
        self.assertEqual(result1, "int")

        # Second call: undefined variable
        node2 = {"type": "identifier", "name": "undefinedVar", "line": 6, "column": 1}
        result2 = _handle_identifier(node2, symbol_table)
        self.assertEqual(result2, "void")

        # Third call: defined variable again
        node3 = {"type": "identifier", "name": "definedVar", "line": 7, "column": 1}
        result3 = _handle_identifier(node3, symbol_table)
        self.assertEqual(result3, "int")

        self.assertEqual(len(symbol_table["errors"]), 1)


if __name__ == "__main__":
    unittest.main()
