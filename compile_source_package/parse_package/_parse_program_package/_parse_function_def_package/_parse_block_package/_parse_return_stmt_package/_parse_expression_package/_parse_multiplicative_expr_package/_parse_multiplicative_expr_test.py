# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative import for UUT ===
from _parse_multiplicative_expr_src import _parse_multiplicative_expr


class TestParseMultiplicativeExpr(unittest.TestCase):
    """测试 _parse_multiplicative_expr 函数的单元测试类。"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助方法：创建 parser_state 字典。"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助方法：创建 token 字典。"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助方法：创建 AST 节点字典。"""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_single_unary_expr_no_operator(self, mock_unary):
        """测试：单个一元表达式，无乘除运算符。"""
        # Arrange
        token = self._create_token("IDENTIFIER", "x", 1, 1)
        parser_state = self._create_parser_state([token], pos=0)
        unary_result = self._create_ast_node("IDENTIFIER", "x", [], 1, 1)
        mock_unary.return_value = unary_result
        mock_unary.side_effect = None

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert
        self.assertEqual(result, unary_result)
        mock_unary.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变，因为没有消费 token

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_multiplication_expression(self, mock_unary):
        """测试：乘法表达式 (a * b)。"""
        # Arrange
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_star = self._create_token("STAR", "*", 1, 3)
        token_b = self._create_token("IDENTIFIER", "b", 1, 5)
        parser_state = self._create_parser_state([token_a, token_star, token_b], pos=0)
        
        unary_a = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        unary_b = self._create_ast_node("IDENTIFIER", "b", [], 1, 5)
        
        mock_unary.side_effect = [unary_a, unary_b]

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], unary_a)
        self.assertEqual(result["children"][1], unary_b)
        self.assertEqual(parser_state["pos"], 3)  # 消费了 3 个 token

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_division_expression(self, mock_unary):
        """测试：除法表达式 (a / b)。"""
        # Arrange
        token_a = self._create_token("IDENTIFIER", "a", 2, 1)
        token_slash = self._create_token("SLASH", "/", 2, 3)
        token_b = self._create_token("IDENTIFIER", "b", 2, 5)
        parser_state = self._create_parser_state([token_a, token_slash, token_b], pos=0)
        
        unary_a = self._create_ast_node("IDENTIFIER", "a", [], 2, 1)
        unary_b = self._create_ast_node("IDENTIFIER", "b", [], 2, 5)
        
        mock_unary.side_effect = [unary_a, unary_b]

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], unary_a)
        self.assertEqual(result["children"][1], unary_b)
        self.assertEqual(parser_state["pos"], 3)

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_chained_left_associative(self, mock_unary):
        """测试：链式乘除表达式，验证左结合性 (a * b / c)。"""
        # Arrange
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_star = self._create_token("STAR", "*", 1, 3)
        token_b = self._create_token("IDENTIFIER", "b", 1, 5)
        token_slash = self._create_token("SLASH", "/", 1, 7)
        token_c = self._create_token("IDENTIFIER", "c", 1, 9)
        parser_state = self._create_parser_state([token_a, token_star, token_b, token_slash, token_c], pos=0)
        
        unary_a = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        unary_b = self._create_ast_node("IDENTIFIER", "b", [], 1, 5)
        unary_c = self._create_ast_node("IDENTIFIER", "c", [], 1, 9)
        
        mock_unary.side_effect = [unary_a, unary_b, unary_c]

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert: 左结合性意味着 (a * b) / c，即根节点是 /，左子是 *，右子是 c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        self.assertEqual(len(result["children"]), 2)
        
        # 左子节点应该是 (a * b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "*")
        self.assertEqual(left_child["children"][0], unary_a)
        self.assertEqual(left_child["children"][1], unary_b)
        
        # 右子节点应该是 c
        right_child = result["children"][1]
        self.assertEqual(right_child, unary_c)
        
        self.assertEqual(parser_state["pos"], 5)

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_empty_tokens(self, mock_unary):
        """测试：空 token 列表。"""
        # Arrange
        parser_state = self._create_parser_state([], pos=0)
        mock_unary.side_effect = IndexError("No tokens")

        # Act & Assert
        with self.assertRaises(IndexError):
            _parse_multiplicative_expr(parser_state)

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_operator_at_end_missing_operand(self, mock_unary):
        """测试：运算符在末尾，缺少右操作数。"""
        # Arrange
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_star = self._create_token("STAR", "*", 1, 3)
        parser_state = self._create_parser_state([token_a, token_star], pos=0)
        
        unary_a = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        mock_unary.side_effect = [unary_a, IndexError("No tokens")]

        # Act & Assert
        with self.assertRaises(IndexError):
            _parse_multiplicative_expr(parser_state)

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_non_multiplicative_operator_stops(self, mock_unary):
        """测试：遇到非乘除运算符时停止解析。"""
        # Arrange
        token_a = self._create_token("IDENTIFIER", "a", 1, 1)
        token_plus = self._create_token("PLUS", "+", 1, 3)
        token_b = self._create_token("IDENTIFIER", "b", 1, 5)
        parser_state = self._create_parser_state([token_a, token_plus, token_b], pos=0)
        
        unary_a = self._create_ast_node("IDENTIFIER", "a", [], 1, 1)
        mock_unary.return_value = unary_a

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert
        self.assertEqual(result, unary_a)
        self.assertEqual(parser_state["pos"], 0)  # 没有消费 token，因为 + 不是乘除运算符
        mock_unary.assert_called_once_with(parser_state)

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_multiple_multiplications(self, mock_unary):
        """测试：多个连续乘法 (a * b * c * d)。"""
        # Arrange
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("STAR", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("STAR", "*", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("STAR", "*", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        unary_nodes = [
            self._create_ast_node("IDENTIFIER", "a", [], 1, 1),
            self._create_ast_node("IDENTIFIER", "b", [], 1, 5),
            self._create_ast_node("IDENTIFIER", "c", [], 1, 9),
            self._create_ast_node("IDENTIFIER", "d", [], 1, 13),
        ]
        mock_unary.side_effect = unary_nodes

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert: 验证左结合性 (((a * b) * c) * d)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["column"], 11)  # 最后一个 * 的列号
        
        # 验证结构
        rightmost = result["children"][1]
        self.assertEqual(rightmost, unary_nodes[3])  # d
        
        left_part = result["children"][0]
        self.assertEqual(left_part["value"], "*")
        self.assertEqual(left_part["column"], 7)  # 倒数第二个 * 的列号
        
        self.assertEqual(parser_state["pos"], 7)

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_mixed_multiply_divide(self, mock_unary):
        """测试：混合乘除表达式 (a * b / c * d)。"""
        # Arrange
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("STAR", "*", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("SLASH", "/", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("STAR", "*", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        unary_nodes = [
            self._create_ast_node("IDENTIFIER", "a", [], 1, 1),
            self._create_ast_node("IDENTIFIER", "b", [], 1, 5),
            self._create_ast_node("IDENTIFIER", "c", [], 1, 9),
            self._create_ast_node("IDENTIFIER", "d", [], 1, 13),
        ]
        mock_unary.side_effect = unary_nodes

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert: 验证左结合性 (((a * b) / c) * d)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["column"], 11)
        
        # 最右操作数是 d
        self.assertEqual(result["children"][1], unary_nodes[3])
        
        # 左侧应该是 ((a * b) / c)
        left_part = result["children"][0]
        self.assertEqual(left_part["value"], "/")
        self.assertEqual(left_part["column"], 7)
        
        self.assertEqual(parser_state["pos"], 7)

    @patch("_parse_multiplicative_expr_src._parse_unary_expr")
    def test_starting_pos_not_zero(self, mock_unary):
        """测试：parser_state 的 pos 不从 0 开始。"""
        # Arrange
        token_skip = self._create_token("PLUS", "+", 1, 1)
        token_a = self._create_token("IDENTIFIER", "a", 1, 3)
        token_star = self._create_token("STAR", "*", 1, 5)
        token_b = self._create_token("IDENTIFIER", "b", 1, 7)
        parser_state = self._create_parser_state([token_skip, token_a, token_star, token_b], pos=1)
        
        unary_a = self._create_ast_node("IDENTIFIER", "a", [], 1, 3)
        unary_b = self._create_ast_node("IDENTIFIER", "b", [], 1, 7)
        mock_unary.side_effect = [unary_a, unary_b]

        # Act
        result = _parse_multiplicative_expr(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(parser_state["pos"], 4)  # 从 pos=1 开始，消费了 3 个 token


if __name__ == "__main__":
    unittest.main()