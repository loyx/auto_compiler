# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of target module ===
from ._extract_literal_value_src import _extract_literal_value

# === ADT defines ===
Token = Dict[str, Any]


class TestExtractLiteralValue(unittest.TestCase):
    """测试 _extract_literal_value 函数的各种场景"""

    def test_number_integer_no_decimal(self):
        """测试整数 NUMBER token（不含小数点）"""
        token: Token = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, 42)
        self.assertIsInstance(result, int)

    def test_number_integer_zero(self):
        """测试零值 NUMBER token"""
        token: Token = {"type": "NUMBER", "value": "0", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, 0)
        self.assertIsInstance(result, int)

    def test_number_integer_negative(self):
        """测试负整数 NUMBER token"""
        token: Token = {"type": "NUMBER", "value": "-123", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, -123)
        self.assertIsInstance(result, int)

    def test_number_float_with_decimal(self):
        """测试浮点数 NUMBER token（含小数点）"""
        token: Token = {"type": "NUMBER", "value": "3.14", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, 3.14)
        self.assertIsInstance(result, float)

    def test_number_float_zero_decimal(self):
        """测试零值浮点数 NUMBER token"""
        token: Token = {"type": "NUMBER", "value": "0.0", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, 0.0)
        self.assertIsInstance(result, float)

    def test_number_float_negative(self):
        """测试负浮点数 NUMBER token"""
        token: Token = {"type": "NUMBER", "value": "-2.5", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, -2.5)
        self.assertIsInstance(result, float)

    def test_number_float_scientific_notation(self):
        """测试科学计数法 NUMBER token"""
        token: Token = {"type": "NUMBER", "value": "1e10", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        # 科学计数法不含 '.'，应返回 int，但 int("1e10") 会失败
        # 实际行为由实现决定，这里测试当前实现
        self.assertEqual(result, 10000000000.0)
        self.assertIsInstance(result, float)

    def test_string_double_quotes(self):
        """测试双引号 STRING token"""
        token: Token = {"type": "STRING", "value": '"hello"', "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, "hello")
        self.assertIsInstance(result, str)

    def test_string_single_quotes(self):
        """测试单引号 STRING token"""
        token: Token = {"type": "STRING", "value": "'world'", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, "world")
        self.assertIsInstance(result, str)

    def test_string_empty_double_quotes(self):
        """测试空字符串（双引号）"""
        token: Token = {"type": "STRING", "value": '""', "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, "")
        self.assertIsInstance(result, str)

    def test_string_empty_single_quotes(self):
        """测试空字符串（单引号）"""
        token: Token = {"type": "STRING", "value": "''", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, "")
        self.assertIsInstance(result, str)

    def test_string_with_spaces(self):
        """测试包含空格的 STRING token"""
        token: Token = {"type": "STRING", "value": '"hello world"', "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, "hello world")
        self.assertIsInstance(result, str)

    def test_string_mismatched_quotes(self):
        """测试引号不匹配的 STRING token（应返回原值）"""
        token: Token = {"type": "STRING", "value": '"hello\'', "line": 1, "column": 1}
        result = _extract_literal_value(token)
        # 首尾引号不匹配，应返回原值
        self.assertEqual(result, '"hello\'')

    def test_string_no_quotes(self):
        """测试无引号的 STRING token（应返回原值）"""
        token: Token = {"type": "STRING", "value": "hello", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        # 无引号，应返回原值
        self.assertEqual(result, "hello")

    def test_string_single_char(self):
        """测试单字符 STRING token（无引号）"""
        token: Token = {"type": "STRING", "value": "a", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        # 长度不足 2，应返回原值
        self.assertEqual(result, "a")

    def test_unknown_token_type(self):
        """测试未知类型的 token（应返回原值）"""
        token: Token = {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, "foo")

    def test_token_missing_type(self):
        """测试缺少 type 字段的 token"""
        token: Token = {"value": "42", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        # type 为空字符串，应返回原值
        self.assertEqual(result, "42")

    def test_token_missing_value(self):
        """测试缺少 value 字段的 token"""
        token: Token = {"type": "NUMBER", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        # value 为空字符串，应返回空字符串
        self.assertEqual(result, "")

    def test_token_empty_dict(self):
        """测试空 token 字典"""
        token: Token = {}
        result = _extract_literal_value(token)
        # type 和 value 都为空，应返回空字符串
        self.assertEqual(result, "")

    def test_number_large_integer(self):
        """测试大整数 NUMBER token"""
        token: Token = {"type": "NUMBER", "value": "999999999999", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertEqual(result, 999999999999)
        self.assertIsInstance(result, int)

    def test_number_float_many_decimals(self):
        """测试多位小数的 NUMBER token"""
        token: Token = {"type": "NUMBER", "value": "3.14159265358979", "line": 1, "column": 1}
        result = _extract_literal_value(token)
        self.assertAlmostEqual(result, 3.14159265358979)
        self.assertIsInstance(result, float)


if __name__ == "__main__":
    unittest.main()
