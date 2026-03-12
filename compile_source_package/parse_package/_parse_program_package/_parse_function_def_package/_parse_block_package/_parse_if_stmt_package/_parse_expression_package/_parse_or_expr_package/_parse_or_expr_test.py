# === std / third-party imports ===
import sys
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === Mock the entire dependency chain before any imports ===
# This prevents the deep import chain from failing
def create_mock_module(name):
    mock = MagicMock()
    sys.modules[name] = mock
    return mock

# Mock all dependencies in the chain with relative paths
# _parse_or_expr_src depends on _parse_and_expr
mock_and_expr_pkg = create_mock_module('._parse_and_expr_package')
mock_and_expr_src = create_mock_module('._parse_and_expr_package._parse_and_expr_src')
mock_and_expr_func = MagicMock()
mock_and_expr_src._parse_and_expr = mock_and_expr_func

# _parse_and_expr_src depends on _parse_comparison_expr
mock_comparison_pkg = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package')
mock_comparison_src = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src')
mock_comparison_src._parse_comparison_expr = MagicMock()

# _parse_comparison_expr_src depends on _parse_additive_expr
mock_additive_pkg = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package')
mock_additive_src = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src')
mock_additive_src._parse_additive_expr = MagicMock()

# _parse_additive_expr_src depends on _parse_multiplicative_expr
mock_multiplicative_pkg = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package')
mock_multiplicative_src = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src')
mock_multiplicative_src._parse_multiplicative_expr = MagicMock()

# _parse_multiplicative_expr_src depends on _parse_unary_expr
mock_unary_pkg = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package')
mock_unary_src = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src')
mock_unary_src._parse_unary_expr = MagicMock()

# _parse_unary_expr_src depends on _parse_primary_expr
mock_primary_pkg = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package')
mock_primary_src = create_mock_module('._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src')
mock_primary_src._parse_primary_expr = MagicMock()

# === sub function imports ===
from ._parse_or_expr_src import _parse_or_expr


class TestParseOrExpr(unittest.TestCase):
    """测试 _parse_or_expr 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, **kwargs) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点"""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    def test_no_or_operator(self):
        """测试：没有 || 操作符，直接返回左操作数"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_and_expr_src._parse_and_expr.return_value = left_ast
        
        tokens = [self._create_token("IDENTIFIER", "a")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result, left_ast)
        mock_and_expr_src._parse_and_expr.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_single_or_operator(self):
        """测试：单个 || 操作符 (a || b)"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_ast = self._create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        mock_and_expr_src._parse_and_expr.side_effect = [left_ast, right_ast]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "||", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "||")
        self.assertEqual(result["left"], left_ast)
        self.assertEqual(result["right"], right_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)  # pos 应前进到 tokens 末尾
        self.assertEqual(mock_and_expr_src._parse_and_expr.call_count, 2)

    def test_multiple_or_operators_left_associative(self):
        """测试：多个 || 操作符，左结合 (a || b || c)"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        middle_ast = self._create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        right_ast = self._create_ast_node("IDENTIFIER", value="c", line=1, column=9)
        mock_and_expr_src._parse_and_expr.side_effect = [left_ast, middle_ast, right_ast]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "||", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("OPERATOR", "||", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert: 应该是 ((a || b) || c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "||")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)  # 第二个 || 的位置
        
        # 右侧应该是 c
        self.assertEqual(result["right"], right_ast)
        
        # 左侧应该是 (a || b)
        left_part = result["left"]
        self.assertEqual(left_part["type"], "BINARY_OP")
        self.assertEqual(left_part["operator"], "||")
        self.assertEqual(left_part["left"], left_ast)
        self.assertEqual(left_part["right"], middle_ast)
        self.assertEqual(left_part["line"], 1)
        self.assertEqual(left_part["column"], 3)  # 第一个 || 的位置
        
        self.assertEqual(parser_state["pos"], 5)  # pos 应前进到 tokens 末尾
        self.assertEqual(mock_and_expr_src._parse_and_expr.call_count, 3)

    def test_empty_tokens(self):
        """测试：空 tokens 列表"""
        # Arrange
        mock_and_expr_src._parse_and_expr.side_effect = IndexError("pos out of range")
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Act & Assert
        with self.assertRaises(IndexError):
            _parse_or_expr(parser_state)

    def test_position_at_end_after_left_operand(self):
        """测试：解析完左操作数后 pos 已在末尾"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_and_expr_src._parse_and_expr.return_value = left_ast
        
        tokens = [self._create_token("IDENTIFIER", "a", line=1, column=1)]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # 模拟 _parse_and_expr 消费了 token
        def consume_token(state):
            state["pos"] = 1
            return left_ast
        mock_and_expr_src._parse_and_expr.side_effect = consume_token
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result, left_ast)
        self.assertEqual(parser_state["pos"], 1)

    @patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr")
    def test_non_or_operator(self, mock_parse_and_expr: MagicMock):
        """测试：遇到非 || 操作符（如 &&）"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_ast = self._create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        mock_parse_and_expr.side_effect = [left_ast, right_ast]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "&&", line=1, column=3),  # 不是 ||
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result, left_ast)  # 不应消费 && 和 b
        mock_parse_and_expr.assert_called_once()
        self.assertEqual(parser_state["pos"], 0)

    @patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr")
    def test_token_without_type_field(self, mock_parse_and_expr: MagicMock):
        """测试：token 缺少 type 字段"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_parse_and_expr.return_value = left_ast
        
        tokens = [{"value": "a"}]  # 缺少 type 字段
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result, left_ast)
        self.assertEqual(parser_state["pos"], 0)

    @patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr")
    def test_token_without_value_field(self, mock_parse_and_expr: MagicMock):
        """测试：token 缺少 value 字段"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_parse_and_expr.return_value = left_ast
        
        tokens = [{"type": "OPERATOR"}]  # 缺少 value 字段
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result, left_ast)
        self.assertEqual(parser_state["pos"], 0)

    @patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr")
    def test_or_operator_without_line_column(self, mock_parse_and_expr: MagicMock):
        """测试：|| 操作符 token 缺少 line/column 字段"""
        # Arrange
        left_ast = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_ast = self._create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        mock_parse_and_expr.side_effect = [left_ast, right_ast]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            {"type": "OPERATOR", "value": "||"},  # 缺少 line/column
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "||")
        self.assertEqual(result["line"], 0)  # 默认值
        self.assertEqual(result["column"], 0)  # 默认值
        self.assertEqual(parser_state["pos"], 3)

    @patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr")
    def test_complex_expression_with_nested_ast(self, mock_parse_and_expr: MagicMock):
        """测试：复杂表达式，_parse_and_expr 返回嵌套 AST"""
        # Arrange
        # 模拟 a && b || c
        and_expr_ast = self._create_ast_node(
            "BINARY_OP",
            operator="&&",
            left=self._create_ast_node("IDENTIFIER", value="a"),
            right=self._create_ast_node("IDENTIFIER", value="b"),
            line=1,
            column=3
        )
        c_ast = self._create_ast_node("IDENTIFIER", value="c", line=1, column=9)
        mock_parse_and_expr.side_effect = [and_expr_ast, c_ast]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "&&", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("OPERATOR", "||", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act
        result = _parse_or_expr(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "||")
        # 左侧应该是 (a && b)
        self.assertEqual(result["left"], and_expr_ast)
        # 右侧应该是 c
        self.assertEqual(result["right"], c_ast)


if __name__ == "__main__":
    unittest.main()
