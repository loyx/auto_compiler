# === imports ===
import unittest
from ._parse_string_value_src import _parse_string_value


# === test cases ===
class TestParseStringValue(unittest.TestCase):
    """测试 _parse_string_value 函数的单元测试"""

    def test_double_quoted_string(self):
        """测试双引号字符串：'"hello"' -> 'hello'"""
        result = _parse_string_value('"hello"')
        self.assertEqual(result, 'hello')

    def test_single_quoted_string(self):
        """测试单引号字符串："'world'" -> 'world'"""
        result = _parse_string_value("'world'")
        self.assertEqual(result, 'world')

    def test_empty_string(self):
        """测试空字符串：'' -> ''"""
        result = _parse_string_value('')
        self.assertEqual(result, '')

    def test_single_character(self):
        """测试单字符：'a' -> 'a'"""
        result = _parse_string_value('a')
        self.assertEqual(result, 'a')

    def test_two_double_quotes(self):
        """测试两个双引号：'""' -> ''"""
        result = _parse_string_value('""')
        self.assertEqual(result, '')

    def test_two_single_quotes(self):
        """测试两个单引号："''" -> ''"""
        result = _parse_string_value("''")
        self.assertEqual(result, '')

    def test_string_without_quotes(self):
        """测试无引号字符串：'hello' -> 'ell'（去除首尾字符）"""
        result = _parse_string_value('hello')
        self.assertEqual(result, 'ell')

    def test_mixed_quotes(self):
        """测试混合引号：'"hello' -> 'hell'（去除首尾字符）"""
        result = _parse_string_value('"hello')
        self.assertEqual(result, 'hell')

    def test_long_string_with_quotes(self):
        """测试长字符串：'"this is a long string"' -> 'this is a long string'"""
        result = _parse_string_value('"this is a long string"')
        self.assertEqual(result, 'this is a long string')

    def test_string_with_spaces(self):
        """测试带空格的字符串：'"hello world"' -> 'hello world'"""
        result = _parse_string_value('"hello world"')
        self.assertEqual(result, 'hello world')

    def test_special_characters_inside(self):
        """测试内部特殊字符：'"hello\\nworld"' -> 'hello\\nworld'"""
        result = _parse_string_value('"hello\\nworld"')
        self.assertEqual(result, 'hello\\nworld')


# === main entry ===
if __name__ == '__main__':
    unittest.main()
