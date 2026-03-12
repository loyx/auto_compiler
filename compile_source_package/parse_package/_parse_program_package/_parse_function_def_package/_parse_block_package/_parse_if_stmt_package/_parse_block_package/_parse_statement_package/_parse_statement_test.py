# -*- coding: utf-8 -*-
"""单元测试：_parse_statement 函数"""

import unittest
from unittest.mock import patch

from ._parse_statement_src import _parse_statement


class TestParseStatement(unittest.TestCase):
    """测试 _parse_statement 函数的语句分发逻辑"""

    def _create_parser_state(self, tokens, pos=0, filename="test.src"):
        """辅助函数：创建 parser_state 对象"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type, value, line=1, column=1):
        """辅助函数：创建 Token 对象"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== Happy Path Tests ====================

    def test_parse_var_decl_with_var_keyword(self):
        """测试 VAR 关键字分发到 _parse_var_decl"""
        tokens = [
            self._create_token("VAR", "var"),
            self._create_token("IDENTIFIER", "x"),
            self._create_token("ASSIGN", "="),
            self._create_token("NUMBER", "5"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "VAR_DECL", "children": []}
        
        with patch("._parse_statement_src._parse_var_decl") as mock_parse_var_decl:
            mock_parse_var_decl.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_var_decl.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_var_decl_with_let_keyword(self):
        """测试 LET 关键字分发到 _parse_var_decl"""
        tokens = [
            self._create_token("LET", "let"),
            self._create_token("IDENTIFIER", "x"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "VAR_DECL", "children": []}
        
        with patch("._parse_statement_src._parse_var_decl") as mock_parse_var_decl:
            mock_parse_var_decl.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_var_decl.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_if_stmt(self):
        """测试 IF 关键字分发到 _parse_if_stmt"""
        tokens = [
            self._create_token("IF", "if"),
            self._create_token("LPAREN", "("),
            self._create_token("IDENTIFIER", "x"),
            self._create_token("RPAREN", ")"),
            self._create_token("LBRACE", "{"),
            self._create_token("RBRACE", "}")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "IF_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_if_stmt") as mock_parse_if_stmt:
            mock_parse_if_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_if_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_while_stmt(self):
        """测试 WHILE 关键字分发到 _parse_while_stmt"""
        tokens = [
            self._create_token("WHILE", "while"),
            self._create_token("LPAREN", "("),
            self._create_token("IDENTIFIER", "x"),
            self._create_token("RPAREN", ")"),
            self._create_token("LBRACE", "{"),
            self._create_token("RBRACE", "}")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "WHILE_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_while_stmt") as mock_parse_while_stmt:
            mock_parse_while_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_while_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_for_stmt(self):
        """测试 FOR 关键字分发到 _parse_for_stmt"""
        tokens = [
            self._create_token("FOR", "for"),
            self._create_token("LPAREN", "("),
            self._create_token("IDENTIFIER", "i"),
            self._create_token("SEMICOLON", ";"),
            self._create_token("RPAREN", ")"),
            self._create_token("LBRACE", "{"),
            self._create_token("RBRACE", "}")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "FOR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_for_stmt") as mock_parse_for_stmt:
            mock_parse_for_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_for_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_return_stmt(self):
        """测试 RETURN 关键字分发到 _parse_return_stmt"""
        tokens = [
            self._create_token("RETURN", "return"),
            self._create_token("NUMBER", "5"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "RETURN_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_return_stmt") as mock_parse_return_stmt:
            mock_parse_return_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_return_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_break_stmt(self):
        """测试 BREAK 关键字分发到 _parse_break_stmt"""
        tokens = [
            self._create_token("BREAK", "break"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "BREAK_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_break_stmt") as mock_parse_break_stmt:
            mock_parse_break_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_break_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_continue_stmt(self):
        """测试 CONTINUE 关键字分发到 _parse_continue_stmt"""
        tokens = [
            self._create_token("CONTINUE", "continue"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "CONTINUE_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_continue_stmt") as mock_parse_continue_stmt:
            mock_parse_continue_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_continue_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expr_stmt_with_identifier(self):
        """测试标识符分发到 _parse_expr_stmt"""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
            self._create_token("ASSIGN", "="),
            self._create_token("NUMBER", "5"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expr_stmt_with_number(self):
        """测试数字字面量分发到 _parse_expr_stmt"""
        tokens = [
            self._create_token("NUMBER", "42"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expr_stmt_with_string(self):
        """测试字符串字面量分发到 _parse_expr_stmt"""
        tokens = [
            self._create_token("STRING", '"hello"'),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_expr_stmt_with_function_call(self):
        """测试函数调用分发到 _parse_expr_stmt"""
        tokens = [
            self._create_token("IDENTIFIER", "func"),
            self._create_token("LPAREN", "("),
            self._create_token("RPAREN", ")"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    # ==================== Boundary/Edge Cases ====================

    def test_empty_token_list_raises_syntax_error(self):
        """测试空 token 列表抛出 SyntaxError"""
        parser_state = self._create_parser_state([])
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.src", str(context.exception))

    def test_pos_at_end_raises_syntax_error(self):
        """测试 pos 在末尾时抛出 SyntaxError"""
        tokens = [self._create_token("NUMBER", "1")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_beyond_end_raises_syntax_error(self):
        """测试 pos 超出范围时抛出 SyntaxError"""
        tokens = [self._create_token("NUMBER", "1")]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_error_message_contains_filename(self):
        """测试错误消息包含文件名"""
        custom_filename = "custom/path/to/file.src"
        parser_state = self._create_parser_state([], filename=custom_filename)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn(custom_filename, str(context.exception))

    # ==================== Multi-statement Context ====================

    def test_parse_statement_at_non_zero_position(self):
        """测试在非零位置解析语句"""
        tokens = [
            self._create_token("NUMBER", "1"),
            self._create_token("SEMICOLON", ";"),
            self._create_token("VAR", "var"),
            self._create_token("IDENTIFIER", "x"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens, pos=2)
        
        mock_ast = {"type": "VAR_DECL", "children": []}
        
        with patch("._parse_statement_src._parse_var_decl") as mock_parse_var_decl:
            mock_parse_var_decl.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_var_decl.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_parse_statement_preserves_parser_state_reference(self):
        """测试 parser_state 引用被传递给子函数"""
        tokens = [self._create_token("IF", "if")]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "IF_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_if_stmt") as mock_parse_if_stmt:
            mock_parse_if_stmt.return_value = mock_ast
            _parse_statement(parser_state)
            
            # 验证传递的是同一个对象引用
            called_args = mock_parse_if_stmt.call_args[0][0]
            self.assertIs(called_args, parser_state)

    # ==================== Token Type Coverage ====================

    def test_unknown_token_type_falls_back_to_expr_stmt(self):
        """测试未知 token 类型回退到表达式语句"""
        tokens = [
            self._create_token("UNKNOWN_TYPE", "unknown"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_operator_token_falls_back_to_expr_stmt(self):
        """测试运算符 token 回退到表达式语句"""
        tokens = [
            self._create_token("PLUS", "+"),
            self._create_token("NUMBER", "1"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_boolean_literal_falls_back_to_expr_stmt(self):
        """测试布尔字面量回退到表达式语句"""
        tokens = [
            self._create_token("TRUE", "true"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_null_literal_falls_back_to_expr_stmt(self):
        """测试 null 字面量回退到表达式语句"""
        tokens = [
            self._create_token("NULL", "null"),
            self._create_token("SEMICOLON", ";")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "EXPR_STMT", "children": []}
        
        with patch("._parse_statement_src._parse_expr_stmt") as mock_parse_expr_stmt:
            mock_parse_expr_stmt.return_value = mock_ast
            result = _parse_statement(parser_state)
            
            mock_parse_expr_stmt.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)


if __name__ == "__main__":
    unittest.main()
