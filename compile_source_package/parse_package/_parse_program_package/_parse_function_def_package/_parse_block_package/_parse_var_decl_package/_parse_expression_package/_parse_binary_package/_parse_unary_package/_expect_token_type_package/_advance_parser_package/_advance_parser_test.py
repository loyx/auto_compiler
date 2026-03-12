# === std / third-party imports ===
import unittest
from typing import List

# === relative import of target function ===
from ._advance_parser_src import _advance_parser, ParserState, Token

# === test cases ===
class TestAdvanceParser(unittest.TestCase):
    """测试 _advance_parser 函数的行为"""

    def _create_parser_state(
        self,
        tokens: List[Token],
        pos: int = 0,
        filename: str = "test.py"
    ) -> ParserState:
        """辅助函数：创建 ParserState 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Token:
        """辅助函数：创建 Token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_advance_from_zero(self):
        """测试从 pos=0 开始前进"""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
            self._create_token("OPERATOR", "="),
            self._create_token("NUMBER", "42")
        ]
        state = self._create_parser_state(tokens, pos=0)

        _advance_parser(state)

        self.assertEqual(state["pos"], 1)
        self.assertEqual(len(state["tokens"]), 3)

    def test_advance_middle_position(self):
        """测试从中间位置前进"""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
            self._create_token("OPERATOR", "="),
            self._create_token("NUMBER", "42"),
            self._create_token("SEMICOLON", ";")
        ]
        state = self._create_parser_state(tokens, pos=2)

        _advance_parser(state)

        self.assertEqual(state["pos"], 3)

    def test_advance_at_last_token(self):
        """测试在最后一个 token 处前进"""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
            self._create_token("OPERATOR", "="),
            self._create_token("NUMBER", "42")
        ]
        state = self._create_parser_state(tokens, pos=2)

        _advance_parser(state)

        self.assertEqual(state["pos"], 3)
        self.assertGreater(state["pos"], len(state["tokens"]) - 1)

    def test_advance_beyond_tokens(self):
        """测试 pos 已超出 tokens 长度时仍会递增"""
        tokens = [
            self._create_token("IDENTIFIER", "x")
        ]
        state = self._create_parser_state(tokens, pos=5)

        _advance_parser(state)

        self.assertEqual(state["pos"], 6)

    def test_advance_multiple_times(self):
        """测试多次连续前进"""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
            self._create_token("OPERATOR", "="),
            self._create_token("NUMBER", "42"),
            self._create_token("SEMICOLON", ";"),
            self._create_token("IDENTIFIER", "y")
        ]
        state = self._create_parser_state(tokens, pos=0)

        _advance_parser(state)
        _advance_parser(state)
        _advance_parser(state)

        self.assertEqual(state["pos"], 3)

    def test_advance_modifies_in_place(self):
        """测试函数直接修改传入的字典（原地修改）"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        state = self._create_parser_state(tokens, pos=0)
        original_id = id(state)

        _advance_parser(state)

        self.assertEqual(id(state), original_id)
        self.assertEqual(state["pos"], 1)

    def test_advance_empty_tokens(self):
        """测试 tokens 为空列表时的行为"""
        tokens: List[Token] = []
        state = self._create_parser_state(tokens, pos=0)

        _advance_parser(state)

        self.assertEqual(state["pos"], 1)
        self.assertEqual(len(state["tokens"]), 0)

    def test_advance_preserves_other_fields(self):
        """测试前进操作不影响其他字段"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        state = self._create_parser_state(tokens, pos=0, filename="source.py")
        state["error"] = None

        _advance_parser(state)

        self.assertEqual(state["filename"], "source.py")
        self.assertEqual(state["error"], None)
        self.assertEqual(len(state["tokens"]), 1)

# === test runner ===
if __name__ == "__main__":
    unittest.main()
