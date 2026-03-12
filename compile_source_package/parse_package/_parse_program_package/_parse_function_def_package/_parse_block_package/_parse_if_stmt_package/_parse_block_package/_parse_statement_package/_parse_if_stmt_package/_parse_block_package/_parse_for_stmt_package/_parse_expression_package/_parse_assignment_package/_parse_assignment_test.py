# -*- coding: utf-8 -*-
"""单元测试：_parse_assignment 函数"""

import unittest
from unittest.mock import patch, MagicMock
import sys

# Mock all dependencies before importing _parse_assignment_src
# This prevents import errors from the long dependency chain

# Create a mock for _parse_conditional that will be used in tests
mock_parse_conditional = MagicMock()
mock_parse_conditional.__name__ = "_parse_conditional"

# Create mock modules for the entire dependency chain
mock_conditional_module = MagicMock()
mock_conditional_module._parse_conditional = mock_parse_conditional

# Pre-register mock modules in sys.modules to prevent actual imports
# The module paths are relative to the test module's package
base_package = __package__  # This is the package of the test module

# Register the _parse_conditional_package._parse_conditional_src module
conditional_module_path = f"{base_package}._parse_conditional_package._parse_conditional_src"
sys.modules[conditional_module_path] = mock_conditional_module

# Also register the parent package
conditional_package_path = f"{base_package}._parse_conditional_package"
if conditional_package_path not in sys.modules:
    sys.modules[conditional_package_path] = MagicMock()

# Now import _parse_assignment_src (it will use our mock for _parse_conditional)
from ._parse_assignment_src import _parse_assignment
# Also import the module itself so we can patch it
from . import _parse_assignment_src as _parse_assignment_src_module


class TestParseAssignment(unittest.TestCase):
    """测试 _parse_assignment 函数的各种场景"""

    def test_simple_assignment(self):
        """测试简单赋值：a = b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        # Mock _parse_conditional 返回左侧表达式
        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_right = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            side_effect=[mock_left, mock_right],
        ) as mock_conditional:
            result = _parse_assignment(parser_state)

        self.assertEqual(result["type"], "ASSIGNMENT")
        self.assertEqual(result["operator"], "=")
        self.assertEqual(result["left"], mock_left)
        self.assertEqual(result["right"], mock_right)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 3)  # pos 应该前进到 token 末尾

    def test_compound_assignment_plus(self):
        """测试复合赋值：a += b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 1},
            {"type": "OPERATOR", "value": "+=", "line": 2, "column": 3},
            {"type": "NUMBER", "value": "5", "line": 2, "column": 6},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 1}
        mock_right = {"type": "NUMBER", "value": "5", "line": 2, "column": 6}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            side_effect=[mock_left, mock_right],
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result["type"], "ASSIGNMENT")
        self.assertEqual(result["operator"], "+=")
        self.assertEqual(result["left"], mock_left)
        self.assertEqual(result["right"], mock_right)
        self.assertEqual(parser_state["pos"], 3)

    def test_compound_assignment_minus(self):
        """测试复合赋值：a -= b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "-=", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_right = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            side_effect=[mock_left, mock_right],
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result["operator"], "-=")

    def test_compound_assignment_multiply(self):
        """测试复合赋值：a *= b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "*=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_right = {"type": "NUMBER", "value": "2", "line": 1, "column": 6}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            side_effect=[mock_left, mock_right],
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result["operator"], "*=")

    def test_compound_assignment_divide(self):
        """测试复合赋值：a /= b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "/=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_right = {"type": "NUMBER", "value": "2", "line": 1, "column": 6}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            side_effect=[mock_left, mock_right],
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result["operator"], "/=")

    def test_compound_assignment_modulo(self):
        """测试复合赋值：a %= b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "%=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_right = {"type": "NUMBER", "value": "3", "line": 1, "column": 6}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            side_effect=[mock_left, mock_right],
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result["operator"], "%=")

    def test_chained_assignment(self):
        """测试连续赋值（右结合）：a = b = c，应解析为 a = (b = c)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        # 模拟三次 _parse_conditional 调用：a, b, c
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            side_effect=[mock_a, mock_b, mock_c],
        ) as mock_conditional:
            result = _parse_assignment(parser_state)

        # 验证右结合：a = (b = c)
        self.assertEqual(result["type"], "ASSIGNMENT")
        self.assertEqual(result["operator"], "=")
        self.assertEqual(result["left"], mock_a)

        # right 应该是一个 ASSIGNMENT 节点：b = c
        self.assertEqual(result["right"]["type"], "ASSIGNMENT")
        self.assertEqual(result["right"]["operator"], "=")
        self.assertEqual(result["right"]["left"], mock_b)
        self.assertEqual(result["right"]["right"], mock_c)

        # pos 应该前进到末尾
        self.assertEqual(parser_state["pos"], 5)

    def test_no_assignment_operator(self):
        """测试没有赋值运算符的情况：直接返回左侧表达式"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            return_value=mock_left,
        ) as mock_conditional:
            result = _parse_assignment(parser_state)

        # 应该直接返回左侧表达式，不是 ASSIGNMENT 节点
        self.assertEqual(result, mock_left)
        # pos 不应该改变（只调用了一次 _parse_conditional）
        self.assertEqual(parser_state["pos"], 0)
        # _parse_conditional 只被调用了一次
        mock_conditional.assert_called_once()

    def test_empty_tokens(self):
        """测试空 tokens 列表"""
        tokens = []
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "LITERAL", "value": "42", "line": 1, "column": 1}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            return_value=mock_left,
        ):
            result = _parse_assignment(parser_state)

        # 应该直接返回左侧表达式
        self.assertEqual(result, mock_left)
        self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end_of_tokens(self):
        """测试 pos 已经在 tokens 末尾的情况"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 1}

        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}

        with patch.object(
            _parse_assignment_src_module,
            "_parse_conditional",
            return_value=mock_left,
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result, mock_left)

    def test_assignment_with_complex_left_expression(self):
        """测试左侧是复杂表达式的情况（由 _parse_conditional 返回）"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "[", "line": 1, "column": 2},
            {"type": "OPERATOR", "value": "]", "line": 1, "column": 3},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 7},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        # 模拟 _parse_conditional 返回一个复杂的左值表达式
        mock_left = {
            "type": "SUBSCRIPT",
            "value": "a",
            "index": {"type": "LITERAL", "value": "0"},
            "line": 1,
            "column": 1,
        }
        mock_right = {"type": "LITERAL", "value": "10", "line": 1, "column": 7}

        with patch(
            "._parse_assignment_src._parse_conditional",
            side_effect=[mock_left, mock_right],
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result["type"], "ASSIGNMENT")
        self.assertEqual(result["operator"], "=")
        self.assertEqual(result["left"]["type"], "SUBSCRIPT")
        self.assertEqual(result["right"], mock_right)

    def test_line_column_preserved_from_left(self):
        """测试 AST 节点的 line 和 column 来自左侧表达式"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10},
            {"type": "OPERATOR", "value": "=", "line": 5, "column": 12},
            {"type": "NUMBER", "value": "100", "line": 5, "column": 14},
        ]
        parser_state = {"tokens": tokens, "filename": "test.py", "pos": 0}

        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10}
        mock_right = {"type": "NUMBER", "value": "100", "line": 5, "column": 14}

        with patch(
            "._parse_assignment_src._parse_conditional",
            side_effect=[mock_left, mock_right],
        ):
            result = _parse_assignment(parser_state)

        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
