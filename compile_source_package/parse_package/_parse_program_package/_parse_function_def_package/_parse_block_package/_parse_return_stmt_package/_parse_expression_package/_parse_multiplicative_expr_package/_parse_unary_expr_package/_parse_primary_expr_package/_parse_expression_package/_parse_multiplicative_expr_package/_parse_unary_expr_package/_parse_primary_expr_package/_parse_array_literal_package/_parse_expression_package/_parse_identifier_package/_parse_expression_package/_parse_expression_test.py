"""单元测试：_parse_expression 函数"""
import unittest
from unittest.mock import patch

# 相对导入被测模块
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """_parse_expression 函数的单元测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_parse_number_literal(self):
        """测试解析 NUMBER 类型 token"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "NUMBER_LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])

    def test_parse_string_literal(self):
        """测试解析 STRING 类型 token"""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "STRING_LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])

    @patch('._parse_expression_src._parse_identifier')
    def test_parse_identifier_delegates(self, mock_parse_identifier):
        """测试解析 IDENTIFIER 类型 token 委托给 _parse_identifier"""
        mock_ast = {
            "type": "IDENTIFIER_REF",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 1
        }
        mock_parse_identifier.return_value = mock_ast
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        mock_parse_identifier.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_ast)

    @patch('._parse_expression_src._parse_paren_expression')
    def test_parse_left_paren_delegates(self, mock_parse_paren):
        """测试解析 LEFT_PAREN 类型 token 委托给 _parse_paren_expression"""
        mock_ast = {
            "type": "PAREN_EXPR",
            "value": None,
            "children": [],
            "line": 1,
            "column": 1
        }
        mock_parse_paren.return_value = mock_ast
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        mock_parse_paren.assert_called_once_with(parser_state)
        self.assertEqual(result, mock_ast)

    def test_parse_plus_operator(self):
        """测试解析 PLUS 运算符"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    def test_parse_minus_operator(self):
        """测试解析 MINUS 运算符"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "-")

    def test_parse_star_operator(self):
        """测试解析 STAR 运算符"""
        parser_state = {
            "tokens": [
                {"type": "STAR", "value": "*", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "*")

    def test_parse_slash_operator(self):
        """测试解析 SLASH 运算符"""
        parser_state = {
            "tokens": [
                {"type": "SLASH", "value": "/", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "/")

    def test_parse_percent_operator(self):
        """测试解析 PERCENT 运算符"""
        parser_state = {
            "tokens": [
                {"type": "PERCENT", "value": "%", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "%")

    def test_parse_eq_operator(self):
        """测试解析 EQ 运算符"""
        parser_state = {
            "tokens": [
                {"type": "EQ", "value": "==", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "==")

    def test_parse_ne_operator(self):
        """测试解析 NE 运算符"""
        parser_state = {
            "tokens": [
                {"type": "NE", "value": "!=", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "!=")

    def test_parse_lt_operator(self):
        """测试解析 LT 运算符"""
        parser_state = {
            "tokens": [
                {"type": "LT", "value": "<", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "<")

    def test_parse_gt_operator(self):
        """测试解析 GT 运算符"""
        parser_state = {
            "tokens": [
                {"type": "GT", "value": ">", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], ">")

    def test_parse_le_operator(self):
        """测试解析 LE 运算符"""
        parser_state = {
            "tokens": [
                {"type": "LE", "value": "<=", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "<=")

    def test_parse_ge_operator(self):
        """测试解析 GE 运算符"""
        parser_state = {
            "tokens": [
                {"type": "GE", "value": ">=", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], ">=")

    def test_parse_and_operator(self):
        """测试解析 AND 运算符"""
        parser_state = {
            "tokens": [
                {"type": "AND", "value": "&&", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "&&")

    def test_parse_or_operator(self):
        """测试解析 OR 运算符"""
        parser_state = {
            "tokens": [
                {"type": "OR", "value": "||", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "||")

    def test_parse_empty_tokens_boundary(self):
        """测试边界情况：tokens 为空列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertEqual(parser_state["error"], "Unexpected end of expression")

    def test_parse_pos_out_of_bounds(self):
        """测试边界情况：pos 超出 tokens 长度"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertEqual(parser_state["error"], "Unexpected end of expression")

    def test_parse_pos_at_boundary(self):
        """测试边界情况：pos 等于 tokens 长度"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)

    def test_parse_unknown_token_type(self):
        """测试未知 token 类型返回 ERROR"""
        parser_state = {
            "tokens": [
                {"type": "UNKNOWN_TYPE", "value": "???", "line": 3, "column": 7}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "???")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertIn("Unexpected token type: UNKNOWN_TYPE", parser_state["error"])

    def test_parse_missing_token_fields(self):
        """测试 token 缺少某些字段时的默认值处理"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER"}  # 缺少 value, line, column
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "NUMBER_LITERAL")
        self.assertEqual(result["value"], "")  # 默认值
        self.assertEqual(result["line"], 0)  # 默认值
        self.assertEqual(result["column"], 0)  # 默认值

    def test_parse_missing_parser_state_fields(self):
        """测试 parser_state 缺少某些字段时的默认值处理"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "100", "line": 1, "column": 1}
            ]
            # 缺少 pos, filename, error
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "NUMBER_LITERAL")
        self.assertEqual(result["value"], "100")

    def test_parse_at_non_zero_position(self):
        """测试在非零位置解析表达式"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 1,  # 从第二个 token 开始
            "filename": "test.cc",
            "error": ""
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    def test_parse_preserves_other_parser_state_fields(self):
        """测试解析后保留 parser_state 的其他字段"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        _parse_expression(parser_state)
        
        self.assertEqual(parser_state["filename"], "test.cc")
        self.assertEqual(parser_state["pos"], 0)  # pos 不应被修改


if __name__ == "__main__":
    unittest.main()
