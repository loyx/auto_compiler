# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_expression_src import _parse_expression

# === ADT type aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseExpression(unittest.TestCase):
    """单元测试：_parse_expression 函数"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.mock_ast: AST = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": {"type": "number", "value": 2},
            "line": 1,
            "column": 0
        }

    def test_happy_path_simple_expression(self):
        """测试：简单表达式解析成功"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch("._parse_expression_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = self.mock_ast

            result = _parse_expression(parser_state)

            mock_parse_logical.assert_called_once_with(parser_state)
            self.assertEqual(result, self.mock_ast)

    def test_happy_path_complex_expression(self):
        """测试：复杂表达式（含逻辑运算符）解析成功"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
                {"type": "AND", "value": "and", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
            ],
            "filename": "test.py",
            "pos": 0
        }

        expected_ast: AST = {
            "type": "logical_op",
            "operator": "and",
            "left": {"type": "identifier", "value": "x"},
            "right": {"type": "identifier", "value": "y"},
            "line": 1,
            "column": 0
        }

        with patch("._parse_expression_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = expected_ast

            result = _parse_expression(parser_state)

            mock_parse_logical.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_happy_path_nested_expression(self):
        """测试：嵌套表达式解析成功"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 0},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
                {"type": "STAR", "value": "*", "line": 1, "column": 8},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 10}
            ],
            "filename": "test.py",
            "pos": 0
        }

        expected_ast: AST = {
            "type": "binary_op",
            "operator": "*",
            "left": {
                "type": "binary_op",
                "operator": "+",
                "left": {"type": "number", "value": 1},
                "right": {"type": "number", "value": 2}
            },
            "right": {"type": "number", "value": 3},
            "line": 1,
            "column": 0
        }

        with patch("._parse_expression_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = expected_ast

            result = _parse_expression(parser_state)

            mock_parse_logical.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_boundary_empty_tokens(self):
        """测试：边界值 - 空 tokens 列表"""
        parser_state: ParserState = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0
        }

        expected_ast: AST = {
            "type": "empty",
            "line": 0,
            "column": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = expected_ast

            result = _parse_expression(parser_state)

            mock_parse_logical.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_boundary_single_token(self):
        """测试：边界值 - 单个 token（字面量）"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        expected_ast: AST = {
            "type": "number",
            "value": 42,
            "line": 1,
            "column": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = expected_ast

            result = _parse_expression(parser_state)

            mock_parse_logical.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_boundary_pos_at_end(self):
        """测试：边界值 - pos 已在 tokens 末尾"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 1
        }

        expected_ast: AST = {
            "type": "empty",
            "line": 0,
            "column": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = expected_ast

            result = _parse_expression(parser_state)

            mock_parse_logical.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_error_syntax_error_propagation(self):
        """测试：非法输入 - 语法错误从 _parse_logical 传播"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.side_effect = SyntaxError("test.py:1:0: Unexpected token '+'")

            with self.assertRaises(SyntaxError) as context:
                _parse_expression(parser_state)

            self.assertIn("Unexpected token '+'", str(context.exception))
            mock_parse_logical.assert_called_once_with(parser_state)

    def test_error_unexpected_end_of_input(self):
        """测试：非法输入 - 意外的输入结束"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.side_effect = SyntaxError("test.py:1:2: Unexpected end of input")

            with self.assertRaises(SyntaxError) as context:
                _parse_expression(parser_state)

            self.assertIn("Unexpected end of input", str(context.exception))
            mock_parse_logical.assert_called_once_with(parser_state)

    def test_state_modification_pos_updated(self):
        """测试：副作用 - parser_state['pos'] 被正确更新"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4}
            ],
            "filename": "test.py",
            "pos": 0
        }

        def update_pos(state: ParserState) -> AST:
            state["pos"] = 3  # 模拟解析后 pos 移动到末尾
            return self.mock_ast

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.side_effect = update_pos

            result = _parse_expression(parser_state)

            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(result, self.mock_ast)

    def test_delegation_only_no_additional_logic(self):
        """测试：验证 _parse_expression 仅委托给 _parse_logical，无额外逻辑"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = {"type": "identifier", "value": "x"}

            _parse_expression(parser_state)

            # 验证只调用了一次 _parse_logical，且传入的是原始 parser_state
            mock_parse_logical.assert_called_once()
            call_args = mock_parse_logical.call_args
            self.assertIs(call_args[0][0], parser_state)

    def test_multiple_expression_types(self):
        """测试：多种表达式类型的解析"""
        test_cases = [
            {
                "name": "布尔表达式",
                "tokens": [
                    {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
                    {"type": "OR", "value": "or", "line": 1, "column": 2},
                    {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
                ],
                "expected_type": "logical_op"
            },
            {
                "name": "比较表达式",
                "tokens": [
                    {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                    {"type": "LESS_THAN", "value": "<", "line": 1, "column": 2},
                    {"type": "NUMBER", "value": "2", "line": 1, "column": 4}
                ],
                "expected_type": "comparison_op"
            },
            {
                "name": "一元表达式",
                "tokens": [
                    {"type": "MINUS", "value": "-", "line": 1, "column": 0},
                    {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
                ],
                "expected_type": "unary_op"
            }
        ]

        for case in test_cases:
            with self.subTest(case=case["name"]):
                parser_state: ParserState = {
                    "tokens": case["tokens"],
                    "filename": "test.py",
                    "pos": 0
                }

                expected_ast: AST = {
                    "type": case["expected_type"],
                    "line": 1,
                    "column": 0
                }

                with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
                    mock_parse_logical.return_value = expected_ast

                    result = _parse_expression(parser_state)

                    mock_parse_logical.assert_called_once_with(parser_state)
                    self.assertEqual(result["type"], case["expected_type"])

    def test_filename_in_parser_state(self):
        """测试：parser_state 中包含 filename 字段"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0}
            ],
            "filename": "src/main.py",
            "pos": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = {"type": "number", "value": 1}

            _parse_expression(parser_state)

            mock_parse_logical.assert_called_once()
            called_state = mock_parse_logical.call_args[0][0]
            self.assertEqual(called_state["filename"], "src/main.py")

    def test_return_value_is_dict(self):
        """测试：返回值类型为 dict"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch("._parse_logical_package._parse_logical_src._parse_logical") as mock_parse_logical:
            mock_parse_logical.return_value = {"type": "string", "value": "hello"}

            result = _parse_expression(parser_state)

            self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main()
