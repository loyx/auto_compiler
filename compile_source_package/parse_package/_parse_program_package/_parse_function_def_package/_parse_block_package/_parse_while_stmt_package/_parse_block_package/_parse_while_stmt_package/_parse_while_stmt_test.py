# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === relative imports ===
from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt(unittest.TestCase):
    """测试 _parse_while_stmt 函数解析 while 语句的行为。"""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典。"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点字典。"""
        return {
            "type": node_type,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典。"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_happy_path_valid_while_statement(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：解析有效的 while 语句（happy path）。"""
        # Arrange
        while_token = self._create_token("WHILE", "while", line=5, column=10)
        mock_peek_token.return_value = while_token
        
        # 模拟 consume_token 返回更新后的 parser_state
        mock_consume_token.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
        
        condition_node = self._create_ast_node("BINARY_OP", line=5, column=17)
        mock_parse_expression.return_value = condition_node
        
        body_node = self._create_ast_node("BLOCK", line=6, column=5)
        mock_parse_block.return_value = body_node
        
        parser_state = self._create_parser_state([while_token], pos=0)
        
        # Act
        result = _parse_while_stmt(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], condition_node)
        self.assertEqual(result["children"][1], body_node)
        
        # 验证依赖调用
        mock_peek_token.assert_called_once_with(parser_state)
        self.assertEqual(mock_consume_token.call_count, 3)  # WHILE, LPAREN, RPAREN
        mock_parse_expression.assert_called_once()
        mock_parse_block.assert_called_once()

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_complex_condition_and_body(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：解析包含复杂条件和多语句体的 while 语句。"""
        # Arrange
        while_token = self._create_token("WHILE", "while", line=10, column=1)
        mock_peek_token.return_value = while_token
        mock_consume_token.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
        
        # 复杂条件：x > 0 and y < 10
        condition_node = self._create_ast_node("BINARY_OP", 
            children=[
                self._create_ast_node("BINARY_OP"),
                self._create_ast_node("BINARY_OP")
            ],
            line=10, column=8
        )
        mock_parse_expression.return_value = condition_node
        
        # 多语句块
        body_node = self._create_ast_node("BLOCK",
            children=[
                self._create_ast_node("ASSIGN_STMT"),
                self._create_ast_node("IF_STMT"),
                self._create_ast_node("BREAK_STMT")
            ],
            line=11, column=5
        )
        mock_parse_block.return_value = body_node
        
        parser_state = self._create_parser_state([while_token], pos=0)
        
        # Act
        result = _parse_while_stmt(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "BINARY_OP")
        self.assertEqual(result["children"][1]["type"], "BLOCK")
        self.assertEqual(len(result["children"][1]["children"]), 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_consume_token_raises_syntax_error(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：当 consume_token 遇到不匹配的 token 时抛出 SyntaxError。"""
        # Arrange
        while_token = self._create_token("WHILE", "while", line=1, column=1)
        mock_peek_token.return_value = while_token
        mock_consume_token.side_effect = SyntaxError("Expected LPAREN but found IDENTIFIER")
        
        parser_state = self._create_parser_state([while_token], pos=0)
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected LPAREN", str(context.exception))

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_parse_expression_raises_syntax_error(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：当 parse_expression 解析失败时抛出 SyntaxError。"""
        # Arrange
        while_token = self._create_token("WHILE", "while", line=1, column=1)
        mock_peek_token.return_value = while_token
        mock_consume_token.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
        mock_parse_expression.side_effect = SyntaxError("Invalid expression syntax")
        
        parser_state = self._create_parser_state([while_token], pos=0)
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Invalid expression", str(context.exception))

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_parse_block_raises_syntax_error(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：当 parse_block 解析失败时抛出 SyntaxError。"""
        # Arrange
        while_token = self._create_token("WHILE", "while", line=1, column=1)
        mock_peek_token.return_value = while_token
        mock_consume_token.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
        mock_parse_expression.return_value = self._create_ast_node("IDENTIFIER")
        mock_parse_block.side_effect = SyntaxError("Expected block start")
        
        parser_state = self._create_parser_state([while_token], pos=0)
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected block", str(context.exception))

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_peek_token_returns_none(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：当 peek_token 返回 None 时的边界情况。"""
        # Arrange
        mock_peek_token.return_value = None
        mock_consume_token.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
        mock_parse_expression.return_value = self._create_ast_node("IDENTIFIER")
        mock_parse_block.return_value = self._create_ast_node("BLOCK")
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Act
        result = _parse_while_stmt(parser_state)
        
        # Assert - 应该使用默认值 0
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_nested_while_statements(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：解析嵌套的 while 语句。"""
        # Arrange
        outer_while_token = self._create_token("WHILE", "while", line=1, column=1)
        mock_peek_token.return_value = outer_while_token
        mock_consume_token.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
        
        # 外层条件
        outer_condition = self._create_ast_node("IDENTIFIER", value="flag")
        mock_parse_expression.return_value = outer_condition
        
        # 内层 while 语句作为 body 的一部分
        inner_while_node = self._create_ast_node("WHILE_STMT",
            children=[
                self._create_ast_node("IDENTIFIER"),
                self._create_ast_node("BLOCK")
            ]
        )
        body_node = self._create_ast_node("BLOCK", children=[inner_while_node])
        mock_parse_block.return_value = body_node
        
        parser_state = self._create_parser_state([outer_while_token], pos=0)
        
        # Act
        result = _parse_while_stmt(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(len(result["children"]), 2)
        # 验证 body 中包含嵌套的 while
        body = result["children"][1]
        self.assertEqual(body["type"], "BLOCK")
        self.assertEqual(body["children"][0]["type"], "WHILE_STMT")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._peek_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._consume_token')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block')
    def test_consume_token_call_sequence(self, mock_parse_block, mock_parse_expression, mock_consume_token, mock_peek_token):
        """测试：验证 consume_token 的调用顺序（WHILE, LPAREN, RPAREN）。"""
        # Arrange
        while_token = self._create_token("WHILE", "while", line=1, column=1)
        mock_peek_token.return_value = while_token
        mock_consume_token.side_effect = lambda state, expected: {**state, "pos": state["pos"] + 1}
        mock_parse_expression.return_value = self._create_ast_node("IDENTIFIER")
        mock_parse_block.return_value = self._create_ast_node("BLOCK")
        
        parser_state = self._create_parser_state([while_token], pos=0)
        
        # Act
        _parse_while_stmt(parser_state)
        
        # Assert - 验证调用顺序
        calls = mock_consume_token.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0][0][1], "WHILE")   # 第一次消费 WHILE
        self.assertEqual(calls[1][0][1], "LPAREN")  # 第二次消费 LPAREN
        self.assertEqual(calls[2][0][1], "RPAREN")  # 第三次消费 RPAREN


if __name__ == "__main__":
    unittest.main()
