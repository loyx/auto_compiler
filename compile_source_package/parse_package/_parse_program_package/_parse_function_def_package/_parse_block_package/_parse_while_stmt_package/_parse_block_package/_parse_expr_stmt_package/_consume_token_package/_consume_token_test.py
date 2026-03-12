# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import for UUT ===
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """测试 _consume_token 函数的行为"""

    def test_consume_token_success(self):
        """Happy Path: token 类型匹配，pos 正确递增"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 2, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "SEMICOLON")
        
        self.assertEqual(result["pos"], 1)
        self.assertEqual(result["tokens"], parser_state["tokens"])
        self.assertEqual(result["filename"], "test.py")

    def test_consume_token_second_token(self):
        """Happy Path: 消费第二个 token"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 2, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "LBRACE")
        
        self.assertEqual(result["pos"], 2)

    def test_consume_token_empty_tokens(self):
        """边界值：tokens 列表为空，应抛出 EOF 错误"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "SEMICOLON")
        
        self.assertIn("EOF", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_consume_token_pos_at_end(self):
        """边界值：pos 已在 tokens 末尾，应抛出 EOF 错误"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "LBRACE")
        
        self.assertIn("EOF", str(context.exception))

    def test_consume_token_type_mismatch(self):
        """错误处理：token 类型不匹配，应抛出带位置信息的 SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 5, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "SEMICOLON")
        
        error_msg = str(context.exception)
        self.assertIn("test.py:5:3", error_msg)
        self.assertIn("期望 'SEMICOLON'", error_msg)
        self.assertIn("但遇到 'LBRACE'", error_msg)

    def test_consume_token_missing_parser_state_fields(self):
        """边界值：parser_state 缺少字段，应使用默认值"""
        parser_state: Dict[str, Any] = {}
        
        with self.assertRaises(SyntaxError):
            _consume_token(parser_state, "SEMICOLON")

    def test_consume_token_missing_token_fields(self):
        """边界值：token 缺少 type 字段，应使用 UNKNOWN 默认值"""
        parser_state = {
            "tokens": [
                {"value": ";", "line": 1, "column": 10},  # 缺少 type
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "SEMICOLON")
        
        error_msg = str(context.exception)
        self.assertIn("UNKNOWN", error_msg)

    def test_consume_token_pos_increment_is_one(self):
        """验证：pos 每次只递增 1"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 2},
                {"type": "LBRACE", "value": "{", "line": 2, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result1 = _consume_token(parser_state, "IDENT")
        self.assertEqual(result1["pos"], 1)
        
        result2 = _consume_token(result1, "SEMICOLON")
        self.assertEqual(result2["pos"], 2)
        
        result3 = _consume_token(result2, "LBRACE")
        self.assertEqual(result3["pos"], 3)

    def test_consume_token_preserves_other_state_fields(self):
        """验证：其他状态字段保持不变"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "",
            "custom_field": "custom_value",
        }
        
        result = _consume_token(parser_state, "SEMICOLON")
        
        self.assertEqual(result["error"], "")
        self.assertEqual(result["custom_field"], "custom_value")

    def test_consume_token_inplace_modification(self):
        """验证：原地修改 parser_state"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        original_id = id(parser_state)
        result = _consume_token(parser_state, "SEMICOLON")
        
        self.assertEqual(id(result), original_id)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
