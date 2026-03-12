# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === sub function imports ===
from ._parse_logical_or_src import _parse_logical_or


class TestParseLogicalOr(unittest.TestCase):
    """单元测试：_parse_logical_or 函数"""

    def test_single_operand_no_or(self):
        """测试：单个操作数，无 OR 运算符"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_logical_or_src._parse_logical_and", return_value=left_node) as mock_and:
            with patch("._parse_logical_or_src._current_token_type", return_value=""):
                result = _parse_logical_or(parser_state)
        
        self.assertEqual(result, left_node)
        mock_and.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)

    def test_one_or_operator(self):
        """测试：一个 OR 运算符"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 6
        }
        
        or_token = {
            "type": "OR",
            "value": "||",
            "line": 1,
            "column": 3
        }
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[left_node, right_node]) as mock_and:
            with patch("._parse_logical_or_src._current_token_type", side_effect=["OR", ""]) as mock_token_type:
                with patch("._parse_logical_or_src._expect_token", return_value=or_token) as mock_expect:
                    result = _parse_logical_or(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(result["children"], [left_node, right_node])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        
        self.assertEqual(mock_and.call_count, 2)
        mock_expect.assert_called_once_with(parser_state, "OR")
        self.assertEqual(parser_state["pos"], 2)

    def test_multiple_or_operators_left_associative(self):
        """测试：多个 OR 运算符，左结合"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OR", "value": "||", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        node_a = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        node_b = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "b",
            "line": 1,
            "column": 6
        }
        
        node_c = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "c",
            "line": 1,
            "column": 11
        }
        
        or_token1 = {"type": "OR", "value": "||", "line": 1, "column": 3}
        or_token2 = {"type": "OR", "value": "||", "line": 1, "column": 8}
        
        # 第一次 OR： (a || b)
        first_binary = {
            "type": "BINARY_OP",
            "children": [node_a, node_b],
            "value": "||",
            "line": 1,
            "column": 1
        }
        
        # 第二次 OR： ((a || b) || c)
        expected_result = {
            "type": "BINARY_OP",
            "children": [first_binary, node_c],
            "value": "||",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[node_a, node_b, node_c]) as mock_and:
            with patch("._parse_logical_or_src._current_token_type", side_effect=["OR", "OR", ""]) as mock_token_type:
                with patch("._parse_logical_or_src._expect_token", side_effect=[or_token1, or_token2]) as mock_expect:
                    result = _parse_logical_or(parser_state)
        
        self.assertEqual(result, expected_result)
        self.assertEqual(mock_and.call_count, 3)
        self.assertEqual(mock_expect.call_count, 2)
        self.assertEqual(parser_state["pos"], 4)

    def test_or_with_complex_left_operand(self):
        """测试：OR 左侧为复杂表达式（来自 _parse_logical_and）"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
                {"type": "OR", "value": "||", "line": 2, "column": 7},
                {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        complex_left = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5},
                {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 7}
            ],
            "value": "&&",
            "line": 2,
            "column": 5
        }
        
        right_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "y",
            "line": 2,
            "column": 10
        }
        
        or_token = {"type": "OR", "value": "||", "line": 2, "column": 7}
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[complex_left, right_node]):
            with patch("._parse_logical_or_src._current_token_type", side_effect=["OR", ""]):
                with patch("._parse_logical_or_src._expect_token", return_value=or_token):
                    result = _parse_logical_or(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "||")
        self.assertEqual(result["children"][0], complex_left)
        self.assertEqual(result["children"][1], right_node)
        # 使用左侧操作数的 line/column
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

    def test_empty_tokens(self):
        """测试：空 token 列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        empty_node = {
            "type": "LITERAL",
            "children": [],
            "value": None,
            "line": 0,
            "column": 0
        }
        
        with patch("._parse_logical_or_src._parse_logical_and", return_value=empty_node):
            with patch("._parse_logical_or_src._current_token_type", return_value=""):
                result = _parse_logical_or(parser_state)
        
        self.assertEqual(result, empty_node)
        self.assertEqual(parser_state["pos"], 0)

    def test_pos_advances_correctly(self):
        """测试：pos 正确推进"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OR", "value": "||", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        node_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        node_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        node_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        or_token1 = {"type": "OR", "value": "||", "line": 1, "column": 3}
        or_token2 = {"type": "OR", "value": "||", "line": 1, "column": 8}
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[node_a, node_b, node_c]):
            with patch("._parse_logical_or_src._current_token_type", side_effect=["OR", "OR", "SEMICOLON"]):
                with patch("._parse_logical_or_src._expect_token", side_effect=[or_token1, or_token2]):
                    result = _parse_logical_or(parser_state)
        
        # 解析完两个 OR 表达式后，pos 应该指向第 4 个 token（索引从 0 开始）
        self.assertEqual(parser_state["pos"], 4)


if __name__ == "__main__":
    unittest.main()
