# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === sub function imports ===
from ._parse_literal_src import _parse_literal


# === Test Helper Functions ===
def create_parser_state(
    tokens: list,
    pos: int = 0,
    filename: str = "test.src"
) -> Dict[str, Any]:
    """创建 ParserState 用于测试"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def create_token(
    token_type: str,
    value: str,
    line: int = 1,
    column: int = 1
) -> Dict[str, Any]:
    """创建 Token 用于测试"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


# === Test Cases ===
class TestParseLiteral(unittest.TestCase):
    """测试 _parse_literal 函数"""

    def test_parse_string_literal(self):
        """测试 STRING 类型字面量解析"""
        token = create_token("STRING", "hello world", line=1, column=5)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])
        # 验证 pos 已前进
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_literal_int(self):
        """测试 NUMBER 类型字面量解析（整数）"""
        token = create_token("NUMBER", "42", line=2, column=10)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_literal_float(self):
        """测试 NUMBER 类型字面量解析（浮点数）"""
        token = create_token("NUMBER", "3.14159", line=3, column=1)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], 3.14159)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_literal_negative(self):
        """测试 NUMBER 类型字面量解析（负数）"""
        token = create_token("NUMBER", "-100", line=1, column=1)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], -100)
        self.assertIsInstance(result["value"], int)

    def test_parse_number_literal_negative_float(self):
        """测试 NUMBER 类型字面量解析（负浮点数）"""
        token = create_token("NUMBER", "-2.5", line=1, column=1)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], -2.5)
        self.assertIsInstance(result["value"], float)

    def test_parse_boolean_literal_true(self):
        """测试 BOOLEAN 类型字面量解析（true）"""
        token = create_token("BOOLEAN", "true", line=5, column=20)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], True)
        self.assertIsInstance(result["value"], bool)
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 20)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_boolean_literal_false(self):
        """测试 BOOLEAN 类型字面量解析（false）"""
        token = create_token("BOOLEAN", "false", line=6, column=15)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], False)
        self.assertIsInstance(result["value"], bool)
        self.assertEqual(result["line"], 6)
        self.assertEqual(result["column"], 15)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_literal(self):
        """测试 NULL 类型字面量解析"""
        token = create_token("NULL", "null", line=7, column=8)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 7)
        self.assertEqual(result["column"], 8)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_with_multiple_tokens(self):
        """测试在多个 token 中解析字面量（pos 不为 0）"""
        tokens = [
            create_token("STRING", "first", line=1, column=1),
            create_token("NUMBER", "123", line=1, column=10),
            create_token("BOOLEAN", "true", line=1, column=15)
        ]
        parser_state = create_parser_state(tokens, pos=1)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], 123)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_literal_pos_out_of_bounds(self):
        """测试 pos 越界错误"""
        tokens = [create_token("STRING", "test", line=1, column=1)]
        parser_state = create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.src", str(context.exception))

    def test_parse_literal_empty_tokens(self):
        """测试空 tokens 列表"""
        parser_state = create_parser_state([], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_literal_invalid_token_type(self):
        """测试无效 token 类型错误"""
        token = create_token("IDENTIFIER", "myVar", line=10, column=5)
        parser_state = create_parser_state([token], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_literal(parser_state)
        
        self.assertIn("Expected literal token", str(context.exception))
        self.assertIn("IDENTIFIER", str(context.exception))
        self.assertIn("line 10", str(context.exception))
        self.assertIn("column 5", str(context.exception))

    def test_parse_literal_invalid_number_format(self):
        """测试无效数字格式错误"""
        token = create_token("NUMBER", "abc123", line=4, column=7)
        parser_state = create_parser_state([token], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_literal(parser_state)
        
        self.assertIn("Invalid number format", str(context.exception))
        self.assertIn("abc123", str(context.exception))
        self.assertIn("line 4", str(context.exception))
        self.assertIn("column 7", str(context.exception))

    def test_parse_literal_invalid_boolean_value(self):
        """测试无效布尔值错误"""
        token = create_token("BOOLEAN", "TRUE", line=8, column=12)
        parser_state = create_parser_state([token], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_literal(parser_state)
        
        self.assertIn("Invalid boolean value", str(context.exception))
        self.assertIn("TRUE", str(context.exception))
        self.assertIn("Expected 'true' or 'false'", str(context.exception))

    def test_parse_literal_custom_filename(self):
        """测试自定义文件名在错误信息中"""
        token = create_token("NUMBER", "invalid", line=1, column=1)
        parser_state = create_parser_state([token], pos=0, filename="my_script.cc")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_literal(parser_state)
        
        self.assertIn("my_script.cc", str(context.exception))

    def test_parse_literal_scientific_notation(self):
        """测试科学计数法数字"""
        token = create_token("NUMBER", "1.5e10", line=1, column=1)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], 1.5e10)
        self.assertIsInstance(result["value"], float)

    def test_parse_literal_zero(self):
        """测试零值"""
        token = create_token("NUMBER", "0", line=1, column=1)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["value"], 0)
        self.assertIsInstance(result["value"], int)

    def test_parse_literal_empty_string(self):
        """测试空字符串"""
        token = create_token("STRING", "", line=1, column=1)
        parser_state = create_parser_state([token], pos=0)
        
        result = _parse_literal(parser_state)
        
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)


# === Main Entry ===
if __name__ == "__main__":
    unittest.main()
