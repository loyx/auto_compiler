# -*- coding: utf-8 -*-
"""单元测试：_parse_while_stmt 函数"""

import unittest
from unittest.mock import patch

from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt(unittest.TestCase):
    """测试 _parse_while_stmt 函数的解析逻辑"""

    def test_happy_path_basic_while(self):
        """测试基本 while 语句解析：while (expr) block"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 10, "column": 5},
                {"type": "LPAREN", "value": "(", "line": 10, "column": 11},
                {"type": "IDENT", "value": "x", "line": 10, "column": 12},
                {"type": "RPAREN", "value": ")", "line": 10, "column": 13},
                {"type": "LBRACE", "value": "{", "line": 10, "column": 15},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_condition_ast = {"type": "EXPR", "value": "x", "line": 10, "column": 12}
        mock_block_ast = {"type": "BLOCK", "children": [], "line": 10, "column": 15}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_block_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE")
            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 5)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], mock_condition_ast)
            self.assertEqual(result["children"][1], mock_block_ast)
            
            self.assertEqual(mock_consume.call_count, 3)
            mock_consume.assert_any_call(parser_state, "WHILE")
            mock_consume.assert_any_call(parser_state, "LPAREN")
            mock_consume.assert_any_call(parser_state, "RPAREN")
            mock_parse_expr.assert_called_once_with(parser_state)
            mock_parse_block.assert_called_once_with(parser_state)

    def test_while_with_complex_condition(self):
        """测试 while 语句带复杂条件表达式"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 20, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 20, "column": 7},
                {"type": "IDENT", "value": "i", "line": 20, "column": 8},
                {"type": "LT", "value": "<", "line": 20, "column": 10},
                {"type": "NUMBER", "value": "10", "line": 20, "column": 12},
                {"type": "RPAREN", "value": ")", "line": 20, "column": 14},
                {"type": "LBRACE", "value": "{", "line": 20, "column": 16},
            ],
            "pos": 0,
            "filename": "loop.c"
        }
        
        mock_condition_ast = {
            "type": "BINOP",
            "children": [
                {"type": "IDENT", "value": "i"},
                {"type": "NUMBER", "value": "10"}
            ],
            "value": "<"
        }
        mock_block_ast = {"type": "BLOCK", "children": [], "line": 20, "column": 16}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_block_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE")
            self.assertEqual(result["line"], 20)
            self.assertEqual(result["column"], 1)
            self.assertEqual(result["children"][0], mock_condition_ast)

    def test_while_with_nested_block(self):
        """测试 while 语句带嵌套语句块"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 30, "column": 0},
                {"type": "LPAREN", "value": "(", "line": 30, "column": 6},
                {"type": "NUMBER", "value": "1", "line": 30, "column": 7},
                {"type": "RPAREN", "value": ")", "line": 30, "column": 8},
                {"type": "LBRACE", "value": "{", "line": 30, "column": 10},
            ],
            "pos": 0,
            "filename": "infinite.c"
        }
        
        mock_condition_ast = {"type": "NUMBER", "value": "1", "line": 30, "column": 7}
        mock_block_ast = {
            "type": "BLOCK",
            "children": [
                {"type": "RETURN", "value": "0"}
            ],
            "line": 30,
            "column": 10
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_block_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][1]["type"], "BLOCK")
            self.assertEqual(len(result["children"][1]["children"]), 1)

    def test_while_at_different_position(self):
        """测试 while token 在不同位置（pos 不为 0）"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 0},
                {"type": "SEMI", "value": ";", "line": 1, "column": 1},
                {"type": "WHILE", "value": "while", "line": 2, "column": 0},
                {"type": "LPAREN", "value": "(", "line": 2, "column": 6},
                {"type": "IDENT", "value": "y", "line": 2, "column": 7},
                {"type": "RPAREN", "value": ")", "line": 2, "column": 8},
                {"type": "LBRACE", "value": "{", "line": 2, "column": 10},
            ],
            "pos": 2,
            "filename": "multi.c"
        }
        
        mock_condition_ast = {"type": "IDENT", "value": "y", "line": 2, "column": 7}
        mock_block_ast = {"type": "BLOCK", "children": [], "line": 2, "column": 10}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_block_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 0)

    def test_while_token_without_line_column(self):
        """测试 WHILE token 缺少 line/column 字段时的默认值"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while"},
                {"type": "LPAREN", "value": "("},
                {"type": "NUMBER", "value": "0"},
                {"type": "RPAREN", "value": ")"},
                {"type": "LBRACE", "value": "{"},
            ],
            "pos": 0,
            "filename": "no_location.c"
        }
        
        mock_condition_ast = {"type": "NUMBER", "value": "0"}
        mock_block_ast = {"type": "BLOCK", "children": []}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_block_ast
            
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE")
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)

    def test_parser_state_modified_by_consume(self):
        """验证 parser_state 被 _consume_token 修改（pos 递增）"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 5, "column": 0},
                {"type": "LPAREN", "value": "(", "line": 5, "column": 6},
                {"type": "IDENT", "value": "flag", "line": 5, "column": 7},
                {"type": "RPAREN", "value": ")", "line": 5, "column": 11},
                {"type": "LBRACE", "value": "{", "line": 5, "column": 13},
            ],
            "pos": 0,
            "filename": "state.c"
        }
        
        mock_condition_ast = {"type": "IDENT", "value": "flag"}
        mock_block_ast = {"type": "BLOCK", "children": []}
        
        def consume_side_effect(state, expected_type):
            state["pos"] += 1
            return state["tokens"][state["pos"] - 1]
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_consume.side_effect = consume_side_effect
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_block_ast
            
            initial_pos = parser_state["pos"]
            result = _parse_while_stmt(parser_state)
            
            self.assertEqual(result["type"], "WHILE")
            self.assertEqual(parser_state["pos"], initial_pos + 3)
            self.assertEqual(mock_consume.call_count, 3)

    def test_parse_expr_error_propagation(self):
        """测试 _parse_expr 抛出异常时的传播"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 0},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "INVALID", "value": "?", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "error.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.side_effect = SyntaxError("Invalid expression")
            
            with self.assertRaises(SyntaxError):
                _parse_while_stmt(parser_state)
            
            mock_consume.assert_called_with(parser_state, "LPAREN")
            mock_parse_block.assert_not_called()

    def test_parse_block_error_propagation(self):
        """测试 _parse_block 抛出异常时的传播"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 0},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 7},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 8},
                {"type": "INVALID", "value": "?", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "block_error.c"
        }
        
        mock_condition_ast = {"type": "NUMBER", "value": "1"}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_expr_src._parse_expr") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_src._parse_block") as mock_parse_block:
            
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.side_effect = SyntaxError("Invalid block")
            
            with self.assertRaises(SyntaxError):
                _parse_while_stmt(parser_state)
            
            self.assertEqual(mock_consume.call_count, 3)
            mock_parse_block.assert_called_once_with(parser_state)


if __name__ == "__main__":
    unittest.main()
