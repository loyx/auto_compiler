# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === UUT import (relative) ===
from ._parse_while_stmt_src import _parse_while_stmt

# === Type aliases ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]
AST = Dict[str, Any]


class TestParseWhileStmt(unittest.TestCase):
    """单元测试：_parse_while_stmt 函数"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block")
    def test_happy_path_valid_while_stmt(self, mock_parse_block, mock_parse_expression):
        """测试：合法的 while 语句解析"""
        # 准备 tokens: while ( condition ) block
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 11),
            self._create_token("LBRACE", "{", 1, 13),
            self._create_token("RBRACE", "}", 1, 15),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 设置 mock 返回值
        condition_ast = {"type": "CONDITION", "value": "x > 0", "line": 1, "column": 9}
        body_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 13}
        mock_parse_expression.return_value = condition_ast
        mock_parse_block.return_value = body_ast
        
        # 执行
        result = _parse_while_stmt(parser_state)
        
        # 验证
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], body_ast)
        
        # 验证 pos 更新到语句结束
        self.assertEqual(parser_state["pos"], 6)
        
        # 验证依赖调用
        mock_parse_expression.assert_called_once()
        mock_parse_block.assert_called_once()

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block")
    def test_happy_path_with_complex_condition(self, mock_parse_block, mock_parse_expression):
        """测试：带复杂条件的 while 语句"""
        tokens = [
            self._create_token("WHILE", "while", 2, 5),
            self._create_token("LPAREN", "(", 2, 11),
            self._create_token("IDENTIFIER", "i", 2, 13),
            self._create_token("LESS", "<", 2, 15),
            self._create_token("NUMBER", "10", 2, 17),
            self._create_token("RPAREN", ")", 2, 20),
            self._create_token("LBRACE", "{", 3, 1),
            self._create_token("RBRACE", "}", 4, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="loop.py")
        
        condition_ast = {"type": "BINARY_OP", "children": [{"type": "IDENTIFIER"}, {"type": "NUMBER"}]}
        body_ast = {"type": "BLOCK", "children": []}
        mock_parse_expression.return_value = condition_ast
        mock_parse_block.return_value = body_ast
        
        result = _parse_while_stmt(parser_state)
        
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 8)

    def test_error_unexpected_eof_before_while(self):
        """测试：tokens 为空，期望 while 但遇到 EOF"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0, filename="empty.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("意外的文件结束", str(context.exception))
        self.assertIn("期望 'while'", str(context.exception))

    def test_error_wrong_token_instead_of_while(self):
        """测试：当前 token 不是 WHILE"""
        tokens = [
            self._create_token("IF", "if", 5, 10),
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="wrong.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("期望 'while'", str(context.exception))
        self.assertIn("得到 'if'", str(context.exception))
        self.assertIn("5:10", str(context.exception))

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_unexpected_eof_after_while(self, mock_parse_expression):
        """测试：WHILE 之后遇到 EOF，期望 LPAREN"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("意外的文件结束", str(context.exception))
        self.assertIn("期望 '('", str(context.exception))

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_wrong_token_instead_of_lparen(self, mock_parse_expression):
        """测试：WHILE 之后不是 LPAREN"""
        tokens = [
            self._create_token("WHILE", "while", 3, 5),
            self._create_token("IDENTIFIER", "x", 3, 11),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("期望 '('", str(context.exception))
        self.assertIn("得到 'x'", str(context.exception))
        self.assertIn("3:11", str(context.exception))

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_unexpected_eof_after_condition(self, mock_parse_expression):
        """测试：条件表达式之后遇到 EOF，期望 RPAREN"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # mock _parse_expression 消耗一个 token
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 2}) or {"type": "EXPR"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("意外的文件结束", str(context.exception))
        self.assertIn("期望 ')'", str(context.exception))

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_wrong_token_instead_of_rparen(self, mock_parse_expression):
        """测试：条件表达式之后不是 RPAREN"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("COMMA", ",", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # mock _parse_expression 消耗一个 token
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 2}) or {"type": "EXPR"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("期望 ')'", str(context.exception))
        self.assertIn("得到 ','", str(context.exception))
        self.assertIn("1:11", str(context.exception))

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_unexpected_eof_before_block(self, mock_parse_expression):
        """测试：RPAREN 之后遇到 EOF，期望语句块"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # mock _parse_expression 消耗一个 token
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 2}) or {"type": "EXPR"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        # _parse_block 应该被调用并抛出错误
        mock_parse_expression.assert_called_once()

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block")
    def test_pos_updated_correctly(self, mock_parse_block, mock_parse_expression):
        """测试：pos 正确更新到语句结束位置"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 11),
            self._create_token("LBRACE", "{", 1, 13),
            self._create_token("IDENTIFIER", "y", 1, 15),
            self._create_token("RBRACE", "}", 1, 17),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # mock _parse_expression 消耗 1 个 token (pos: 2 -> 3)
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 3}) or {"type": "EXPR"}
        # mock _parse_block 消耗 3 个 token (pos: 4 -> 7)
        mock_parse_block.side_effect = lambda state: state.update({"pos": 7}) or {"type": "BLOCK"}
        
        result = _parse_while_stmt(parser_state)
        
        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(result["type"], "WHILE_STMT")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression")
    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_while_stmt_package._parse_statement_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block")
    def test_default_filename_when_not_provided(self, mock_parse_block, mock_parse_expression):
        """测试：当 filename 未提供时使用默认值"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 11),
            self._create_token("LBRACE", "{", 1, 13),
            self._create_token("RBRACE", "}", 1, 15),
        ]
        # 不提供 filename
        parser_state = {
            "tokens": tokens,
            "pos": 0,
        }
        
        mock_parse_expression.return_value = {"type": "EXPR"}
        mock_parse_block.return_value = {"type": "BLOCK"}
        
        result = _parse_while_stmt(parser_state)
        
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(parser_state["pos"], 6)


if __name__ == "__main__":
    unittest.main()
