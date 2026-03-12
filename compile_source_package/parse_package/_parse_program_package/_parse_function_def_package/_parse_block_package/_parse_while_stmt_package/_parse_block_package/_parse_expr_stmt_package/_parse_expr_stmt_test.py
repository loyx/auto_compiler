# -*- coding: utf-8 -*-
"""单元测试：_parse_expr_stmt 函数"""

import unittest
from unittest.mock import patch

from ._parse_expr_stmt_src import _parse_expr_stmt


class TestParseExprStmt(unittest.TestCase):
    """测试 _parse_expr_stmt 函数的各种场景"""

    def test_happy_path_valid_expression_with_semicolon(self):
        """正常路径：有效的表达式后跟分号"""
        mock_expression_node = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "NUMBER", "value": 5}
            ],
            "line": 1,
            "column": 0
        }
        
        mock_first_token = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        
        mock_semicolon_token = {
            "type": "SEMICOLON",
            "value": ";",
            "line": 1,
            "column": 5
        }
        
        mock_parser_state = {
            "tokens": [mock_first_token, mock_semicolon_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            with patch("._parse_expr_stmt_src._parse_expression") as mock_parse_expr:
                with patch("._parse_expr_stmt_src._consume_token") as mock_consume:
                    # 第一次 _peek_token 返回表达式起始 token
                    # 第二次 _peek_token 返回分号 token
                    mock_peek.side_effect = [mock_first_token, mock_semicolon_token]
                    mock_parse_expr.return_value = mock_expression_node
                    mock_consume.return_value = mock_parser_state
                    
                    result = _parse_expr_stmt(mock_parser_state)
                    
                    self.assertEqual(result["type"], "EXPR_STMT")
                    self.assertEqual(result["children"], [mock_expression_node])
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 0)
                    
                    # 验证 _parse_expression 被调用一次
                    mock_parse_expr.assert_called_once_with(mock_parser_state)
                    
                    # 验证 _consume_token 被调用一次，期望类型为 SEMICOLON
                    mock_consume.assert_called_once_with(mock_parser_state, "SEMICOLON")

    def test_empty_input_raises_syntax_error(self):
        """边界情况：输入为空（无 token）时抛出 SyntaxError"""
        mock_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            mock_peek.return_value = None
            
            with self.assertRaises(SyntaxError) as context:
                _parse_expr_stmt(mock_parser_state)
            
            self.assertIn("Unexpected end of input", str(context.exception))

    def test_missing_semicolon_raises_syntax_error(self):
        """边界情况：表达式后缺少分号时抛出 SyntaxError"""
        mock_expression_node = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        
        mock_first_token = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        
        mock_wrong_token = {
            "type": "RPAREN",
            "value": ")",
            "line": 1,
            "column": 2
        }
        
        mock_parser_state = {
            "tokens": [mock_first_token, mock_wrong_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            with patch("._parse_expr_stmt_src._parse_expression") as mock_parse_expr:
                # 第一次返回表达式起始 token，第二次返回错误 token
                mock_peek.side_effect = [mock_first_token, mock_wrong_token]
                mock_parse_expr.return_value = mock_expression_node
                
                with self.assertRaises(SyntaxError) as context:
                    _parse_expr_stmt(mock_parser_state)
                
                error_msg = str(context.exception)
                self.assertIn("test.c:1:0", error_msg)
                self.assertIn("期望 ';'", error_msg)
                self.assertIn("RPAREN", error_msg)
                
                # 验证 _consume_token 未被调用（在验证分号前就失败了）
                # 注意：这里不需要验证 consume_token，因为它在 raise 之后

    def test_eof_after_expression_raises_syntax_error(self):
        """边界情况：表达式后到达文件末尾（EOF）时抛出 SyntaxError"""
        mock_expression_node = {
            "type": "NUMBER",
            "value": 42,
            "line": 2,
            "column": 5
        }
        
        mock_first_token = {
            "type": "NUMBER",
            "value": "42",
            "line": 2,
            "column": 5
        }
        
        mock_parser_state = {
            "tokens": [mock_first_token],
            "pos": 0,
            "filename": "main.c"
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            with patch("._parse_expr_stmt_src._parse_expression") as mock_parse_expr:
                # 第一次返回表达式起始 token，第二次返回 None（EOF）
                mock_peek.side_effect = [mock_first_token, None]
                mock_parse_expr.return_value = mock_expression_node
                
                with self.assertRaises(SyntaxError) as context:
                    _parse_expr_stmt(mock_parser_state)
                
                error_msg = str(context.exception)
                self.assertIn("main.c:2:5", error_msg)
                self.assertIn("期望 ';'", error_msg)
                self.assertIn("EOF", error_msg)

    def test_unknown_filename_defaults_correctly(self):
        """边界情况：parser_state 中缺少 filename 时使用默认值"""
        mock_expression_node = {
            "type": "IDENTIFIER",
            "value": "y",
            "line": 3,
            "column": 10
        }
        
        mock_first_token = {
            "type": "IDENTIFIER",
            "value": "y",
            "line": 3,
            "column": 10
        }
        
        mock_semicolon_token = {
            "type": "SEMICOLON",
            "value": ";",
            "line": 3,
            "column": 12
        }
        
        mock_parser_state = {
            "tokens": [mock_first_token, mock_semicolon_token],
            "pos": 0
            # 注意：没有 filename 字段
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            with patch("._parse_expr_stmt_src._parse_expression") as mock_parse_expr:
                with patch("._parse_expr_stmt_src._consume_token") as mock_consume:
                    mock_peek.side_effect = [mock_first_token, mock_semicolon_token]
                    mock_parse_expr.return_value = mock_expression_node
                    mock_consume.return_value = mock_parser_state
                    
                    result = _parse_expr_stmt(mock_parser_state)
                    
                    self.assertEqual(result["type"], "EXPR_STMT")
                    self.assertEqual(result["line"], 3)
                    self.assertEqual(result["column"], 10)

    def test_token_missing_line_column_uses_defaults(self):
        """边界情况：token 缺少 line/column 字段时使用默认值 0"""
        mock_expression_node = {
            "type": "CALL",
            "value": "func()",
            "line": 0,
            "column": 0
        }
        
        mock_first_token = {
            "type": "IDENTIFIER",
            "value": "func"
            # 注意：没有 line 和 column 字段
        }
        
        mock_semicolon_token = {
            "type": "SEMICOLON",
            "value": ";"
        }
        
        mock_parser_state = {
            "tokens": [mock_first_token, mock_semicolon_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            with patch("._parse_expr_stmt_src._parse_expression") as mock_parse_expr:
                with patch("._parse_expr_stmt_src._consume_token") as mock_consume:
                    mock_peek.side_effect = [mock_first_token, mock_semicolon_token]
                    mock_parse_expr.return_value = mock_expression_node
                    mock_consume.return_value = mock_parser_state
                    
                    result = _parse_expr_stmt(mock_parser_state)
                    
                    # 验证默认值为 0
                    self.assertEqual(result["line"], 0)
                    self.assertEqual(result["column"], 0)

    def test_parse_expression_error_propagates(self):
        """依赖异常：_parse_expression 抛出的异常应该向上传播"""
        mock_first_token = {
            "type": "INVALID",
            "value": "@",
            "line": 5,
            "column": 3
        }
        
        mock_parser_state = {
            "tokens": [mock_first_token],
            "pos": 0,
            "filename": "error.c"
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            with patch("._parse_expr_stmt_src._parse_expression") as mock_parse_expr:
                mock_peek.return_value = mock_first_token
                mock_parse_expr.side_effect = SyntaxError("Invalid expression syntax")
                
                with self.assertRaises(SyntaxError) as context:
                    _parse_expr_stmt(mock_parser_state)
                
                self.assertEqual(str(context.exception), "Invalid expression syntax")
                
                # 验证 _consume_token 未被调用（在 parse_expression 失败后就停止了）

    def test_complex_expression_node(self):
        """多分支逻辑：复杂嵌套表达式节点"""
        mock_expression_node = {
            "type": "BINARY_OP",
            "operator": "+",
            "children": [
                {
                    "type": "BINARY_OP",
                    "operator": "*",
                    "children": [
                        {"type": "NUMBER", "value": 2},
                        {"type": "IDENTIFIER", "value": "x"}
                    ]
                },
                {
                    "type": "CALL",
                    "children": [
                        {"type": "IDENTIFIER", "value": "foo"},
                        {"type": "NUMBER", "value": 1}
                    ]
                }
            ],
            "line": 10,
            "column": 0
        }
        
        mock_first_token = {
            "type": "NUMBER",
            "value": "2",
            "line": 10,
            "column": 0
        }
        
        mock_semicolon_token = {
            "type": "SEMICOLON",
            "value": ";",
            "line": 10,
            "column": 20
        }
        
        mock_parser_state = {
            "tokens": [mock_first_token, mock_semicolon_token],
            "pos": 0,
            "filename": "complex.c"
        }
        
        with patch("._parse_expr_stmt_src._peek_token") as mock_peek:
            with patch("._parse_expr_stmt_src._parse_expression") as mock_parse_expr:
                with patch("._parse_expr_stmt_src._consume_token") as mock_consume:
                    mock_peek.side_effect = [mock_first_token, mock_semicolon_token]
                    mock_parse_expr.return_value = mock_expression_node
                    mock_consume.return_value = mock_parser_state
                    
                    result = _parse_expr_stmt(mock_parser_state)
                    
                    self.assertEqual(result["type"], "EXPR_STMT")
                    self.assertEqual(len(result["children"]), 1)
                    self.assertEqual(result["children"][0]["type"], "BINARY_OP")
                    self.assertEqual(result["children"][0]["operator"], "+")


if __name__ == "__main__":
    unittest.main()
