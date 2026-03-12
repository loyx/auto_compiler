# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_return_stmt_src import _parse_return_stmt


class TestParseReturnStmt(unittest.TestCase):
    """单元测试：_parse_return_stmt 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper: 创建 parser_state 对象"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper: 创建 token 对象"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_return_with_expression(self):
        """测试：return 语句带表达式"""
        tokens = [
            self._create_token("RETURN", "return", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("SEMICOLON", ";", 1, 9),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast
            
            result = _parse_return_stmt(parser_state)
            
            self.assertEqual(result["type"], "RETURN")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_expression_ast)
            self.assertEqual(parser_state["pos"], 3)
            mock_parse_expr.assert_called_once()

    def test_return_without_expression(self):
        """测试：return 语句不带表达式（return;）"""
        tokens = [
            self._create_token("RETURN", "return", 2, 5),
            self._create_token("SEMICOLON", ";", 2, 11),
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 2)

    def test_return_with_complex_expression(self):
        """测试：return 语句带复杂表达式（a + b * c）"""
        tokens = [
            self._create_token("RETURN", "return", 3, 1),
            self._create_token("IDENTIFIER", "a", 3, 8),
            self._create_token("PLUS", "+", 3, 10),
            self._create_token("IDENTIFIER", "b", 3, 12),
            self._create_token("STAR", "*", 3, 14),
            self._create_token("IDENTIFIER", "c", 3, 16),
            self._create_token("SEMICOLON", ";", 3, 17),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expression_ast = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "value": "a"},
            "right": {"type": "BINARY_OP", "operator": "*", "left": {"type": "IDENTIFIER", "value": "b"}, "right": {"type": "IDENTIFIER", "value": "c"}},
            "line": 3,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast
            
            result = _parse_return_stmt(parser_state)
            
            self.assertEqual(result["type"], "RETURN")
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_expression_ast)
            self.assertEqual(parser_state["pos"], 7)

    def test_return_missing_semicolon(self):
        """测试：return 语句缺少分号，应抛出 SyntaxError"""
        tokens = [
            self._create_token("RETURN", "return", 4, 1),
            self._create_token("IDENTIFIER", "x", 4, 8),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 4,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_return_stmt(parser_state)
            
            self.assertIn("Expected token type SEMICOLON", str(context.exception))

    def test_return_eof_without_semicolon(self):
        """测试：return 后直接 EOF，应抛出 SyntaxError"""
        tokens = [
            self._create_token("RETURN", "return", 5, 1),
        ]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("Expected token type SEMICOLON", str(context.exception))
        self.assertIn("EOF", str(context.exception))

    def test_return_with_number_literal(self):
        """测试：return 数字字面量"""
        tokens = [
            self._create_token("RETURN", "return", 6, 1),
            self._create_token("NUMBER", "42", 6, 8),
            self._create_token("SEMICOLON", ";", 6, 10),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expression_ast = {
            "type": "NUMBER",
            "value": 42,
            "line": 6,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast
            
            result = _parse_return_stmt(parser_state)
            
            self.assertEqual(result["type"], "RETURN")
            self.assertEqual(result["line"], 6)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "NUMBER")
            self.assertEqual(result["children"][0]["value"], 42)

    def test_return_with_string_literal(self):
        """测试：return 字符串字面量"""
        tokens = [
            self._create_token("RETURN", "return", 7, 1),
            self._create_token("STRING", '"hello"', 7, 8),
            self._create_token("SEMICOLON", ";", 7, 15),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expression_ast = {
            "type": "STRING",
            "value": "hello",
            "line": 7,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast
            
            result = _parse_return_stmt(parser_state)
            
            self.assertEqual(result["type"], "RETURN")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "STRING")

    def test_return_with_function_call(self):
        """测试：return 函数调用表达式"""
        tokens = [
            self._create_token("RETURN", "return", 8, 1),
            self._create_token("IDENTIFIER", "foo", 8, 8),
            self._create_token("LPAREN", "(", 8, 11),
            self._create_token("RPAREN", ")", 8, 12),
            self._create_token("SEMICOLON", ";", 8, 13),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expression_ast = {
            "type": "CALL",
            "callee": {"type": "IDENTIFIER", "value": "foo"},
            "arguments": [],
            "line": 8,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast
            
            result = _parse_return_stmt(parser_state)
            
            self.assertEqual(result["type"], "RETURN")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "CALL")

    def test_return_position_advancement(self):
        """测试：parser_state pos 正确前进"""
        tokens = [
            self._create_token("RETURN", "return", 9, 1),
            self._create_token("SEMICOLON", ";", 9, 7),
            self._create_token("IDENTIFIER", "next", 9, 8),
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(_parse_return_stmt.__name__, "_parse_return_stmt")

    def test_return_preserves_filename(self):
        """测试：parser_state filename 保持不变"""
        tokens = [
            self._create_token("RETURN", "return", 10, 1),
            self._create_token("SEMICOLON", ";", 10, 7),
        ]
        parser_state = self._create_parser_state(tokens, filename="my_module.py")
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(parser_state["filename"], "my_module.py")


if __name__ == "__main__":
    unittest.main()
