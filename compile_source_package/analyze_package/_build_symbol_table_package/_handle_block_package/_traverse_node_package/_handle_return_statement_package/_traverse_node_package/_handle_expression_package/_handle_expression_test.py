# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_expression 函数测试
"""
import unittest
from typing import Any, Dict, List

from ._handle_expression_src import _handle_expression, AST, SymbolTable


def create_ast_node(
    node_type: str = "expression",
    value: str = "",
    children: List[Dict[str, Any]] = None,
    data_type: str = "int",
    line: int = 1,
    column: int = 1
) -> AST:
    """Helper function to create AST nodes for testing."""
    return {
        "type": node_type,
        "value": value,
        "children": children if children is not None else [],
        "data_type": data_type,
        "line": line,
        "column": column
    }


def create_symbol_table() -> SymbolTable:
    """Helper function to create a fresh symbol table."""
    return {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": [0],
        "current_function": "",
        "errors": []
    }


class TestHandleExpressionArithmetic(unittest.TestCase):
    """测试算术运算符的类型检查。"""

    def test_arithmetic_with_int_operands_valid(self):
        """算术运算符 + 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arithmetic_minus_with_int_operands_valid(self):
        """算术运算符 - 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="-",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arithmetic_multiply_with_int_operands_valid(self):
        """算术运算符 * 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="*",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arithmetic_divide_with_int_operands_valid(self):
        """算术运算符 / 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="/",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arithmetic_modulo_with_int_operands_valid(self):
        """算术运算符 % 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="%",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arithmetic_with_char_operand_invalid(self):
        """算术运算符使用 char 操作数应报告类型错误。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="char")
            ],
            line=5,
            column=10
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type error", symbol_table["errors"][0])
        self.assertIn("arithmetic operations require int operands", symbol_table["errors"][0])
        self.assertIn("char", symbol_table["errors"][0])
        self.assertIn("line 5", symbol_table["errors"][0])

    def test_arithmetic_with_both_char_operands_invalid(self):
        """算术运算符使用两个 char 操作数应报告两个类型错误。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="char"),
                create_ast_node(value="b", data_type="char")
            ],
            line=3,
            column=5
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 2)
        for error in symbol_table["errors"]:
            self.assertIn("Type error", error)
            self.assertIn("arithmetic operations require int operands", error)


