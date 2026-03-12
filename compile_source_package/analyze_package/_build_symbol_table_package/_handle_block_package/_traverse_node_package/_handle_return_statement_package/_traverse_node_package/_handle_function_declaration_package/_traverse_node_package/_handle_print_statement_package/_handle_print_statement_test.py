"""Unit tests for _handle_print_statement function."""
import unittest

from ._handle_print_statement_src import _handle_print_statement


class TestHandlePrintStatement(unittest.TestCase):
    """Test cases for _handle_print_statement function."""

    def test_declared_variable_no_error(self):
        """Test that declared variables don't produce errors."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "x",
                    "line": 1,
                    "column": 5
                }
            ],
            "line": 1,
            "column": 1
        }

        symbol_table = {
            "variables": {"x": {"type": "int", "scope": 0}},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_undeclared_variable_adds_error(self):
        """Test that undeclared variables produce error messages."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "y",
                    "line": 3,
                    "column": 10
                }
            ],
            "line": 3,
            "column": 1
        }

        symbol_table = {
            "variables": {"x": {"type": "int", "scope": 0}},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Variable 'y' used in print without declaration", symbol_table["errors"][0])
        self.assertIn("line 3", symbol_table["errors"][0])
        self.assertIn("column 10", symbol_table["errors"][0])

    def test_creates_errors_list_if_missing(self):
        """Test that function creates errors list if not present in symbol_table."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "z",
                    "line": 5,
                    "column": 15
                }
            ],
            "line": 5,
            "column": 1
        }

        symbol_table = {
            "variables": {}
        }

        _handle_print_statement(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_creates_variables_dict_if_missing(self):
        """Test that function creates variables dict if not present in symbol_table."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "w",
                    "line": 7,
                    "column": 20
                }
            ],
            "line": 7,
            "column": 1
        }

        symbol_table = {
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIsInstance(symbol_table["variables"], dict)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_empty_children_no_error(self):
        """Test that print statement with no arguments doesn't produce errors."""
        node = {
            "type": "print_statement",
            "children": [],
            "line": 1,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_arguments_mixed_declaration(self):
        """Test multiple print arguments with mix of declared and undeclared variables."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "declared_var",
                    "line": 10,
                    "column": 5
                },
                {
                    "type": "variable_ref",
                    "name": "undeclared_var",
                    "line": 10,
                    "column": 20
                }
            ],
            "line": 10,
            "column": 1
        }

        symbol_table = {
            "variables": {"declared_var": {"type": "int", "scope": 0}},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("undeclared_var", symbol_table["errors"][0])

    def test_nested_expression_with_variable(self):
        """Test nested expression containing variable reference."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "binary_expression",
                    "children": [
                        {
                            "type": "variable_ref",
                            "name": "nested_var",
                            "line": 12,
                            "column": 8
                        },
                        {
                            "type": "literal",
                            "value": 5
                        }
                    ],
                    "line": 12,
                    "column": 5
                }
            ],
            "line": 12,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("nested_var", symbol_table["errors"][0])

    def test_literal_argument_no_error(self):
        """Test that literal values don't produce errors."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "literal",
                    "value": 42,
                    "line": 15,
                    "column": 5
                }
            ],
            "line": 15,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_error_format_correct(self):
        """Test that error message format is correct."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "test_var",
                    "line": 20,
                    "column": 25
                }
            ],
            "line": 20,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        expected_error = "Error: Variable 'test_var' used in print without declaration at line 20, column 25"
        self.assertEqual(symbol_table["errors"][0], expected_error)

    def test_node_without_line_column_uses_defaults(self):
        """Test that missing line/column in node uses defaults."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "missing_info"
                }
            ]
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 0", symbol_table["errors"][0])
        self.assertIn("column 0", symbol_table["errors"][0])

    def test_variable_with_value_instead_of_name(self):
        """Test variable reference that uses 'value' field instead of 'name'."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "value": "alt_var",
                    "line": 25,
                    "column": 30
                }
            ],
            "line": 25,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("alt_var", symbol_table["errors"][0])

    def test_deeply_nested_variables(self):
        """Test deeply nested expression with multiple variable references."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "binary_expression",
                    "children": [
                        {
                            "type": "binary_expression",
                            "children": [
                                {
                                    "type": "variable_ref",
                                    "name": "var1",
                                    "line": 30,
                                    "column": 5
                                },
                                {
                                    "type": "variable_ref",
                                    "name": "var2",
                                    "line": 30,
                                    "column": 10
                                }
                            ]
                        },
                        {
                            "type": "variable_ref",
                            "name": "var3",
                            "line": 30,
                            "column": 15
                        }
                    ]
                }
            ],
            "line": 30,
            "column": 1
        }

        symbol_table = {
            "variables": {"var2": {"type": "int", "scope": 0}},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        error_messages = " ".join(symbol_table["errors"])
        self.assertIn("var1", error_messages)
        self.assertIn("var3", error_messages)
        self.assertNotIn("var2", error_messages)

    def test_same_variable_multiple_times(self):
        """Test same undeclared variable referenced multiple times."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "duplicate",
                    "line": 35,
                    "column": 5
                },
                {
                    "type": "variable_ref",
                    "name": "duplicate",
                    "line": 35,
                    "column": 15
                }
            ],
            "line": 35,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_preserves_existing_errors(self):
        """Test that function preserves existing errors in symbol_table."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "new_error",
                    "line": 40,
                    "column": 5
                }
            ],
            "line": 40,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": ["Existing error message"]
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0], "Existing error message")
        self.assertIn("new_error", symbol_table["errors"][1])

    def test_no_children_key_uses_default(self):
        """Test that missing children key uses empty list default."""
        node = {
            "type": "print_statement",
            "line": 1,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_non_string_variable_name_ignored(self):
        """Test that non-string variable names are ignored."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": 123,
                    "line": 45,
                    "column": 5
                }
            ],
            "line": 45,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_empty_variable_name_ignored(self):
        """Test that empty variable names are ignored."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "",
                    "line": 50,
                    "column": 5
                }
            ],
            "line": 50,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_none_variable_name_ignored(self):
        """Test that None variable names are ignored."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": None,
                    "line": 55,
                    "column": 5
                }
            ],
            "line": 55,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_returns_none(self):
        """Test that function returns None."""
        node = {
            "type": "print_statement",
            "children": [],
            "line": 1,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        result = _handle_print_statement(node, symbol_table)

        self.assertIsNone(result)

    def test_no_side_effects_on_declared_variables(self):
        """Test that symbol_table variables dict is not modified for declared variables."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "variable_ref",
                    "name": "existing",
                    "line": 1,
                    "column": 1
                }
            ],
            "line": 1,
            "column": 1
        }

        symbol_table = {
            "variables": {"existing": {"type": "int", "scope": 0}},
            "errors": []
        }

        original_variables = symbol_table["variables"].copy()
        _handle_print_statement(node, symbol_table)

        self.assertEqual(symbol_table["variables"], original_variables)

    def test_complex_expression_tree(self):
        """Test complex expression tree with multiple levels and variable types."""
        node = {
            "type": "print_statement",
            "children": [
                {
                    "type": "function_call",
                    "name": "print_value",
                    "children": [
                        {
                            "type": "binary_expression",
                            "children": [
                                {
                                    "type": "variable_ref",
                                    "name": "a",
                                    "line": 60,
                                    "column": 10
                                },
                                {
                                    "type": "literal",
                                    "value": 10
                                }
                            ]
                        }
                    ]
                }
            ],
            "line": 60,
            "column": 1
        }

        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_print_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("a", symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()
