# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === relative imports ===
from ._parse_and_src import _parse_and, _is_current_token_and


# === Test Helper Types ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseAnd(unittest.TestCase):
    """测试 _parse_and 函数的逻辑 AND 表达式解析功能。"""
    
    def test_no_and_token_returns_comparison_result(self):
        """测试：当前 token 不是 AND 时，直接返回 comparison 结果，不构建 BINARY_OP。"""
        mock_comparison_result = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        mock_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with patch("._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.return_value = (mock_comparison_result, mock_state)
            
            result_ast, result_state = _parse_and(mock_state)
            
            # 验证返回的是 comparison 的结果，不是 BINARY_OP
            self.assertEqual(result_ast["type"], "IDENTIFIER")
            self.assertEqual(result_ast["value"], "a")
            mock_parse_comparison.assert_called_once_with(mock_state)
    
    def test_single_and_expression(self):
        """测试：解析单个 AND 表达式 a && b。"""
        left_comparison = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        right_comparison = {
            "type": "IDENTIFIER",
            "value": "b",
            "children": [],
            "line": 1,
            "column": 5
        }
        and_token = {
            "type": "AND",
            "value": "&&",
            "line": 1,
            "column": 3
        }
        state_after_and = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 2,
            "filename": "test.py",
            "error": ""
        }
        initial_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with patch("._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume_token:
                # 第一次调用 _parse_comparison 返回 left
                # 第二次调用 _parse_comparison 返回 right
                mock_parse_comparison.side_effect = [
                    (left_comparison, initial_state),
                    (right_comparison, state_after_and)
                ]
                mock_consume_token.return_value = (and_token, state_after_and)
                
                result_ast, result_state = _parse_and(initial_state)
                
                # 验证构建了 BINARY_OP 节点
                self.assertEqual(result_ast["type"], "BINARY_OP")
                self.assertEqual(result_ast["value"], "&&")
                self.assertEqual(result_ast["line"], 1)
                self.assertEqual(result_ast["column"], 3)
                self.assertEqual(len(result_ast["children"]), 2)
                self.assertEqual(result_ast["children"][0]["value"], "a")
                self.assertEqual(result_ast["children"][1]["value"], "b")
                
                # 验证调用顺序
                self.assertEqual(mock_parse_comparison.call_count, 2)
                mock_consume_token.assert_called_once_with(initial_state, "AND")
    
    def test_left_associative_chaining(self):
        """测试：左结合链式解析 a && b && c → 嵌套 BINARY_OP 结构。"""
        # 构建三个 comparison 结果
        comp_a = {"type": "IDENTIFIER", "value": "a", "children": [], "line": 1, "column": 1}
        comp_b = {"type": "IDENTIFIER", "value": "b", "children": [], "line": 1, "column": 5}
        comp_c = {"type": "IDENTIFIER", "value": "c", "children": [], "line": 1, "column": 9}
        
        and_token_1 = {"type": "AND", "value": "&&", "line": 1, "column": 3}
        and_token_2 = {"type": "AND", "value": "&&", "line": 1, "column": 7}
        
        state_0 = {"tokens": [], "pos": 0, "filename": "test.py", "error": ""}
        state_1 = {"tokens": [], "pos": 1, "filename": "test.py", "error": ""}
        state_2 = {"tokens": [], "pos": 2, "filename": "test.py", "error": ""}
        state_3 = {"tokens": [], "pos": 3, "filename": "test.py", "error": ""}
        
        with patch("._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume_token:
                # _parse_comparison 被调用 3 次
                mock_parse_comparison.side_effect = [
                    (comp_a, state_0),
                    (comp_b, state_1),
                    (comp_c, state_2)
                ]
                # _consume_token 被调用 2 次
                mock_consume_token.side_effect = [
                    (and_token_1, state_1),
                    (and_token_2, state_2)
                ]
                
                result_ast, result_state = _parse_and(state_0)
                
                # 验证结构：(a && b) && c
                # 外层 BINARY_OP
                self.assertEqual(result_ast["type"], "BINARY_OP")
                self.assertEqual(result_ast["value"], "&&")
                self.assertEqual(result_ast["line"], 1)
                self.assertEqual(result_ast["column"], 7)  # 第二个 AND 的位置
                
                # 左子节点应该是 (a && b)
                left_child = result_ast["children"][0]
                self.assertEqual(left_child["type"], "BINARY_OP")
                self.assertEqual(left_child["value"], "&&")
                self.assertEqual(left_child["line"], 1)
                self.assertEqual(left_child["column"], 3)
                self.assertEqual(left_child["children"][0]["value"], "a")
                self.assertEqual(left_child["children"][1]["value"], "b")
                
                # 右子节点应该是 c
                right_child = result_ast["children"][1]
                self.assertEqual(right_child["value"], "c")
                
                # 验证调用次数
                self.assertEqual(mock_parse_comparison.call_count, 3)
                self.assertEqual(mock_consume_token.call_count, 2)
    
    def test_is_current_token_and_true(self):
        """测试：_is_current_token_and 在当前 token 是 AND 时返回 True。"""
        state = {
            "tokens": [{"type": "AND", "value": "&&", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _is_current_token_and(state)
        self.assertTrue(result)
    
    def test_is_current_token_and_false(self):
        """测试：_is_current_token_and 在当前 token 不是 AND 时返回 False。"""
        state = {
            "tokens": [{"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _is_current_token_and(state)
        self.assertFalse(result)
    
    def test_is_current_token_and_at_end(self):
        """测试：_is_current_token_and 在已到达 token 列表末尾时返回 False。"""
        state = {
            "tokens": [{"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}],
            "pos": 1,  # pos 超出 tokens 长度
            "filename": "test.py",
            "error": ""
        }
        
        result = _is_current_token_and(state)
        self.assertFalse(result)
    
    def test_is_current_token_and_empty_tokens(self):
        """测试：_is_current_token_and 在 tokens 为空时返回 False。"""
        state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _is_current_token_and(state)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()