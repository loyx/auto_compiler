# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports for tested module ===
from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """测试 _parse_primary_expr 函数的单元测试类"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    # ==================== Happy Path Tests ====================

    def test_parse_literal_success(self):
        """测试成功解析字面量"""
        tokens = [self._create_token("LITERAL", "42", 1, 5)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_multiple_tokens(self):
        """测试解析字面量后 pos 正确更新"""
        tokens = [
            self._create_token("LITERAL", "100", 2, 10),
            self._create_token("IDENTIFIER", "x", 2, 15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "100")
        self.assertEqual(parser_state["pos"], 1)

    # ==================== Identifier Tests (with mock) ====================

    @patch("_parse_primary_expr_src._handle_identifier")
    def test_parse_identifier_delegates_to_handler(self, mock_handle_identifier):
        """测试标识符解析委派给 _handle_identifier"""
        tokens = [self._create_token("IDENTIFIER", "myVar", 3, 8)]
        parser_state = self._create_parser_state(tokens, pos=0)

        expected_ast = {"type": "IDENTIFIER", "value": "myVar", "line": 3, "column": 8}
        mock_handle_identifier.return_value = expected_ast

        result = _parse_primary_expr(parser_state)

        mock_handle_identifier.assert_called_once_with(parser_state, tokens[0])
        self.assertEqual(result, expected_ast)

    @patch("_parse_primary_expr_src._handle_identifier")
    def test_parse_identifier_call_node(self, mock_handle_identifier):
        """测试函数调用节点的解析"""
        tokens = [self._create_token("IDENTIFIER", "func", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)

        call_node = {
            "type": "CALL",
            "function": {"type": "IDENTIFIER", "value": "func"},
            "arguments": [],
            "line": 1,
            "column": 1
        }
        mock_handle_identifier.return_value = call_node

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["function"]["value"], "func")

    # ==================== Paren Expression Tests (with mock) ====================

    @patch("_parse_primary_expr_package._parse_primary_expr_src._handle_paren_expr")
    def test_parse_paren_expr_delegates_to_handler(self, mock_handle_paren_expr):
        """测试括号表达式解析委派给 _handle_paren_expr"""
        tokens = [self._create_token("LPAREN", "(", 4, 12)]
        parser_state = self._create_parser_state(tokens, pos=0)

        expected_ast = {"type": "LITERAL", "value": "5", "line": 4, "column": 13}
        mock_handle_paren_expr.return_value = expected_ast

        result = _parse_primary_expr(parser_state)

        mock_handle_paren_expr.assert_called_once_with(parser_state, tokens[0])
        self.assertEqual(result, expected_ast)

    @patch("_parse_primary_expr_package._parse_primary_expr_src._handle_paren_expr")
    def test_parse_nested_paren_expr(self, mock_handle_paren_expr):
        """测试嵌套括号表达式"""
        tokens = [self._create_token("LPAREN", "(", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)

        nested_ast = {
            "type": "BINARY",
            "left": {"type": "LITERAL", "value": "1"},
            "right": {"type": "LITERAL", "value": "2"},
            "line": 1,
            "column": 2
        }
        mock_handle_paren_expr.return_value = nested_ast

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "BINARY")

    # ==================== Error Handling Tests ====================

    @patch("_parse_primary_expr_package._parse_primary_expr_src._build_error_node")
    def test_parse_empty_tokens_returns_error(self, mock_build_error_node):
        """测试空 token 列表返回错误节点"""
        parser_state = self._create_parser_state([], pos=0)

        error_node = {"type": "ERROR", "value": "unexpected end of input", "line": 0, "column": 0}
        mock_build_error_node.return_value = error_node

        result = _parse_primary_expr(parser_state)

        mock_build_error_node.assert_called_once()
        self.assertEqual(result["type"], "ERROR")

    @patch("_parse_primary_expr_package._parse_primary_expr_src._build_error_node")
    def test_parse_pos_beyond_tokens_returns_error(self, mock_build_error_node):
        """测试 pos 超出 token 列表范围返回错误"""
        tokens = [self._create_token("LITERAL", "1", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=5)

        error_node = {"type": "ERROR", "value": "unexpected end of input", "line": 1, "column": 1}
        mock_build_error_node.return_value = error_node

        result = _parse_primary_expr(parser_state)

        mock_build_error_node.assert_called_once()
        self.assertEqual(result["type"], "ERROR")

    @patch("_parse_primary_expr_package._parse_primary_expr_src._build_error_node")
    def test_parse_unexpected_token_type_returns_error(self, mock_build_error_node):
        """测试未知 token 类型返回错误"""
        tokens = [self._create_token("OPERATOR", "+", 5, 20)]
        parser_state = self._create_parser_state(tokens, pos=0)

        error_node = {
            "type": "ERROR",
            "value": "unexpected token: OPERATOR at line 5, column 20",
            "line": 5,
            "column": 20
        }
        mock_build_error_node.return_value = error_node

        result = _parse_primary_expr(parser_state)

        mock_build_error_node.assert_called_once()
        call_args = mock_build_error_node.call_args
        self.assertIn("unexpected token: OPERATOR", call_args[0][1])
        self.assertEqual(result["type"], "ERROR")

    @patch("_parse_primary_expr_package._parse_primary_expr_src._build_error_node")
    def test_parse_comma_token_returns_error(self, mock_build_error_node):
        """测试 COMMA token 返回错误"""
        tokens = [self._create_token("COMMA", ",", 2, 15)]
        parser_state = self._create_parser_state(tokens, pos=0)

        error_node = {
            "type": "ERROR",
            "value": "unexpected token: COMMA at line 2, column 15",
            "line": 2,
            "column": 15
        }
        mock_build_error_node.return_value = error_node

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "解析失败")

    @patch("_parse_primary_expr_package._parse_primary_expr_src._build_error_node")
    def test_parse_rparen_token_returns_error(self, mock_build_error_node):
        """测试 RPAREN token 返回错误（孤立的右括号）"""
        tokens = [self._create_token("RPAREN", ")", 3, 8)]
        parser_state = self._create_parser_state(tokens, pos=0)

        error_node = {
            "type": "ERROR",
            "value": "unexpected token: RPAREN at line 3, column 8",
            "line": 3,
            "column": 8
        }
        mock_build_error_node.return_value = error_node

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")

    # ==================== Edge Cases ====================

    def test_parse_literal_string_value(self):
        """测试字符串字面量解析"""
        tokens = [self._create_token("LITERAL", '"hello world"', 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello world"')
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_boolean_value(self):
        """测试布尔字面量解析"""
        tokens = [self._create_token("LITERAL", "true", 2, 5)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "true")

    def test_parse_literal_at_end_of_multiple_tokens(self):
        """测试在多个 token 末尾解析字面量"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("LITERAL", "999", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=2)

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "999")
        self.assertEqual(parser_state["pos"], 3)

    @patch("_parse_primary_expr_package._parse_primary_expr_src._handle_identifier")
    def test_parse_identifier_preserves_error_state(self, mock_handle_identifier):
        """测试标识符解析时保持 error 状态"""
        tokens = [self._create_token("IDENTIFIER", "var", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)
        parser_state["error"] = "previous error"

        mock_handle_identifier.return_value = {"type": "IDENTIFIER", "value": "var"}

        result = _parse_primary_expr(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")


if __name__ == "__main__":
    unittest.main()
