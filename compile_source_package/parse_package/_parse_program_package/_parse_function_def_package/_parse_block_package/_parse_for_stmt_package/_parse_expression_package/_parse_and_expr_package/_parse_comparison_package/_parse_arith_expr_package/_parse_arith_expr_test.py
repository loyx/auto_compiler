import unittest
from unittest.mock import patch
from typing import Dict, Any, Callable

from ._parse_arith_expr_src import _parse_arith_expr


class TestParseArithExpr(unittest.TestCase):
    """测试 _parse_arith_expr 函数"""
    
    def _create_term_mock(self, parser_state: Dict[str, Any], return_node: Dict[str, Any]) -> Callable:
        """创建模拟 _parse_term 的函数，自动更新 pos"""
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = state.get("pos", 0) + 1
            return return_node
        return mock_term
    
    def test_single_term_no_operator(self):
        """测试单个 term，无运算符"""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        tokens = [token_a]
        parser_state = {"tokens": tokens, "pos": 0}
        
        mock_term_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = self._create_term_mock(parser_state, mock_term_node)
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "a")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_term.assert_called_once()
    
    def test_addition_operator(self):
        """测试加法运算符 a + b"""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        token_plus = {"type": "PLUS", "value": "+", "line": 1, "column": 3}
        token_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        tokens = [token_a, token_plus, token_b]
        parser_state = {"tokens": tokens, "pos": 0}
        
        call_count = [0]
        mock_nodes = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            state["pos"] = state.get("pos", 0) + 1
            return mock_nodes[call_count[0] - 1]
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][1]["value"], "b")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_term.call_count, 2)
    
    def test_subtraction_operator(self):
        """测试减法运算符 a - b"""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 10}
        token_minus = {"type": "MINUS", "value": "-", "line": 2, "column": 12}
        token_b = {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 14}
        tokens = [token_a, token_minus, token_b]
        parser_state = {"tokens": tokens, "pos": 0}
        
        call_count = [0]
        mock_nodes = [
            {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 10},
            {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 14}
        ]
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            state["pos"] = state.get("pos", 0) + 1
            return mock_nodes[call_count[0] - 1]
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "b")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_left_associativity(self):
        """测试左结合性：a - b - c 应解析为 ((a - b) - c)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "MINUS", "value": "-", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]
        parser_state = {"tokens": tokens, "pos": 0}
        
        call_count = [0]
        mock_nodes = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            state["pos"] = state.get("pos", 0) + 1
            return mock_nodes[call_count[0] - 1]
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            # 验证左结合结构：((a - b) - c)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            
            # 左侧应该是 (a - b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "-")
            self.assertEqual(left_child["children"][0]["value"], "a")
            self.assertEqual(left_child["children"][1]["value"], "b")
            
            # 右侧应该是 c
            right_child = result["children"][1]
            self.assertEqual(right_child["type"], "IDENTIFIER")
            self.assertEqual(right_child["value"], "c")
            
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_term.call_count, 3)
    
    def test_multiple_mixed_operators(self):
        """测试多个混合运算符：a + b - c + d"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "MINUS", "value": "-", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            {"type": "PLUS", "value": "+", "line": 1, "column": 11},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        ]
        parser_state = {"tokens": tokens, "pos": 0}
        
        call_count = [0]
        mock_nodes = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        ]
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            state["pos"] = state.get("pos", 0) + 1
            return mock_nodes[call_count[0] - 1]
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            # 验证结构：(((a + b) - c) + d)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")  # 最外层是最后一个 +
            
            # 左侧应该是 ((a + b) - c)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "-")
            
            # 左左侧应该是 (a + b)
            left_left = left_child["children"][0]
            self.assertEqual(left_left["type"], "BINARY_OP")
            self.assertEqual(left_left["value"], "+")
            self.assertEqual(left_left["children"][0]["value"], "a")
            self.assertEqual(left_left["children"][1]["value"], "b")
            
            # 左右侧应该是 c
            self.assertEqual(left_child["children"][1]["value"], "c")
            
            # 右侧应该是 d
            self.assertEqual(result["children"][1]["value"], "d")
            
            self.assertEqual(parser_state["pos"], 7)
            self.assertEqual(mock_parse_term.call_count, 4)
    
    def test_term_returns_error(self):
        """测试当 _parse_term 返回 ERROR 节点时的处理"""
        token_a = {"type": "INVALID", "value": "x", "line": 1, "column": 1}
        tokens = [token_a]
        parser_state = {"tokens": tokens, "pos": 0}
        
        error_node = {"type": "ERROR", "value": "Invalid term", "line": 1, "column": 1}
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = state.get("pos", 0) + 1
            return error_node
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Invalid term")
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_term.assert_called_once()
    
    def test_right_term_returns_error(self):
        """测试当右侧 _parse_term 返回 ERROR 时的处理"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "INVALID", "value": "x", "line": 1, "column": 5}
        ]
        parser_state = {"tokens": tokens, "pos": 0}
        
        call_count = [0]
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            state["pos"] = state.get("pos", 0) + 1
            if call_count[0] == 1:
                return {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            else:
                return {"type": "ERROR", "value": "Invalid term", "line": 1, "column": 5}
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Invalid term")
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_term.call_count, 2)
    
    def test_empty_tokens(self):
        """测试空 tokens 列表"""
        parser_state = {"tokens": [], "pos": 0}
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            return {"type": "ERROR", "value": "No token", "line": 0, "column": 0}
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            mock_parse_term.assert_called_once()
    
    def test_stops_at_non_arithmetic_token(self):
        """测试在非算术运算符 token 处停止（如 RPAREN）"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
        ]
        parser_state = {"tokens": tokens, "pos": 0}
        
        call_count = [0]
        mock_nodes = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            call_count[0] += 1
            state["pos"] = state.get("pos", 0) + 1
            return mock_nodes[call_count[0] - 1]
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_term.call_count, 2)
    
    def test_position_at_end(self):
        """测试 pos 已在 tokens 末尾的情况"""
        tokens = [{"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 1}
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            return {"type": "ERROR", "value": "Out of bounds", "line": 0, "column": 0}
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_term.assert_called_once()
    
    def test_missing_tokens_key(self):
        """测试 parser_state 缺少 tokens 键的情况"""
        parser_state = {"pos": 0}
        
        def mock_term(state: Dict[str, Any]) -> Dict[str, Any]:
            return {"type": "ERROR", "value": "No tokens", "line": 0, "column": 0}
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = mock_term
            
            result = _parse_arith_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            mock_parse_term.assert_called_once()


if __name__ == "__main__":
    unittest.main()
