import unittest
from typing import Any, Dict

from ._parse_literal_src import _parse_literal


class TestParseLiteral(unittest.TestCase):
    """测试 _parse_literal 函数解析字面量 token 的功能。"""

    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """创建测试用的 parser_state 对象。"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test_file.py",
            "error": ""
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """创建测试用的 token 对象。"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== NUMBER Token Tests ====================

    def test_parse_integer_number(self):
        """测试解析整数字面量。"""
        token = self._create_token("NUMBER", "42")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_negative_integer(self):
        """测试解析负整数字面量。"""
        token = self._create_token("NUMBER", "-100")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], -100)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_float_number(self):
        """测试解析浮点数字面量。"""
        token = self._create_token("NUMBER", "3.14")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_negative_float(self):
        """测试解析负浮点数字面量。"""
        token = self._create_token("NUMBER", "-2.5")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], -2.5)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_zero(self):
        """测试解析零值。"""
        token = self._create_token("NUMBER", "0")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 0)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_large_number(self):
        """测试解析大数字。"""
        token = self._create_token("NUMBER", "999999999")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 999999999)
        self.assertEqual(parser_state["pos"], 1)

    # ==================== STRING Token Tests ====================

    def test_parse_string_with_double_quotes(self):
        """测试解析双引号字符串字面量。"""
        token = self._create_token("STRING", '"hello world"')
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello world")
        self.assertIsInstance(result["value"], str)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_with_single_quotes(self):
        """测试解析单引号字符串字面量。"""
        token = self._create_token("STRING", "'test string'")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "test string")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_empty_string(self):
        """测试解析空字符串字面量。"""
        token = self._create_token("STRING", '""')
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_with_special_chars(self):
        """测试解析包含特殊字符的字符串。"""
        token = self._create_token("STRING", '"hello\\nworld"')
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello\\nworld")
        self.assertEqual(parser_state["pos"], 1)

    # ==================== BOOLEAN Token Tests ====================

    def test_parse_true_boolean(self):
        """测试解析 true 布尔值。"""
        token = self._create_token("BOOLEAN", "true")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertIsInstance(result["value"], bool)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_false_boolean(self):
        """测试解析 false 布尔值。"""
        token = self._create_token("BOOLEAN", "false")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertIsInstance(result["value"], bool)
        self.assertEqual(parser_state["pos"], 1)

    # ==================== NONE Token Tests ====================

    def test_parse_none_literal(self):
        """测试解析 None 字面量。"""
        token = self._create_token("NONE", "none")
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(parser_state["pos"], 1)

    # ==================== Position Advancement Tests ====================

    def test_position_advances_after_parse(self):
        """测试解析后位置正确前进。"""
        token1 = self._create_token("NUMBER", "1")
        token2 = self._create_token("STRING", '"test"')
        parser_state = self._create_parser_state([token1, token2], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["value"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_position_from_non_zero_start(self):
        """测试从非零位置开始解析。"""
        token1 = self._create_token("NUMBER", "1")
        token2 = self._create_token("NUMBER", "2")
        token3 = self._create_token("NUMBER", "3")
        parser_state = self._create_parser_state([token1, token2, token3], pos=1)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["value"], 2)
        self.assertEqual(parser_state["pos"], 2)

    # ==================== AST Structure Tests ====================

    def test_ast_node_has_required_fields(self):
        """测试 AST 节点包含所有必需字段。"""
        token = self._create_token("NUMBER", "42", line=5, column=10)
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertIn("type", result)
        self.assertIn("value", result)
        self.assertIn("children", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)

    def test_preserves_token_location(self):
        """测试保留 token 的行列位置信息。"""
        token = self._create_token("STRING", '"test"', line=10, column=25)
        parser_state = self._create_parser_state([token])
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    # ==================== Side Effect Tests ====================

    def test_modifies_original_parser_state(self):
        """测试直接修改传入的 parser_state 对象。"""
        token = self._create_token("NUMBER", "100")
        parser_state = self._create_parser_state([token])
        original_id = id(parser_state)
        
        _parse_literal(parser_state)
        
        self.assertEqual(id(parser_state), original_id)
        self.assertEqual(parser_state["pos"], 1)

    def test_multiple_parses_advance_position_correctly(self):
        """测试多次解析正确推进位置。"""
        tokens = [
            self._create_token("NUMBER", "1"),
            self._create_token("BOOLEAN", "true"),
            self._create_token("STRING", '"hello"')
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result1 = _parse_literal(parser_state)
        self.assertEqual(result1["value"], 1)
        self.assertEqual(parser_state["pos"], 1)
        
        result2 = _parse_literal(parser_state)
        self.assertEqual(result2["value"], True)
        self.assertEqual(parser_state["pos"], 2)
        
        result3 = _parse_literal(parser_state)
        self.assertEqual(result3["value"], "hello")
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()
