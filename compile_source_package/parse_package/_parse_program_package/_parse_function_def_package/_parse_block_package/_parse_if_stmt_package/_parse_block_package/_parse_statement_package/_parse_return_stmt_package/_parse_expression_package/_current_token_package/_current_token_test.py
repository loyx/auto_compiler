# === std / third-party imports ===
import unittest

# === relative imports ===
from ._current_token_src import _current_token, ParserState


class TestCurrentToken(unittest.TestCase):
    """测试 _current_token 函数"""

    def test_happy_path_returns_token_at_pos(self):
        """正常路径：pos 有效时返回对应位置的 token"""
        tokens = [
            {"type": "keyword", "value": "if", "line": 1, "column": 1},
            {"type": "identifier", "value": "x", "line": 1, "column": 4},
            {"type": "operator", "value": ">", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result, {"type": "identifier", "value": "x", "line": 1, "column": 4})

    def test_boundary_first_token(self):
        """边界值：pos=0 返回第一个 token"""
        tokens = [
            {"type": "keyword", "value": "def", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result, {"type": "keyword", "value": "def", "line": 1, "column": 1})

    def test_boundary_last_token(self):
        """边界值：pos 在最后一个有效索引"""
        tokens = [
            {"type": "keyword", "value": "return", "line": 5, "column": 1},
            {"type": "identifier", "value": "result", "line": 5, "column": 8},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # 最后一个有效索引
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result, {"type": "identifier", "value": "result", "line": 5, "column": 8})

    def test_edge_empty_tokens_returns_none(self):
        """边缘情况：tokens 为空列表时返回 None"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_edge_pos_beyond_length_returns_none(self):
        """边缘情况：pos >= len(tokens) 时返回 None"""
        tokens = [
            {"type": "number", "value": "42", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 5,  # 超出范围
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_edge_pos_equals_length_returns_none(self):
        """边缘情况：pos == len(tokens) 时返回 None"""
        tokens = [
            {"type": "string", "value": "hello", "line": 1, "column": 1},
            {"type": "string", "value": "world", "line": 1, "column": 8},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 2,  # 等于长度
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_edge_missing_tokens_key_defaults_to_empty(self):
        """边缘情况：缺少 tokens 键时默认为空列表"""
        parser_state: ParserState = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_edge_missing_pos_key_defaults_to_zero(self):
        """边缘情况：缺少 pos 键时默认为 0"""
        tokens = [
            {"type": "punctuation", "value": "(", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
        }
        
        result = _current_token(parser_state)
        
        self.assertEqual(result, {"type": "punctuation", "value": "(", "line": 1, "column": 1})

    def test_no_side_effect_parser_state_unchanged(self):
        """验证无副作用：调用后 parser_state 不被修改"""
        tokens = [
            {"type": "keyword", "value": "while", "line": 3, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }
        original_pos = parser_state["pos"]
        original_tokens = parser_state["tokens"]
        
        _current_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_multiple_calls_same_result(self):
        """多次调用返回相同结果（不消费 token）"""
        tokens = [
            {"type": "operator", "value": "+", "line": 2, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
        }
        
        result1 = _current_token(parser_state)
        result2 = _current_token(parser_state)
        result3 = _current_token(parser_state)
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)


if __name__ == "__main__":
    unittest.main()
