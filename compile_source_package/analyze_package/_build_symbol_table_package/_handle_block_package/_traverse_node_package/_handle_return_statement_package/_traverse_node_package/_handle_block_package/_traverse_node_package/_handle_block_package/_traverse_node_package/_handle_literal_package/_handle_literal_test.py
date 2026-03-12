# -*- coding: utf-8 -*-
"""
Unit tests for _handle_literal function.
Tests literal node validation for type compatibility (int/char).
"""

import unittest
from typing import Any, Dict

# Relative import from the same package
from ._handle_literal_src import _handle_literal

# Type aliases for convenience
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleLiteralValidCases(unittest.TestCase):
    """Test cases for valid literal nodes (happy path)."""

    def test_valid_int_literal(self):
        """Test valid integer literal does not produce errors."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": 42,
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_int_literal_zero(self):
        """Test valid integer literal with value 0."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": 0,
            "line": 1,
            "column": 1
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_int_literal_negative(self):
        """Test valid negative integer literal."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": -100,
            "line": 5,
            "column": 10
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_char_literal_single_character(self):
        """Test valid char literal with single character."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": "a",
            "line": 15,
            "column": 20
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_char_literal_special_character(self):
        """Test valid char literal with special character."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": "\n",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_char_literal_digit_as_char(self):
        """Test valid char literal with digit character."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": "5",
            "line": 8,
            "column": 12
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)


class TestHandleLiteralIntTypeMismatches(unittest.TestCase):
    """Test cases for int type mismatches."""

    def test_int_type_with_string_value(self):
        """Test int data_type with string value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "hello",
            "line": 25,
            "column": 7
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Type mismatch", error["message"])
        self.assertIn("int", error["message"])
        self.assertEqual(error["line"], 25)
        self.assertEqual(error["column"], 7)

    def test_int_type_with_float_value(self):
        """Test int data_type with float value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": 3.14,
            "line": 30,
            "column": 15
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("float", error["message"])

    def test_int_type_with_char_value(self):
        """Test int data_type with single char string value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "x",
            "line": 35,
            "column": 22
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Type mismatch", error["message"])

    def test_int_type_with_list_value(self):
        """Test int data_type with list value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": [1, 2, 3],
            "line": 40,
            "column": 8
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("list", error["message"])

    def test_int_type_with_none_value(self):
        """Test int data_type with None value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": None,
            "line": 45,
            "column": 11
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("NoneType", error["message"])


class TestHandleLiteralCharTypeMismatches(unittest.TestCase):
    """Test cases for char type mismatches."""

    def test_char_type_with_empty_string(self):
        """Test char data_type with empty string produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": "",
            "line": 50,
            "column": 14
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Type mismatch", error["message"])
        self.assertIn("length=0", error["message"])

    def test_char_type_with_multi_char_string(self):
        """Test char data_type with multi-character string produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": "abc",
            "line": 55,
            "column": 19
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Type mismatch", error["message"])
        self.assertIn("length=3", error["message"])

    def test_char_type_with_integer_value(self):
        """Test char data_type with integer value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": 65,
            "line": 60,
            "column": 25
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Type mismatch", error["message"])
        self.assertIn("int", error["message"])

    def test_char_type_with_float_value(self):
        """Test char data_type with float value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": 2.5,
            "line": 65,
            "column": 30
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("float", error["message"])

    def test_char_type_with_list_value(self):
        """Test char data_type with list value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": ["a"],
            "line": 70,
            "column": 5
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("list", error["message"])

    def test_char_type_with_none_value(self):
        """Test char data_type with None value produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": None,
            "line": 75,
            "column": 9
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("NoneType", error["message"])


class TestHandleLiteralEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_unknown_data_type_no_error(self):
        """Test unknown data_type does not produce errors."""
        node: AST = {
            "type": "literal",
            "data_type": "float",
            "value": 3.14,
            "line": 80,
            "column": 12
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_empty_data_type_no_error(self):
        """Test empty data_type does not produce errors."""
        node: AST = {
            "type": "literal",
            "data_type": "",
            "value": "test",
            "line": 85,
            "column": 16
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_data_type_uses_default(self):
        """Test missing data_type uses default empty string."""
        node: AST = {
            "type": "literal",
            "value": "test",
            "line": 90,
            "column": 20
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_value_field(self):
        """Test missing value field with int data_type produces error."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "line": 95,
            "column": 24
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("NoneType", error["message"])

    def test_missing_line_column_uses_defaults(self):
        """Test missing line/column uses default values."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "invalid"
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], -1)
        self.assertEqual(error["column"], -1)

    def test_creates_errors_list_if_missing(self):
        """Test function creates errors list if not present in symbol_table."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "invalid",
            "line": 100,
            "column": 30
        }
        symbol_table: SymbolTable = {}
        
        _handle_literal(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_appends_to_existing_errors(self):
        """Test function appends to existing errors list."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "invalid",
            "line": 105,
            "column": 35
        }
        symbol_table: SymbolTable = {
            "errors": [
                {"type": "error", "message": "Previous error", "line": 1, "column": 1}
            ]
        }
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "Previous error")

    def test_multiple_errors_accumulate(self):
        """Test multiple invalid literals accumulate errors."""
        symbol_table: SymbolTable = {"errors": []}
        
        node1: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "first",
            "line": 110,
            "column": 1
        }
        node2: AST = {
            "type": "literal",
            "data_type": "char",
            "value": "second",
            "line": 111,
            "column": 2
        }
        
        _handle_literal(node1, symbol_table)
        _handle_literal(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["line"], 110)
        self.assertEqual(symbol_table["errors"][1]["line"], 111)

    def test_does_not_throw_exception_on_malformed_node(self):
        """Test function does not throw exception on malformed node."""
        node: AST = {}
        symbol_table: SymbolTable = {}
        
        try:
            _handle_literal(node, symbol_table)
        except Exception as e:
            self.fail(f"_handle_literal raised unexpected exception: {e}")
        
        self.assertIn("errors", symbol_table)


class TestHandleLiteralErrorFormat(unittest.TestCase):
    """Test error message format and structure."""

    def test_error_has_required_fields(self):
        """Test error object has all required fields."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "test",
            "line": 120,
            "column": 40
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        error = symbol_table["errors"][0]
        self.assertIn("type", error)
        self.assertIn("message", error)
        self.assertIn("line", error)
        self.assertIn("column", error)

    def test_error_type_is_error(self):
        """Test error type field is 'error'."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": "ab",
            "line": 125,
            "column": 45
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")

    def test_error_message_mentions_expected_type(self):
        """Test error message mentions expected type."""
        node: AST = {
            "type": "literal",
            "data_type": "int",
            "value": "test",
            "line": 130,
            "column": 50
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        error = symbol_table["errors"][0]
        self.assertIn("int", error["message"])
        self.assertIn("expected", error["message"].lower())

    def test_error_message_mentions_actual_type(self):
        """Test error message mentions actual type."""
        node: AST = {
            "type": "literal",
            "data_type": "char",
            "value": 123,
            "line": 135,
            "column": 55
        }
        symbol_table: SymbolTable = {"errors": []}
        
        _handle_literal(node, symbol_table)
        
        error = symbol_table["errors"][0]
        self.assertIn("int", error["message"])
        self.assertIn("got", error["message"].lower())


if __name__ == "__main__":
    unittest.main()
