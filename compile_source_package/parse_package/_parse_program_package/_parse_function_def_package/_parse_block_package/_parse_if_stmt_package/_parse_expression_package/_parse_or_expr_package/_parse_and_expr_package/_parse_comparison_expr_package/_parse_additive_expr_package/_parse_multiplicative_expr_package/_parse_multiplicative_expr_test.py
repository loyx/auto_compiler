# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._parse_multiplicative_expr_src import _parse_multiplicative_expr


class TestParseMultiplicativeExpr(unittest.TestCase):
    """单元测试：_parse_multiplicative_expr 函数"""

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

    @patch("_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr")
    def test_single_operand_no_operator(self, mock_unary: MagicMock):
        """测试：单个操作数，无乘除操作符"""
        operand_node = {"type": "NUMBER", "value": 42, "line": 1, "column": 1}
        mock_unary.return_value = operand_node
        
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result, operand_node)
        mock_unary.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)

    @patch("_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr")
    def test_multiplication_operator(self, mock_unary: MagicMock):
        """测试：乘法操作符 a * b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_unary.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "*", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "*")
        self.assertEqual(result["left"], left_node)
        self.assertEqual(result["right"], right_node)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_unary.call_count, 2)

    @patch("_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr")
    def test_division_operator(self, mock_unary: MagicMock):
        """测试：除法操作符 a / b"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "NUMBER", "value": 2, "line": 1, "column": 5}
        
        mock_unary.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "/", line=1, column=3),
            self._create_token("NUMBER", "2", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "/")
        self.assertEqual(result["left"], left_node)
        self.assertEqual(result["right"], right_node)
        self.assertEqual(parser_state["pos"], 3)

    @patch("_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr")
    def test_modulo_operator(self, mock_unary: MagicMock):
        """测试：取模操作符 a % b"""
        left_node = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1}
        right_node = {"type": "NUMBER", "value": 3, "line": 2, "column": 5}
        
        mock_unary.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "x", line=2, column=1),
            self._create_token("OPERATOR", "%", line=2, column=3),
            self._create_token("NUMBER", "3", line=2, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "%")
        self.assertEqual(result["left"], left_node)
        self.assertEqual(result["right"], right_node)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)

    @patch("_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr")
    def test_left_associativity_multiple_operators(self, mock_unary: MagicMock):
        """测试：左结合性 - 多个操作符 a * b / c % d"""
        node_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        node_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        node_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        node_d = {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        
        mock_unary.side_effect = [node_a, node_b, node_c, node_d]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "*", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("OPERATOR", "/", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9),
            self._create_token("OPERATOR", "%", line=1, column=11),
            self._create_token("IDENTIFIER", "d", line=1, column=13)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "%")
        self.assertEqual(result["right"], node_d)
        
        left_subtree = result["left"]
        self.assertEqual(left_subtree["type"], "BINARY_OP")
        self.assertEqual(left_subtree["operator"], "/")
        self.assertEqual(left_subtree["right"], node_c)
        
        inner_subtree = left_subtree["left"]
        self.assertEqual(inner_subtree["type"], "BINARY_OP")
        self.assertEqual(inner_subtree["operator"], "*")
        self.assertEqual(inner_subtree["left"], node_a)
        self.assertEqual(inner_subtree["right"], node_b)
        
        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(mock_unary.call_count, 4)

    @patch("_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_unary_expr")
    def test_empty_tokens(self, mock_unary: MagicMock):
        """测试：空 tokens 列表"""
        mock_unary.side_effect = IndexError("No tokens")
        
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(IndexError):
            _parse_multiplicative_expr(parser_state)

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_position_at_end(self, mock_unary: MagicMock):
        """测试：pos 在 tokens 末尾"""
        operand_node = {"type": "NUMBER", "value": 42, "line": 1, "column": 1}
        mock_unary.return_value = operand_node
        
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result, operand_node)
        mock_unary.assert_called_once_with(parser_state)

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_operator_at_end_without_right_operand(self, mock_unary: MagicMock):
        """测试：操作符在末尾，缺少右操作数"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        mock_unary.side_effect = [left_node, IndexError("No right operand")]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "*", line=1, column=3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(IndexError):
            _parse_multiplicative_expr(parser_state)

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_mixed_operators_chain(self, mock_unary: MagicMock):
        """测试：混合操作符链 a * b % c / d"""
        node_a = {"type": "NUMBER", "value": 10, "line": 1, "column": 1}
        node_b = {"type": "NUMBER", "value": 2, "line": 1, "column": 5}
        node_c = {"type": "NUMBER", "value": 3, "line": 1, "column": 9}
        node_d = {"type": "NUMBER", "value": 4, "line": 1, "column": 13}
        
        mock_unary.side_effect = [node_a, node_b, node_c, node_d]
        
        tokens = [
            self._create_token("NUMBER", "10", line=1, column=1),
            self._create_token("OPERATOR", "*", line=1, column=3),
            self._create_token("NUMBER", "2", line=1, column=5),
            self._create_token("OPERATOR", "%", line=1, column=7),
            self._create_token("NUMBER", "3", line=1, column=9),
            self._create_token("OPERATOR", "/", line=1, column=11),
            self._create_token("NUMBER", "4", line=1, column=13)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result["operator"], "/")
        self.assertEqual(result["right"], node_d)
        
        left_subtree = result["left"]
        self.assertEqual(left_subtree["operator"], "%")
        self.assertEqual(left_subtree["right"], node_c)
        
        inner_subtree = left_subtree["left"]
        self.assertEqual(inner_subtree["operator"], "*")
        self.assertEqual(inner_subtree["left"], node_a)
        self.assertEqual(inner_subtree["right"], node_b)

    @patch("._parse_multiplicative_expr_src._parse_unary_expr")
    def test_non_operator_token_stops_parsing(self, mock_unary: MagicMock):
        """测试：遇到非乘除操作符时停止解析"""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        mock_unary.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OPERATOR", "*", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("OPERATOR", "+", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_multiplicative_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "*")
        self.assertEqual(result["left"], left_node)
        self.assertEqual(result["right"], right_node)
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_unary.call_count, 2)


if __name__ == "__main__":
    unittest.main()
