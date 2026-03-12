# -*- coding: utf-8 -*-
"""单元测试：_parse_expression 函数"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """_parse_expression 函数的单元测试类"""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_parse_identifier_only(self):
        """测试：仅解析标识符表达式"""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        primary_ast = {
            "type": "Identifier",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None) as mock_unary:
            with patch("._parse_expression_src._parse_primary", return_value=primary_ast) as mock_primary:
                with patch("._parse_expression_src._parse_function_call", return_value=primary_ast) as mock_func:
                    with patch("._parse_expression_src._parse_binary_op", return_value=primary_ast) as mock_binary:
                        result = _parse_expression(parser_state)
                        
                        mock_unary.assert_called_once()
                        mock_primary.assert_called_once()
                        mock_binary.assert_called_once()
                        self.assertEqual(result, primary_ast)
                        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_only(self):
        """测试：仅解析字面量表达式"""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        primary_ast = {
            "type": "Literal",
            "value": 42,
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None) as mock_unary:
            with patch("._parse_expression_src._parse_primary", return_value=primary_ast) as mock_primary:
                with patch("._parse_expression_src._parse_binary_op", return_value=primary_ast) as mock_binary:
                    result = _parse_expression(parser_state)
                    
                    self.assertEqual(result, primary_ast)

    def test_parse_unary_expression(self):
        """测试：解析一元运算符表达式"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "IDENT", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = self._create_parser_state(tokens)
        
        unary_ast = {
            "type": "UnaryOp",
            "operator": "-",
            "operand": {"type": "Identifier", "value": "x"},
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=unary_ast) as mock_unary:
            with patch("._parse_expression_src._parse_primary") as mock_primary:
                with patch("._parse_expression_src._parse_binary_op", return_value=unary_ast) as mock_binary:
                    result = _parse_expression(parser_state)
                    
                    mock_unary.assert_called_once()
                    mock_primary.assert_not_called()
                    self.assertEqual(result, unary_ast)

    def test_parse_function_call(self):
        """测试：解析函数调用表达式"""
        tokens = [
            {"type": "IDENT", "value": "func", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens)
        
        primary_ast = {
            "type": "Identifier",
            "value": "func",
            "line": 1,
            "column": 1
        }
        
        call_ast = {
            "type": "FunctionCall",
            "function": primary_ast,
            "arguments": [],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None):
            with patch("._parse_expression_src._parse_primary", return_value=primary_ast):
                with patch("._parse_expression_src._parse_function_call", return_value=call_ast) as mock_func:
                    with patch("._parse_expression_src._parse_binary_op", return_value=call_ast):
                        result = _parse_expression(parser_state)
                        
                        mock_func.assert_called_once()
                        self.assertEqual(result, call_ast)

    def test_parse_binary_expression(self):
        """测试：解析二元运算符表达式"""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens)
        
        primary_ast = {
            "type": "Literal",
            "value": 1,
            "line": 1,
            "column": 1
        }
        
        binary_ast = {
            "type": "BinaryOp",
            "operator": "+",
            "left": primary_ast,
            "right": {"type": "Literal", "value": 2},
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None):
            with patch("._parse_expression_src._parse_primary", return_value=primary_ast):
                with patch("._parse_expression_src._parse_binary_op", return_value=binary_ast) as mock_binary:
                    result = _parse_expression(parser_state)
                    
                    mock_binary.assert_called_once()
                    self.assertEqual(mock_binary.call_args[0][1], 0)
                    self.assertEqual(result, binary_ast)

    def test_parse_parenthesized_expression(self):
        """测试：解析括号表达式"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
        ]
        parser_state = self._create_parser_state(tokens)
        
        primary_ast = {
            "type": "Literal",
            "value": 42,
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None):
            with patch("._parse_expression_src._parse_primary", return_value=primary_ast):
                with patch("._parse_expression_src._parse_binary_op", return_value=primary_ast):
                    result = _parse_expression(parser_state)
                    
                    self.assertEqual(result, primary_ast)

    def test_empty_tokens_raises_error(self):
        """测试：空 token 列表抛出语法错误"""
        tokens = []
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:1:1", str(context.exception))

    def test_pos_beyond_tokens_raises_error(self):
        """测试：pos 超出 token 列表长度抛出语法错误"""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_primary_returns_none_raises_error(self):
        """测试：primary 和 unary 都返回 None 时抛出语法错误"""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None):
            with patch("._parse_expression_src._parse_primary", return_value=None):
                with self.assertRaises(SyntaxError) as context:
                    _parse_expression(parser_state)
                
                self.assertIn("Unexpected token", str(context.exception))
                self.assertIn("test.py:1:1", str(context.exception))

    def test_custom_filename_in_error(self):
        """测试：错误信息中包含自定义文件名"""
        tokens = []
        parser_state = self._create_parser_state(tokens, filename="custom.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("custom.py:1:1", str(context.exception))

    def test_nested_unary_and_binary(self):
        """测试：嵌套一元和二元运算"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 2},
            {"type": "PLUS", "value": "+", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens)
        
        unary_ast = {
            "type": "UnaryOp",
            "operator": "-",
            "operand": {"type": "Literal", "value": 5},
            "line": 1,
            "column": 1
        }
        
        binary_ast = {
            "type": "BinaryOp",
            "operator": "+",
            "left": unary_ast,
            "right": {"type": "Literal", "value": 3},
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=unary_ast):
            with patch("._parse_expression_src._parse_binary_op", return_value=binary_ast):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result, binary_ast)

    def test_function_call_with_arguments(self):
        """测试：带参数的函数调用"""
        tokens = [
            {"type": "IDENT", "value": "add", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
            {"type": "COMMA", "value": ",", "line": 1, "column": 6},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 7},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 8}
        ]
        parser_state = self._create_parser_state(tokens)
        
        func_ast = {"type": "Identifier", "value": "add", "line": 1, "column": 1}
        call_ast = {
            "type": "FunctionCall",
            "function": func_ast,
            "arguments": [
                {"type": "Literal", "value": 1},
                {"type": "Literal", "value": 2}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None):
            with patch("._parse_expression_src._parse_primary", return_value=func_ast):
                with patch("._parse_expression_src._parse_function_call", return_value=call_ast):
                    with patch("._parse_expression_src._parse_binary_op", return_value=call_ast):
                        result = _parse_expression(parser_state)
                        
                        self.assertEqual(result, call_ast)

    def test_pos_updated_after_parsing(self):
        """测试：解析后 pos 正确更新"""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        primary_ast = {"type": "Literal", "value": 42, "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_unary_op", return_value=None):
            with patch("._parse_expression_src._parse_primary", return_value=primary_ast):
                with patch("._parse_expression_src._parse_binary_op", return_value=primary_ast):
                    _parse_expression(parser_state)
                    
                    self.assertEqual(parser_state["pos"], 1)

    def test_not_operator(self):
        """测试：not 一元运算符"""
        tokens = [
            {"type": "NOT", "value": "not", "line": 1, "column": 1},
            {"type": "IDENT", "value": "flag", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens)
        
        unary_ast = {
            "type": "UnaryOp",
            "operator": "not",
            "operand": {"type": "Identifier", "value": "flag"},
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=unary_ast):
            with patch("._parse_expression_src._parse_binary_op", return_value=unary_ast):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result, unary_ast)

    def test_tilde_operator(self):
        """测试：~ 一元运算符"""
        tokens = [
            {"type": "TILDE", "value": "~", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
        ]
        parser_state = self._create_parser_state(tokens)
        
        unary_ast = {
            "type": "UnaryOp",
            "operator": "~",
            "operand": {"type": "Literal", "value": 5},
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=unary_ast):
            with patch("._parse_expression_src._parse_binary_op", return_value=unary_ast):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result, unary_ast)

    def test_complex_expression_chain(self):
        """测试：复杂表达式链（一元 + primary + 函数调用 + 二元）"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "IDENT", "value": "func", "line": 1, "column": 2},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 7},
            {"type": "STAR", "value": "*", "line": 1, "column": 9},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 11}
        ]
        parser_state = self._create_parser_state(tokens)
        
        func_ast = {"type": "Identifier", "value": "func", "line": 1, "column": 2}
        call_ast = {
            "type": "FunctionCall",
            "function": func_ast,
            "arguments": [],
            "line": 1,
            "column": 2
        }
        unary_ast = {
            "type": "UnaryOp",
            "operator": "-",
            "operand": call_ast,
            "line": 1,
            "column": 1
        }
        binary_ast = {
            "type": "BinaryOp",
            "operator": "*",
            "left": unary_ast,
            "right": {"type": "Literal", "value": 2},
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_unary_op", return_value=unary_ast):
            with patch("._parse_expression_src._parse_binary_op", return_value=binary_ast):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result, binary_ast)


if __name__ == "__main__":
    unittest.main()
