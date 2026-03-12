# -*- coding: utf-8 -*-
"""单元测试文件：测试 _parse_factor 函数"""

import unittest
from unittest.mock import patch

from ._parse_factor_src import _parse_factor


class TestParseFactor(unittest.TestCase):
    """测试 _parse_factor 函数的各种场景"""

    def test_empty_tokens(self):
        """测试 tokens 为空的情况"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        result = _parse_factor(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state["error"], "Unexpected end of input: expected factor")

    def test_pos_out_of_bounds(self):
        """测试 pos 越界的情况"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        result = _parse_factor(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state["error"], "Unexpected end of input: expected factor")

    def test_primary_identifier(self):
        """测试解析标识符（primary）"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 1
            }
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            mock_get_primary.assert_called_once()

    def test_primary_literal(self):
        """测试解析字面量（primary）"""
        parser_state = {
            "tokens": [
                {"type": "LITERAL", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "LITERAL",
                "value": "42",
                "children": [],
                "line": 1,
                "column": 1
            }
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "42")

    def test_unary_plus(self):
        """测试一元加运算符"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)

    def test_unary_minus(self):
        """测试一元减运算符"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "LITERAL",
                "value": "5",
                "children": [],
                "line": 1,
                "column": 2
            }
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 1)

    def test_nested_unary_operators(self):
        """测试嵌套一元运算符：--x"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
            result = _parse_factor(parser_state)
            
            # 外层 UNARY_OP
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # 内层 UNARY_OP
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["value"], "-")
            self.assertEqual(inner["line"], 1)
            self.assertEqual(inner["column"], 2)
            
            # 最内层 IDENTIFIER
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 2)

    def test_parentheses_expression(self):
        """测试括号表达式：(x)"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        def mock_expr_impl(state):
            state["pos"] = 2  # 消耗 IDENTIFIER
            return {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_expression") as mock_get_expr:
            mock_get_expr.return_value.side_effect = mock_expr_impl
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 3)
            mock_get_expr.assert_called_once()

    def test_parentheses_complex_expression(self):
        """测试括号内复杂表达式：(1+2)"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "LITERAL", "value": "1", "line": 1, "column": 2},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "LITERAL", "value": "2", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        def mock_expr_impl(state):
            state["pos"] = 4  # 消耗 LITERAL, PLUS, LITERAL
            return {
                "type": "BINARY_OP",
                "value": "+",
                "children": [
                    {"type": "LITERAL", "value": "1", "line": 1, "column": 2},
                    {"type": "LITERAL", "value": "2", "line": 1, "column": 4}
                ],
                "line": 1,
                "column": 2
            }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_expression") as mock_get_expr:
            mock_get_expr.return_value.side_effect = mock_expr_impl
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 5)

    def test_nested_parentheses(self):
        """测试嵌套括号：((x))"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        def mock_expr_impl(state):
            # 模拟 _parse_expression 的行为：消耗括号内的所有内容
            # 对于 ((x))，当 _parse_expression 被调用时，pos 指向内层 LPAREN
            # 它应该处理 (x) 并返回，pos 应该指向外层 RPAREN
            state["pos"] = 4  # 消耗 (, x, )
            return {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_expression") as mock_get_expr:
            mock_get_expr.return_value.side_effect = mock_expr_impl
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 5)

    def test_missing_rparen(self):
        """测试缺少右括号的情况：(x"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_expression") as mock_get_expr:
            mock_get_expr.return_value.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Expected ')'")
            self.assertEqual(parser_state["error"], "Expected ')' after expression")

    def test_missing_rparen_at_end(self):
        """测试右括号在末尾缺失"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_expression") as mock_get_expr:
            mock_get_expr.return_value.return_value = {
                "type": "ERROR",
                "value": "Unexpected end",
                "children": [],
                "line": 0,
                "column": 0
            }
            parser_state["error"] = "Unexpected end"
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["error"], "Unexpected end")

    def test_unary_with_error_in_operand(self):
        """测试一元运算符后操作数解析错误"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "ERROR",
                "value": "Unexpected end",
                "children": [],
                "line": 0,
                "column": 0
            }
            parser_state["error"] = "Unexpected end of input: expected factor"
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["error"], "Unexpected end of input: expected factor")

    def test_parentheses_with_error_in_expression(self):
        """测试括号内表达式解析错误"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_expression") as mock_get_expr:
            mock_get_expr.return_value.return_value = {
                "type": "ERROR",
                "value": "Syntax error",
                "children": [],
                "line": 1,
                "column": 1
            }
            parser_state["error"] = "Syntax error in expression"
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["error"], "Syntax error in expression")

    def test_unary_plus_literal(self):
        """测试一元加作用于字面量：+42"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "LITERAL", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "LITERAL",
                "value": "42",
                "children": [],
                "line": 1,
                "column": 2
            }
            result = _parse_factor(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(result["children"][0]["value"], "42")

    def test_multiple_unary_operators(self):
        """测试多个一元运算符：+-x"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
            result = _parse_factor(parser_state)
            
            # 外层是 PLUS
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # 内层是 MINUS
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["value"], "-")
            self.assertEqual(inner["line"], 1)
            self.assertEqual(inner["column"], 2)
            
            # 最内层是 IDENTIFIER
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")

    def test_pos_advanced_correctly_for_primary(self):
        """测试 primary 解析后 pos 正确推进"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        def mock_primary_impl(state):
            state["pos"] = 1
            return {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 1
            }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_package._parse_arith_expr_package._parse_term_package._parse_factor_package._parse_factor_src._get_parse_primary") as mock_get_primary:
            mock_get_primary.return_value.side_effect = mock_primary_impl
            result = _parse_factor(parser_state)
            
            # _parse_primary 应该推进 pos
            self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
