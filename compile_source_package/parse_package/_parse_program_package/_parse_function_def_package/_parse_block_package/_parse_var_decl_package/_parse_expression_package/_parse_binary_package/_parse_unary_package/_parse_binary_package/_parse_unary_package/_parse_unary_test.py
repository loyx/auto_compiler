"""
单元测试文件：_parse_unary 函数测试
测试目标：验证一元表达式解析器的正确行为
"""

import unittest
from unittest.mock import patch

# 相对导入被测试模块
from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """_parse_unary 函数的单元测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_minus_operator(self):
        """测试 MINUS 一元运算符解析"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 6}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        # Mock _parse_primary to return a simple identifier AST
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 6
            }

            result = _parse_unary(parser_state)

            # 验证返回的 AST 结构
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"]["operator"], "-")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)

            # 验证 pos 被正确消耗
            self.assertEqual(parser_state["pos"], 1)

            # 验证 _parse_primary 被调用
            mock_primary.assert_called_once()

    def test_plus_operator(self):
        """测试 PLUS 一元运算符解析"""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 2, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 2, "column": 4}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": "42",
                "children": [],
                "line": 2,
                "column": 4
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"]["operator"], "+")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 1)

    def test_not_operator(self):
        """测试 NOT 一元运算符解析"""
        tokens = [
            {"type": "NOT", "value": "not", "line": 3, "column": 1},
            {"type": "IDENTIFIER", "value": "flag", "line": 3, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "children": [],
                "line": 3,
                "column": 5
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"]["operator"], "not")
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 1)

    def test_bang_operator(self):
        """测试 BANG 一元运算符解析"""
        tokens = [
            {"type": "BANG", "value": "!", "line": 4, "column": 10},
            {"type": "IDENTIFIER", "value": "valid", "line": 4, "column": 11}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "valid",
                "children": [],
                "line": 4,
                "column": 11
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"]["operator"], "!")
            self.assertEqual(result["line"], 4)
            self.assertEqual(result["column"], 10)

    def test_chained_unary_operators(self):
        """测试链式一元运算符解析（如 --x）"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 5, "column": 1},
            {"type": "MINUS", "value": "-", "line": 5, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        # 需要模拟 _parse_unary 的递归调用
        # 第一次调用 _parse_primary 返回标识符
        # 第二次调用（递归）返回内层 UNARY_OP
        def primary_side_effect(state):
            # 当 pos=2 时，返回标识符 AST
            if state["pos"] == 2:
                return {
                    "type": "IDENTIFIER",
                    "value": "x",
                    "children": [],
                    "line": 5,
                    "column": 3
                }
            # 其他情况不应被调用
            raise RuntimeError("_parse_primary called at unexpected pos")

        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.side_effect = primary_side_effect

            result = _parse_unary(parser_state)

            # 外层应该是 UNARY_OP
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"]["operator"], "-")
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 1)

            # 内层也应该是 UNARY_OP
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["value"]["operator"], "-")
            self.assertEqual(inner["line"], 5)
            self.assertEqual(inner["column"], 2)

            # 最内层是标识符
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(inner["children"][0]["value"], "x")

            # pos 应该消耗了 2 个 token
            self.assertEqual(parser_state["pos"], 2)

    def test_non_unary_token_falls_to_primary(self):
        """测试非一元运算符 token 直接调用 _parse_primary"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 6, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        expected_primary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 6,
            "column": 1
        }

        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = expected_primary_result

            result = _parse_unary(parser_state)

            # 应该直接返回 _parse_primary 的结果
            self.assertEqual(result, expected_primary_result)

            # _parse_primary 应该被调用
            mock_primary.assert_called_once()

            # pos 不应该被 _parse_unary 修改（由 _parse_primary 修改）
            # 这里验证 _parse_primary 被调用了即可

    def test_empty_tokens_raises_syntax_error(self):
        """测试空 tokens 列表抛出 SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)

        # 验证错误消息包含文件名
        self.assertIn("test.c", str(context.exception))
        self.assertIn("期望表达式但遇到文件结束", str(context.exception))

    def test_pos_at_end_raises_syntax_error(self):
        """测试 pos 已到 tokens 末尾时抛出 SyntaxError"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,  # pos 已经在末尾
            "filename": "myfile.c"
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)

        self.assertIn("myfile.c", str(context.exception))
        self.assertIn("期望表达式但遇到文件结束", str(context.exception))

    def test_unknown_filename_in_error(self):
        """测试没有 filename 时使用默认值"""
        parser_state = {
            "tokens": [],
            "pos": 0
            # 没有 filename 字段
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)

        self.assertIn("<unknown>", str(context.exception))

    def test_ast_children_structure(self):
        """测试 AST 节点的 children 结构正确"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 7, "column": 1},
            {"type": "NUMBER", "value": "100", "line": 7, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": "100",
                "children": [],
                "line": 7,
                "column": 2
            }

            result = _parse_unary(parser_state)

            # 验证 children 是列表且包含一个元素
            self.assertIsInstance(result["children"], list)
            self.assertEqual(len(result["children"]), 1)

            # 验证 children[0] 是 _parse_primary 返回的结果
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(result["children"][0]["value"], "100")

    def test_pos_mutation_side_effect(self):
        """测试 parser_state['pos'] 的副作用修改"""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 8, "column": 1},
            {"type": "IDENTIFIER", "value": "y", "line": 8, "column": 2},
            {"type": "SEMICOLON", "value": ";", "line": 8, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }

        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "y",
                "children": [],
                "line": 8,
                "column": 2
            }

            initial_pos = parser_state["pos"]
            result = _parse_unary(parser_state)
            final_pos = parser_state["pos"]

            # 验证 pos 从 0 变为 1（消耗了 PLUS token）
            self.assertEqual(initial_pos, 0)
            self.assertEqual(final_pos, 1)


if __name__ == "__main__":
    unittest.main()
