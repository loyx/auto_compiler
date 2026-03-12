# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

# === UUT import ===
from ._parse_and_src import _parse_and, _current_token_is_and, _build_binary_op_node


# === Test Cases ===
class TestParseAnd(unittest.TestCase):
    """测试 _parse_and 函数的逻辑与表达式解析功能。"""

    def test_single_comparison_no_and(self):
        """测试单一比较表达式，无 && 运算符。"""
        comparison_node = {"type": "COMPARISON", "value": "==", "children": [], "line": 1, "column": 1}
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.txt"
        }

        with patch.object(_parse_comparison, '__call__', return_value=comparison_node) as mock_parse_comparison:
            with patch.object(_current_token_is_and, '__call__', return_value=False) as mock_is_and:
                result = _parse_and(parser_state)

        self.assertEqual(result, comparison_node)
        mock_parse_comparison.assert_called_once_with(parser_state)
        mock_is_and.assert_called_once_with(parser_state)

    def test_two_and_operators_left_associative(self):
        """测试两个 && 运算符，验证左结合性：(a && b) && c。"""
        comp_a = {"type": "COMPARISON", "value": "a==1", "children": [], "line": 1, "column": 1}
        comp_b = {"type": "COMPARISON", "value": "b==2", "children": [], "line": 1, "column": 5}
        comp_c = {"type": "COMPARISON", "value": "c==3", "children": [], "line": 1, "column": 9}
        
        and_token_1 = {"type": "AND", "value": "&&", "line": 1, "column": 4}
        and_token_2 = {"type": "AND", "value": "&&", "line": 1, "column": 8}

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "a", "line": 1, "column": 1},
                and_token_1,
                {"type": "NUMBER", "value": "b", "line": 1, "column": 5},
                and_token_2,
                {"type": "NUMBER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        # 模拟三次 _parse_comparison 调用，分别返回 comp_a, comp_b, comp_c
        comparison_results = [comp_a, comp_b, comp_c]
        call_count = [0]

        def parse_comparison_side_effect(state):
            result = comparison_results[call_count[0]]
            call_count[0] += 1
            return result

        # 模拟两次 _current_token_is_and 返回 True，然后 False
        is_and_results = [True, True, False]
        is_and_count = [0]

        def is_and_side_effect(state):
            result = is_and_results[is_and_count[0]]
            is_and_count[0] += 1
            return result

        # 模拟 _consume_token 返回两个 AND token
        consume_results = [and_token_1, and_token_2]
        consume_count = [0]

        def consume_token_side_effect(state, token_type):
            result = consume_results[consume_count[0]]
            consume_count[0] += 1
            return result

        with patch.object(_parse_comparison, '__call__', side_effect=parse_comparison_side_effect) as mock_parse_comparison:
            with patch.object(_current_token_is_and, '__call__', side_effect=is_and_side_effect) as mock_is_and:
                with patch.object(_consume_token, '__call__', side_effect=consume_token_side_effect) as mock_consume:
                    result = _parse_and(parser_state)

        # 验证结果是左结合的：((a && b) && c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "&&")
        self.assertEqual(result["line"], and_token_2["line"])
        self.assertEqual(result["column"], and_token_2["column"])
        
        # 右操作数应该是 comp_c
        self.assertEqual(result["children"][1], comp_c)
        
        # 左操作数应该是 (a && b)
        left_op = result["children"][0]
        self.assertEqual(left_op["type"], "BINARY_OP")
        self.assertEqual(left_op["value"], "&&")
        self.assertEqual(left_op["children"][0], comp_a)
        self.assertEqual(left_op["children"][1], comp_b)

        # 验证调用次数
        self.assertEqual(mock_parse_comparison.call_count, 3)
        self.assertEqual(mock_is_and.call_count, 3)
        self.assertEqual(mock_consume.call_count, 2)

    def test_current_token_is_and_true(self):
        """测试 _current_token_is_and 当当前 token 是 AND 时返回 True。"""
        parser_state = {
            "tokens": [{"type": "AND", "value": "&&", "line": 1, "column": 1}],
            "pos": 0
        }
        result = _current_token_is_and(parser_state)
        self.assertTrue(result)

    def test_current_token_is_and_false_different_type(self):
        """测试 _current_token_is_and 当当前 token 不是 AND 时返回 False。"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0
        }
        result = _current_token_is_and(parser_state)
        self.assertFalse(result)

    def test_current_token_is_and_false_pos_at_end(self):
        """测试 _current_token_is_and 当 pos 在 tokens 末尾时返回 False。"""
        parser_state = {
            "tokens": [{"type": "AND", "value": "&&", "line": 1, "column": 1}],
            "pos": 1
        }
        result = _current_token_is_and(parser_state)
        self.assertFalse(result)

    def test_current_token_is_and_false_empty_tokens(self):
        """测试 _current_token_is_and 当 tokens 为空时返回 False。"""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        result = _current_token_is_and(parser_state)
        self.assertFalse(result)

    def test_current_token_is_and_missing_pos(self):
        """测试 _current_token_is_and 当 parser_state 缺少 pos 字段时使用默认值 0。"""
        parser_state = {
            "tokens": [{"type": "AND", "value": "&&", "line": 1, "column": 1}]
        }
        result = _current_token_is_and(parser_state)
        self.assertTrue(result)

    def test_current_token_is_and_missing_tokens(self):
        """测试 _current_token_is_and 当 parser_state 缺少 tokens 字段时使用空列表。"""
        parser_state = {
            "pos": 0
        }
        result = _current_token_is_and(parser_state)
        self.assertFalse(result)

    def test_build_binary_op_node(self):
        """测试 _build_binary_op_node 构建正确的 AST 节点。"""
        left = {"type": "COMPARISON", "value": "a==1", "line": 1, "column": 1}
        right = {"type": "COMPARISON", "value": "b==2", "line": 1, "column": 5}
        and_token = {"type": "AND", "value": "&&", "line": 1, "column": 4}

        result = _build_binary_op_node(left, right, and_token)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["children"], [left, right])
        self.assertEqual(result["value"], "&&")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 4)

    def test_build_binary_op_node_missing_token_fields(self):
        """测试 _build_binary_op_node 当 token 缺少 line/column 字段时使用 None。"""
        left = {"type": "COMPARISON", "value": "a==1"}
        right = {"type": "COMPARISON", "value": "b==2"}
        and_token = {"type": "AND", "value": "&&"}

        result = _build_binary_op_node(left, right, and_token)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["children"], [left, right])
        self.assertEqual(result["value"], "&&")
        self.assertIsNone(result["line"])
        self.assertIsNone(result["column"])

    def test_four_and_operators_chain(self):
        """测试四个 && 运算符链，验证左结合性：(((a && b) && c) && d)。"""
        comp_nodes = [
            {"type": "COMPARISON", "value": f"comp_{i}", "children": [], "line": 1, "column": i}
            for i in range(4)
        ]
        and_tokens = [
            {"type": "AND", "value": "&&", "line": 1, "column": i + 0.5}
            for i in range(4)
        ]

        parser_state = {"tokens": [], "pos": 0, "filename": "test.txt"}

        comparison_results = comp_nodes.copy()
        comparison_count = [0]

        def parse_comparison_side_effect(state):
            result = comparison_results[comparison_count[0]]
            comparison_count[0] += 1
            return result

        is_and_results = [True, True, True, True, False]
        is_and_count = [0]

        def is_and_side_effect(state):
            result = is_and_results[is_and_count[0]]
            is_and_count[0] += 1
            return result

        consume_results = and_tokens.copy()
        consume_count = [0]

        def consume_token_side_effect(state, token_type):
            result = consume_results[consume_count[0]]
            consume_count[0] += 1
            return result

        with patch.object(_parse_comparison, '__call__', side_effect=parse_comparison_side_effect):
            with patch.object(_current_token_is_and, '__call__', side_effect=is_and_side_effect):
                with patch.object(_consume_token, '__call__', side_effect=consume_token_side_effect):
                    result = _parse_and(parser_state)

        # 验证最外层是第四个 && 运算
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "&&")
        self.assertEqual(result["children"][1], comp_nodes[3])
        
        # 验证左结合结构
        left_level_1 = result["children"][0]
        self.assertEqual(left_level_1["children"][1], comp_nodes[2])
        
        left_level_2 = left_level_1["children"][0]
        self.assertEqual(left_level_2["children"][1], comp_nodes[1])
        self.assertEqual(left_level_2["children"][0], comp_nodes[0])


if __name__ == "__main__":
    unittest.main()
