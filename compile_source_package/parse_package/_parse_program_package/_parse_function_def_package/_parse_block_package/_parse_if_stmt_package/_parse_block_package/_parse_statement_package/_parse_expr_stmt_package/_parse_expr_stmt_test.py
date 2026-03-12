"""
单元测试文件：_parse_expr_stmt 函数测试
测试表达式语句解析功能（expr;）
"""
import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测函数
from ._parse_expr_stmt_src import _parse_expr_stmt


class TestParseExprStmt(unittest.TestCase):
    """_parse_expr_stmt 函数测试类"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_happy_path_assignment_expression(self):
        """测试：赋值表达式语句 x = 5;"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("ASSIGN", "=", 1, 3),
            self._create_token("NUMBER", "5", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression 返回赋值表达式 AST
        mock_expr_ast = {
            "type": "ASSIGN",
            "children": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "NUMBER", "value": "5"}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            # _parse_expression 会更新 pos，模拟它消费了 3 个 token
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 3}) or mock_expr_ast
            
            result = _parse_expr_stmt(parser_state)
            
            # 验证返回的 AST 结构
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_expr_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # 验证 parser_state["pos"] 被更新（消费了分号）
            self.assertEqual(parser_state["pos"], 4)
            
            # 验证 _parse_expression 被调用
            mock_parse_expr.assert_called_once()

    def test_happy_path_function_call_expression(self):
        """测试：函数调用表达式语句 func();"""
        tokens = [
            self._create_token("IDENTIFIER", "func", 2, 5),
            self._create_token("LPAREN", "(", 2, 9),
            self._create_token("RPAREN", ")", 2, 10),
            self._create_token("SEMICOLON", ";", 2, 11)
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="main.py")
        
        mock_expr_ast = {
            "type": "CALL",
            "children": [{"type": "IDENTIFIER", "value": "func"}],
            "line": 2,
            "column": 5
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 3}) or mock_expr_ast
            
            result = _parse_expr_stmt(parser_state)
            
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
            self.assertEqual(parser_state["pos"], 4)

    def test_error_missing_semicolon_eof(self):
        """测试：错误情况 - 表达式后缺少分号（到达文件末尾）"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("ASSIGN", "=", 1, 3),
            self._create_token("NUMBER", "5", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {"type": "ASSIGN", "children": [], "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 3}) or mock_expr_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_expr_stmt(parser_state)
            
            # 验证错误消息包含预期信息
            self.assertIn("expected ';' after expression", str(context.exception))
            self.assertIn("test.py", str(context.exception))

    def test_error_wrong_token_after_expression(self):
        """测试：错误情况 - 表达式后是错误 token 类型（不是分号）"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("ASSIGN", "=", 1, 3),
            self._create_token("NUMBER", "5", 1, 5),
            self._create_token("COMMA", ",", 1, 6)  # 错误的 token
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {"type": "ASSIGN", "children": [], "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 3}) or mock_expr_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_expr_stmt(parser_state)
            
            self.assertIn("expected ';' after expression", str(context.exception))
            self.assertIn(",", str(context.exception))

    def test_empty_tokens_list(self):
        """测试：边界情况 - tokens 列表为空"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {"type": "EMPTY", "children": [], "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_expr_stmt(parser_state)
            
            self.assertIn("expected ';' after expression", str(context.exception))

    def test_semicolon_at_different_position(self):
        """测试：分号在不同位置（pos 不为 0）"""
        tokens = [
            self._create_token("KEYWORD", "let", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
            self._create_token("ASSIGN", "=", 1, 7),
            self._create_token("NUMBER", "10", 1, 9),
            self._create_token("SEMICOLON", ";", 1, 11)
        ]
        # pos 指向表达式起始（跳过 let）
        parser_state = self._create_parser_state(tokens, pos=1)
        
        mock_expr_ast = {"type": "ASSIGN", "children": [], "line": 1, "column": 5}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 4}) or mock_expr_ast
            
            result = _parse_expr_stmt(parser_state)
            
            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            # pos 应该更新到 5（消费了分号）
            self.assertEqual(parser_state["pos"], 5)

    def test_preserves_filename_in_error(self):
        """测试：错误消息中保留正确的文件名"""
        tokens = [
            self._create_token("IDENTIFIER", "y", 3, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="module.py")
        
        mock_expr_ast = {"type": "IDENTIFIER", "children": [], "line": 3, "column": 10}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_expr_stmt(parser_state)
            
            self.assertIn("module.py", str(context.exception))
            self.assertIn("3", str(context.exception))  # line number

    def test_multiple_expressions_sequential(self):
        """测试：多个表达式语句顺序解析（验证 pos 正确更新）"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("ASSIGN", "=", 1, 3),
            self._create_token("NUMBER", "1", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("IDENTIFIER", "b", 1, 8),
            self._create_token("ASSIGN", "=", 1, 10),
            self._create_token("NUMBER", "2", 1, 12),
            self._create_token("SEMICOLON", ";", 1, 13)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_expr_ast1 = {"type": "ASSIGN", "children": [], "line": 1, "column": 1}
        mock_expr_ast2 = {"type": "ASSIGN", "children": [], "line": 1, "column": 8}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            # 第一次调用解析 a = 1，pos 更新到 3
            mock_parse_expr.side_effect = [
                lambda state: state.update({"pos": 3}) or mock_expr_ast1,
                lambda state: state.update({"pos": 7}) or mock_expr_ast2
            ]
            
            # 解析第一个表达式语句
            result1 = _parse_expr_stmt(parser_state)
            self.assertEqual(parser_state["pos"], 4)
            self.assertEqual(result1["column"], 1)
            
            # 解析第二个表达式语句
            result2 = _parse_expr_stmt(parser_state)
            self.assertEqual(parser_state["pos"], 8)
            self.assertEqual(result2["column"], 8)


if __name__ == "__main__":
    unittest.main()