class TestHandleExpressionComparison(unittest.TestCase):
    """测试关系运算符的类型检查。"""

    def test_comparison_with_matching_int_types_valid(self):
        """关系运算符 == 使用匹配的 int 类型应无错误。"""
        node = create_ast_node(
            value="==",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_comparison_with_matching_char_types_valid(self):
        """关系运算符 == 使用匹配的 char 类型应无错误。"""
        node = create_ast_node(
            value="==",
            children=[
                create_ast_node(value="a", data_type="char"),
                create_ast_node(value="b", data_type="char")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_comparison_with_type_mismatch_invalid(self):
        """关系运算符使用不匹配的类型应报告错误。"""
        node = create_ast_node(
            value="!=",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="char")
            ],
            line=7,
            column=15
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type mismatch", symbol_table["errors"][0])
        self.assertIn("left is int but right is char", symbol_table["errors"][0])
        self.assertIn("line 7", symbol_table["errors"][0])

    def test_comparison_less_than_with_matching_types_valid(self):
        """关系运算符 < 使用匹配类型应无错误。"""
        node = create_ast_node(
            value="<",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_comparison_greater_than_with_matching_types_valid(self):
        """关系运算符 > 使用匹配类型应无错误。"""
        node = create_ast_node(
            value=">",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_comparison_less_equal_with_matching_types_valid(self):
        """关系运算符 <= 使用匹配类型应无错误。"""
        node = create_ast_node(
            value="<=",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_comparison_greater_equal_with_matching_types_valid(self):
        """关系运算符 >= 使用匹配类型应无错误。"""
        node = create_ast_node(
            value=">=",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)


class TestHandleExpressionLogical(unittest.TestCase):
    """测试逻辑运算符的类型检查。"""

    def test_logical_and_with_int_operands_valid(self):
        """逻辑运算符 && 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="&&",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_logical_or_with_int_operands_valid(self):
        """逻辑运算符 || 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="||",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_logical_not_with_int_operand_valid(self):
        """逻辑运算符 ! 使用 int 操作数应无错误。"""
        node = create_ast_node(
            value="!",
            children=[
                create_ast_node(value="a", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_logical_and_with_char_operand_invalid(self):
        """逻辑运算符 && 使用 char 操作数应报告类型错误。"""
        node = create_ast_node(
            value="&&",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="char")
            ],
            line=10,
            column=20
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type error", symbol_table["errors"][0])
        self.assertIn("logical operations require int operands", symbol_table["errors"][0])

    def test_logical_not_with_char_operand_invalid(self):
        """逻辑运算符 ! 使用 char 操作数应报告类型错误。"""
        node = create_ast_node(
            value="!",
            children=[
                create_ast_node(value="a", data_type="char")
            ],
            line=12,
            column=8
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type error", symbol_table["errors"][0])
        self.assertIn("logical operations require int operands", symbol_table["errors"][0])


class TestHandleExpressionOperandCount(unittest.TestCase):
    """测试操作数数量检查。"""

    def test_binary_operator_with_one_operand_invalid(self):
        """二元运算符只有一个操作数应报告错误。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="int")
            ],
            line=15,
            column=3
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Syntax error", symbol_table["errors"][0])
        self.assertIn("operator '+' expects 2 operands, got 1", symbol_table["errors"][0])

    def test_binary_operator_with_three_operands_invalid(self):
        """二元运算符有三个操作数应报告错误。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int"),
                create_ast_node(value="c", data_type="int")
            ],
            line=16,
            column=5
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Syntax error", symbol_table["errors"][0])
        self.assertIn("operator '+' expects 2 operands, got 3", symbol_table["errors"][0])

    def test_unary_operator_with_two_operands_invalid(self):
        """一元运算符 ! 有两个操作数应报告错误。"""
        node = create_ast_node(
            value="!",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ],
            line=18,
            column=7
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Syntax error", symbol_table["errors"][0])
        self.assertIn("operator '!' expects 1 operands, got 2", symbol_table["errors"][0])

    def test_unary_operator_with_zero_operands_invalid(self):
        """一元运算符 ! 没有操作数应报告错误。"""
        node = create_ast_node(
            value="!",
            children=[],
            line=20,
            column=9
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Syntax error", symbol_table["errors"][0])
        self.assertIn("operator '!' expects 1 operands, got 0", symbol_table["errors"][0])


class TestHandleExpressionEdgeCases(unittest.TestCase):
    """测试边界情况。"""

    def test_missing_line_column_uses_child_info(self):
        """当节点缺少 line/column 时，应从子节点获取。"""
        node = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "identifier", "value": "a", "data_type": "char", "line": 25, "column": 30},
                {"type": "identifier", "value": "b", "data_type": "int", "line": 25, "column": 30}
            ],
            "data_type": "int"
        }
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 25", symbol_table["errors"][0])
        self.assertIn("column 30", symbol_table["errors"][0])

    def test_missing_line_column_defaults_to_zero(self):
        """当节点和子节点都缺少 line/column 时，应默认为 0。"""
        node = {
            "type": "expression",
            "value": "+",
            "children": [
                {"type": "identifier", "value": "a", "data_type": "char"},
                {"type": "identifier", "value": "b", "data_type": "int"}
            ],
            "data_type": "int"
        }
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 0", symbol_table["errors"][0])
        self.assertIn("column 0", symbol_table["errors"][0])

    def test_empty_children_list(self):
        """空子节点列表应报告操作数数量错误。"""
        node = create_ast_node(
            value="+",
            children=[],
            line=30,
            column=1
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("operator '+' expects 2 operands, got 0", symbol_table["errors"][0])

    def test_unknown_data_type_treated_as_unknown(self):
        """未知数据类型应被记录为 unknown。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="unknown"),
                create_ast_node(value="b", data_type="int")
            ],
            line=32,
            column=5
        )
        symbol_table = create_symbol_table()
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("unknown", symbol_table["errors"][0])

    def test_errors_list_created_if_not_exists(self):
        """如果 symbol_table 中没有 errors 列表，应自动创建。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="char"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = {
            "variables": {},
            "functions": {}
        }
        _handle_expression(node, symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_no_side_effects_on_valid_expression(self):
        """有效的表达式不应产生任何错误。"""
        node = create_ast_node(
            value="+",
            children=[
                create_ast_node(value="a", data_type="int"),
                create_ast_node(value="b", data_type="int")
            ]
        )
        symbol_table = create_symbol_table()
        initial_errors = len(symbol_table["errors"])
        _handle_expression(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), initial_errors)


class TestHandleExpressionMixedOperators(unittest.TestCase):
    """测试混合运算符场景。"""

    def test_all_arithmetic_operators(self):
        """测试所有算术运算符。"""
        for op in ["+", "-", "*", "/", "%"]:
            with self.subTest(operator=op):
                node = create_ast_node(
                    value=op,
                    children=[
                        create_ast_node(value="a", data_type="int"),
                        create_ast_node(value="b", data_type="int")
                    ]
                )
                symbol_table = create_symbol_table()
                _handle_expression(node, symbol_table)
                self.assertEqual(len(symbol_table["errors"]), 0, f"Operator {op} should not produce errors")

    def test_all_comparison_operators(self):
        """测试所有关系运算符。"""
        for op in ["==", "!=", "<", ">", "<=", ">="]:
            with self.subTest(operator=op):
                node = create_ast_node(
                    value=op,
                    children=[
                        create_ast_node(value="a", data_type="int"),
                        create_ast_node(value="b", data_type="int")
                    ]
                )
                symbol_table = create_symbol_table()
                _handle_expression(node, symbol_table)
                self.assertEqual(len(symbol_table["errors"]), 0, f"Operator {op} should not produce errors")

    def test_all_logical_operators(self):
        """测试所有逻辑运算符。"""
        for op in ["&&", "||"]:
            with self.subTest(operator=op):
                node = create_ast_node(
                    value=op,
                    children=[
                        create_ast_node(value="a", data_type="int"),
                        create_ast_node(value="b", data_type="int")
                    ]
                )
                symbol_table = create_symbol_table()
                _handle_expression(node, symbol_table)
                self.assertEqual(len(symbol_table["errors"]), 0, f"Operator {op} should not produce errors")


if __name__ == "__main__":
    unittest.main()
