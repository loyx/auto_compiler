# === std / third-party imports ===
import unittest

# === relative import for UUT ===
from ._current_token_src import _current_token


class TestCurrentToken(unittest.TestCase):
    """单元测试：_current_token 函数"""

    def test_current_token_within_bounds_first(self):
        """测试：pos=0，返回第一个 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})

    def test_current_token_within_bounds_middle(self):
        """测试：pos 在中间位置，返回对应 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "OPERATOR", "value": "=", "line": 1, "column": 3})

    def test_current_token_within_bounds_last(self):
        """测试：pos 指向最后一个 token，返回该 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "42", "line": 1, "column": 5})

    def test_current_token_pos_equals_length(self):
        """测试：pos == len(tokens)，越界返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_pos_greater_than_length(self):
        """测试：pos > len(tokens)，越界返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_negative_pos(self):
        """测试：pos < 0，越界返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": -1,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_empty_tokens(self):
        """测试：tokens 为空列表，任何 pos 都返回 None"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_missing_tokens_key(self):
        """测试：parser_state 缺少 tokens 键，返回 None"""
        parser_state = {
            "pos": 0,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_missing_pos_key(self):
        """测试：parser_state 缺少 pos 键，默认 pos=0"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1})

    def test_current_token_tokens_is_none(self):
        """测试：tokens 为 None，返回 None"""
        parser_state = {
            "tokens": None,
            "pos": 0,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_no_side_effects(self):
        """测试：函数无副作用，不修改 parser_state"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.src",
        }
        original_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.src",
        }
        _current_token(parser_state)
        self.assertEqual(parser_state, original_state)

    def test_current_token_single_token(self):
        """测试：只有一个 token 的情况"""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "return", "line": 10, "column": 5},
            ],
            "pos": 0,
            "filename": "test.src",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "KEYWORD", "value": "return", "line": 10, "column": 5})


if __name__ == "__main__":
    unittest.main()
