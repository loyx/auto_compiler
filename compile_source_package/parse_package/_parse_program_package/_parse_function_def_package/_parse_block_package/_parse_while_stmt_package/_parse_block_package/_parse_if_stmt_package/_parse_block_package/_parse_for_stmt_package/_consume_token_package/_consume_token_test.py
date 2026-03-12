# -*- coding: utf-8 -*-
"""
单元测试文件：_consume_token 函数测试
"""
import unittest

# 相对导入被测模块
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """_consume_token 函数的单元测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_consume_token_without_type_check(self):
        """测试：不指定 expected_type 时正常消费 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        token = _consume_token(parser_state)
        
        self.assertEqual(token["type"], "IDENTIFIER")
        self.assertEqual(token["value"], "x")
        self.assertEqual(token["line"], 1)
        self.assertEqual(token["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_matching_expected_type(self):
        """测试：指定 expected_type 且类型匹配时正常消费"""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        token = _consume_token(parser_state, expected_type="KEYWORD")
        
        self.assertEqual(token["type"], "KEYWORD")
        self.assertEqual(token["value"], "if")
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_with_mismatched_expected_type(self):
        """测试：指定 expected_type 但类型不匹配时抛出 SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, expected_type="KEYWORD")
        
        self.assertIn("Expected KEYWORD, got IDENTIFIER", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_pos_at_end(self):
        """测试：pos 在 tokens 末尾时抛出 SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_pos_beyond_end(self):
        """测试：pos 超出 tokens 范围时抛出 SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_empty_tokens(self):
        """测试：tokens 为空列表时抛出 SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_multiple_consumes(self):
        """测试：连续消费多个 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        token1 = _consume_token(parser_state)
        self.assertEqual(token1["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 1)
        
        token2 = _consume_token(parser_state)
        self.assertEqual(token2["type"], "OPERATOR")
        self.assertEqual(parser_state["pos"], 2)
        
        token3 = _consume_token(parser_state)
        self.assertEqual(token3["type"], "NUMBER")
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_pos_increment_is_one(self):
        """测试：pos 每次只增加 1"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        _consume_token(parser_state)
        self.assertEqual(parser_state["pos"], 1)
        
        _consume_token(parser_state)
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_returns_correct_token_at_pos(self):
        """测试：从中间位置开始消费返回正确的 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "first", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "second", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "third", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        token = _consume_token(parser_state)
        
        self.assertEqual(token["value"], "second")
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_preserves_other_state_fields(self):
        """测试：消费 token 不影响其他状态字段"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test_module.py",
            "error": "some previous error"
        }
        
        _consume_token(parser_state)
        
        self.assertEqual(parser_state["filename"], "test_module.py")
        self.assertEqual(parser_state["error"], "some previous error")
        self.assertEqual(len(parser_state["tokens"]), 1)


if __name__ == "__main__":
    unittest.main()
