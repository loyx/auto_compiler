# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._check_expression_types_src import (
    _check_expression_types,
    _check_arithmetic_op,
    _check_logical_op,
    _check_comparison_op,
    _check_assignment_op,
    _add_error,
)

# === type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestCheckExpressionTypes(unittest.TestCase):
    """Test cases for _check_expression_types function."""

    def test_arithmetic_operator_int_operands(self):
        """Test arithmetic operator with int operands - no errors expected."""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 1, "column": 1},
                {"type": "literal", "value": 2, "data_type": "int", "line": 1, "column": 3},
            ],
            "line": 1,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arithmetic_operator_char_operand(self):
        """Test arithmetic operator with char operand - error expected."""
        node: AST = {
            "type": "expression",
            "value": "*",
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 2, "column": 1},
                {"type": "literal", "value": "a", "data_type": "char", "line": 2, "column": 3},
            ],
            "line": 2,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("算术运算符要求操作数为 int 类型", symbol_table["errors"][0]["message"])

    def test_logical_operator_int_operands(self):
        """Test logical operator with int operands - no errors expected."""
        node: AST = {
            "type": "expression",
            "value": "&&",
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 3, "column": 1},
                {"type": "literal", "value": 0, "data_type": "int", "line": 3, "column": 4},
            ],
            "line": 3,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_logical_operator_char_operand(self):
        """Test logical operator with char operand - error expected."""
        node: AST = {
            "type": "expression",
            "value": "||",
            "children": [
                {"type": "literal", "value": "x", "data_type": "char", "line": 4, "column": 1},
            ],
            "line": 4,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("逻辑运算符要求操作数为 int 类型", symbol_table["errors"][0]["message"])

    def test_not_operator_int_operand(self):
        """Test ! operator with int operand - no errors expected."""
        node: AST = {
            "type": "expression",
            "value": "!",
            "children": [
                {"type": "literal", "value": 1, "data_type": "int", "line": 5, "column": 1},
            ],
            "line": 5,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_comparison_operator_same_types(self):
        """Test comparison operator with same operand types - no errors expected."""
        node: AST = {
            "type": "expression",
            "value": "==",
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 6, "column": 1},
                {"type": "literal", "value": 10, "data_type": "int", "line": 6, "column": 4},
            ],
            "line": 6,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_comparison_operator_different_types(self):
        """Test comparison operator with different operand types - error expected."""
        node: AST = {
            "type": "expression",
            "value": "!=",
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 7, "column": 1},
                {"type": "literal", "value": "a", "data_type": "char", "line": 7, "column": 4},
            ],
            "line": 7,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("比较运算符要求操作数类型一致", symbol_table["errors"][0]["message"])

    def test_comparison_operator_single_operand(self):
        """Test comparison operator with single operand - no error (early return)."""
        node: AST = {
            "type": "expression",
            "value": "<",
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 8, "column": 1},
            ],
            "line": 8,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_assignment_operator_valid(self):
        """Test assignment operator with valid declared variable - no errors expected."""
        node: AST = {
            "type": "expression",
            "value": "=",
            "children": [
                {"type": "identifier", "value": "x", "line": 9, "column": 1},
                {"type": "literal", "value": 10, "data_type": "int", "line": 9, "column": 3},
            ],
            "line": 9,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": [],
        }
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_assignment_operator_undeclared_variable(self):
        """Test assignment operator with undeclared variable - error expected."""
        node: AST = {
            "type": "expression",
            "value": "=",
            "children": [
                {"type": "identifier", "value": "y", "line": 10, "column": 1},
                {"type": "literal", "value": 5, "data_type": "int", "line": 10, "column": 3},
            ],
            "line": 10,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": [],
        }
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("变量 'y' 未声明", symbol_table["errors"][0]["message"])

    def test_assignment_operator_type_mismatch(self):
        """Test assignment operator with type mismatch - error expected."""
        node: AST = {
            "type": "expression",
            "value": "=",
            "children": [
                {"type": "identifier", "value": "z", "line": 11, "column": 1},
                {"type": "literal", "value": "a", "data_type": "char", "line": 11, "column": 3},
            ],
            "line": 11,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "z": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": [],
        }
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("赋值类型不兼容", symbol_table["errors"][0]["message"])

    def test_assignment_operator_non_identifier_left(self):
        """Test assignment operator with non-identifier left value - error expected."""
        node: AST = {
            "type": "expression",
            "value": "=",
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 12, "column": 1},
                {"type": "literal", "value": 10, "data_type": "int", "line": 12, "column": 3},
            ],
            "line": 12,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("赋值运算符左值必须为 identifier", symbol_table["errors"][0]["message"])

    def test_assignment_operator_insufficient_children(self):
        """Test assignment operator with insufficient children - no error (early return)."""
        node: AST = {
            "type": "expression",
            "value": "=",
            "children": [
                {"type": "identifier", "value": "x", "line": 13, "column": 1},
            ],
            "line": 13,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_unknown_operator(self):
        """Test unknown operator - no errors expected (no handler)."""
        node: AST = {
            "type": "expression",
            "value": "%",
            "children": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 14, "column": 1},
            ],
            "line": 14,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_empty_children(self):
        """Test expression with empty children - no crash."""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": [],
            "line": 15,
            "column": 1,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_symbol_table_errors_field(self):
        """Test when symbol_table doesn't have errors field - should create it."""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "literal", "value": "a", "data_type": "char", "line": 16, "column": 1},
            ],
            "line": 16,
            "column": 1,
        }
        symbol_table: SymbolTable = {}
        _check_expression_types(node, symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_error_record_structure(self):
        """Test that error records have correct structure."""
        node: AST = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "literal", "value": "x", "data_type": "char", "line": 17, "column": 5},
            ],
            "line": 17,
            "column": 5,
        }
        symbol_table: SymbolTable = {"errors": []}
        _check_expression_types(node, symbol_table)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_mismatch")
        self.assertEqual(error["line"], 17)
        self.assertEqual(error["column"], 5)
        self.assertEqual(error["node_type"], "expression")
        self.assertIn("message", error)


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions."""

    def test_check_arithmetic_op_multiple_errors(self):
        """Test _check_arithmetic_op with multiple char operands."""
        children = [
            {"data_type": "char"},
            {"data_type": "char"},
            {"data_type": "int"},
        ]
        symbol_table: SymbolTable = {"errors": []}
        _check_arithmetic_op(children, symbol_table, 1, 1)
        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_check_logical_op_empty_children(self):
        """Test _check_logical_op with empty children."""
        symbol_table: SymbolTable = {"errors": []}
        _check_logical_op([], symbol_table, 1, 1)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_check_comparison_op_all_same_type(self):
        """Test _check_comparison_op with all same types."""
        children = [
            {"data_type": "int"},
            {"data_type": "int"},
            {"data_type": "int"},
        ]
        symbol_table: SymbolTable = {"errors": []}
        _check_comparison_op(children, symbol_table, 1, 1)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_check_comparison_op_multiple_mismatches(self):
        """Test _check_comparison_op with multiple type mismatches."""
        children = [
            {"data_type": "int"},
            {"data_type": "char"},
            {"data_type": "char"},
        ]
        symbol_table: SymbolTable = {"errors": []}
        _check_comparison_op(children, symbol_table, 1, 1)
        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_check_assignment_op_not_declared_variable(self):
        """Test _check_assignment_op with variable that exists but not declared."""
        children = [
            {"type": "identifier", "value": "x"},
            {"data_type": "int"},
        ]
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": False}
            },
            "errors": [],
        }
        _check_assignment_op(children, symbol_table, 1, 1)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("未声明", symbol_table["errors"][0]["message"])

    def test_add_error_creates_errors_list(self):
        """Test _add_error creates errors list if not exists."""
        symbol_table: SymbolTable = {}
        _add_error(symbol_table, 10, 20, "Test error")
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "Test error")
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 20)

    def test_add_error_appends_to_existing_list(self):
        """Test _add_error appends to existing errors list."""
        symbol_table: SymbolTable = {"errors": [{"message": "Existing"}]}
        _add_error(symbol_table, 5, 5, "New error")
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][1]["message"], "New error")


if __name__ == "__main__":
    unittest.main()
