# === std / third-party imports ===
import unittest
from typing import Dict, Any
from unittest.mock import patch

# === target function import ===
from ._parse_while_stmt_src import _parse_while_stmt

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseWhileStmt(unittest.TestCase):
    """测试 _parse_while_stmt 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0) -> ParserState:
        """创建测试用的 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.c"
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
        """创建测试用的 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, children: list = None, value: Any = None, line: int = 1, column: int = 1) -> AST:
        """创建测试用的 AST 节点"""
        return {
            "type": node_type,
            "children": children or [],
            "value": value,
            "line": line,
            "column": column
        }

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_happy_path_basic_while(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试基本 while 语句解析 - Happy Path"""
        # 准备测试数据
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 10),
            self._create_token("LBRACE", "{", 1, 12),
            self._create_token("IDENTIFIER", "y", 1, 14),
            self._create_token("RBRACE", "}", 1, 15),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        # 设置 mock 返回值
        condition_ast = self._create_ast_node("BINARY_OP", value="x > 0", line=1, column=9)
        body_ast = self._create_ast_node("BLOCK", children=[], line=1, column=14)
        mock_parse_expression.return_value = condition_ast
        mock_parse_statement.return_value = body_ast
        
        # 执行测试
        result = _parse_while_stmt(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], body_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 9)
        
        # 验证 _expect_token 被调用 5 次 (WHILE, LPAREN, RPAREN, LBRACE, RBRACE)
        self.assertEqual(mock_expect_token.call_count, 5)
        mock_expect_token.assert_any_call(parser_state, "WHILE")
        mock_expect_token.assert_any_call(parser_state, "LPAREN")
        mock_expect_token.assert_any_call(parser_state, "RPAREN")
        mock_expect_token.assert_any_call(parser_state, "LBRACE")
        mock_expect_token.assert_any_call(parser_state, "RBRACE")
        
        # 验证子函数被调用
        mock_parse_expression.assert_called_once_with(parser_state)
        mock_parse_statement.assert_called_once_with(parser_state)

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_happy_path_nested_while(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试嵌套 while 语句解析"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 9),
            self._create_token("RPAREN", ")", 1, 10),
            self._create_token("LBRACE", "{", 1, 12),
            self._create_token("WHILE", "while", 2, 5),
            self._create_token("RBRACE", "}", 3, 1),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        condition_ast = self._create_ast_node("IDENTIFIER", value="i", line=1, column=9)
        body_ast = self._create_ast_node("WHILE_STMT", children=[], line=2, column=5)
        mock_parse_expression.return_value = condition_ast
        mock_parse_statement.return_value = body_ast
        
        result = _parse_while_stmt(parser_state)
        
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["children"][0], condition_ast)
        self.assertEqual(result["children"][1], body_ast)

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_happy_path_complex_expression(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试复杂条件表达式的 while 语句"""
        tokens = [
            self._create_token("WHILE", "while", 5, 1),
            self._create_token("LPAREN", "(", 5, 7),
            self._create_token("IDENTIFIER", "count", 5, 9),
            self._create_token("RPAREN", ")", 5, 14),
            self._create_token("LBRACE", "{", 5, 16),
            self._create_token("IDENTIFIER", "x", 6, 5),
            self._create_token("RBRACE", "}", 7, 1),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        condition_ast = self._create_ast_node("BINARY_OP", value="count < 10", line=5, column=9)
        body_ast = self._create_ast_node("BLOCK", children=[], line=6, column=5)
        mock_parse_expression.return_value = condition_ast
        mock_parse_statement.return_value = body_ast
        
        result = _parse_while_stmt(parser_state)
        
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 9)

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_error_missing_while_token(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试缺少 WHILE 关键字时的错误处理"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        # 设置 _expect_token 在期望 WHILE 时抛出 SyntaxError
        def expect_token_side_effect(state, expected_type):
            if expected_type == "WHILE":
                raise SyntaxError(f"Expected WHILE token, got {state['tokens'][state['pos']]['type']}")
        
        mock_expect_token.side_effect = expect_token_side_effect
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected WHILE", str(context.exception))

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_error_missing_lparen(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试缺少左括号时的错误处理"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 7),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        call_count = [0]
        def expect_token_side_effect(state, expected_type):
            call_count[0] += 1
            if expected_type == "LPAREN" and call_count[0] == 2:
                raise SyntaxError(f"Expected LPAREN token, got {state['tokens'][state['pos']]['type']}")
        
        mock_expect_token.side_effect = expect_token_side_effect
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected LPAREN", str(context.exception))

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_error_missing_rparen(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试缺少右括号时的错误处理"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        call_count = [0]
        def expect_token_side_effect(state, expected_type):
            call_count[0] += 1
            if expected_type == "RPAREN" and call_count[0] == 3:
                raise SyntaxError(f"Expected RPAREN token, got {state['tokens'][state['pos']]['type']}")
        
        mock_expect_token.side_effect = expect_token_side_effect
        mock_parse_expression.return_value = self._create_ast_node("IDENTIFIER", value="x")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected RPAREN", str(context.exception))

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_error_missing_lbrace(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试缺少左大括号时的错误处理"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 10),
            self._create_token("IDENTIFIER", "y", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        call_count = [0]
        def expect_token_side_effect(state, expected_type):
            call_count[0] += 1
            if expected_type == "LBRACE" and call_count[0] == 4:
                raise SyntaxError(f"Expected LBRACE token, got {state['tokens'][state['pos']]['type']}")
        
        mock_expect_token.side_effect = expect_token_side_effect
        mock_parse_expression.return_value = self._create_ast_node("IDENTIFIER", value="x")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected LBRACE", str(context.exception))

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_error_missing_rbrace(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试缺少右大括号时的错误处理"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 10),
            self._create_token("LBRACE", "{", 1, 12),
            self._create_token("IDENTIFIER", "y", 1, 14),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        call_count = [0]
        def expect_token_side_effect(state, expected_type):
            call_count[0] += 1
            if expected_type == "RBRACE" and call_count[0] == 5:
                raise SyntaxError(f"Expected RBRACE token, got {state['tokens'][state['pos']]['type']}")
        
        mock_expect_token.side_effect = expect_token_side_effect
        mock_parse_expression.return_value = self._create_ast_node("IDENTIFIER", value="x")
        mock_parse_statement.return_value = self._create_ast_node("EXPR_STMT", value="y")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected RBRACE", str(context.exception))

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_expression_parse_error_propagation(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试表达式解析错误传播"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 10),
            self._create_token("LBRACE", "{", 1, 12),
            self._create_token("IDENTIFIER", "y", 1, 14),
            self._create_token("RBRACE", "}", 1, 15),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        mock_parse_expression.side_effect = SyntaxError("Invalid expression syntax")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Invalid expression", str(context.exception))
        mock_parse_statement.assert_not_called()

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_statement_parse_error_propagation(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试语句解析错误传播"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("RPAREN", ")", 1, 10),
            self._create_token("LBRACE", "{", 1, 12),
            self._create_token("IDENTIFIER", "y", 1, 14),
            self._create_token("RBRACE", "}", 1, 15),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        mock_parse_expression.return_value = self._create_ast_node("IDENTIFIER", value="x")
        mock_parse_statement.side_effect = SyntaxError("Invalid statement syntax")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Invalid statement", str(context.exception))

    @patch("_parse_while_stmt_package._parse_while_stmt_src._expect_token")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_expression")
    @patch("_parse_while_stmt_package._parse_while_stmt_src._parse_statement")
    def test_ast_node_line_column_preservation(self, mock_parse_statement, mock_parse_expression, mock_expect_token):
        """测试 AST 节点行号和列号保留"""
        tokens = [
            self._create_token("WHILE", "while", 10, 5),
            self._create_token("LPAREN", "(", 10, 11),
            self._create_token("IDENTIFIER", "x", 10, 13),
            self._create_token("RPAREN", ")", 10, 14),
            self._create_token("LBRACE", "{", 10, 16),
            self._create_token("IDENTIFIER", "y", 11, 5),
            self._create_token("RBRACE", "}", 12, 1),
        ]
        parser_state = self._create_parser_state(tokens, 0)
        
        condition_ast = self._create_ast_node("BINARY_OP", value="x > 0", line=10, column=13)
        body_ast = self._create_ast_node("BLOCK", children=[], line=11, column=5)
        mock_parse_expression.return_value = condition_ast
        mock_parse_statement.return_value = body_ast
        
        result = _parse_while_stmt(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 13)


if __name__ == "__main__":
    unittest.main()
