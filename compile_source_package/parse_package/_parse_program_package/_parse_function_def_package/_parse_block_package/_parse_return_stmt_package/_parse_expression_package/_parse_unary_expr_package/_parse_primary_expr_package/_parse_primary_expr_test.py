# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# === relative imports ===
from ._parse_primary_expr_src import _parse_primary_expr
from ._create_error_node_package._create_error_node_src import _create_error_node

# === Type Aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParsePrimaryExpr(unittest.TestCase):
    """测试 _parse_primary_expr 函数的各种场景。"""

    def test_parse_identifier(self):
        """测试解析标识符。"""
        tokens = [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_parse_number_int(self):
        """测试解析整数。"""
        tokens = [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_float(self):
        """测试解析浮点数。"""
        tokens = [{"type": "NUMBER", "value": "3.14", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string(self):
        """测试解析字符串字面量。"""
        tokens = [{"type": "STRING", "value": "hello", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_true(self):
        """测试解析 TRUE 关键字。"""
        tokens = [{"type": "TRUE", "value": "true", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertTrue(result["value"])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_false(self):
        """测试解析 FALSE 关键字。"""
        tokens = [{"type": "FALSE", "value": "false", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertFalse(result["value"])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null(self):
        """测试解析 NULL 关键字。"""
        tokens = [{"type": "NULL", "value": "null", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(parser_state["pos"], 1)

    @patch.object(_parse_unary_expr, '__module__', _parse_unary_expr.__module__)
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_parse_paren_expr_valid(self, mock_parse_unary):
        """测试解析有效的括号表达式。"""
        inner_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        mock_parse_unary.return_value = inner_ast
        
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], inner_ast)
        self.assertEqual(parser_state["pos"], 3)
        self.assertNotIn("error", parser_state)
        mock_parse_unary.assert_called_once()

    def test_empty_tokens(self):
        """测试空 token 列表（位置超出范围）。"""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        with patch.object(_create_error_node, '__module__', _create_error_node.__module__):
            with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_unary_expr_package._parse_primary_expr_package._create_error_node_package._create_error_node_src._create_error_node') as mock_create_error:
                mock_create_error.return_value = {"type": "ERROR", "value": "error", "line": 0, "column": 0, "children": []}
                
                result = _parse_primary_expr(parser_state)
                
                self.assertEqual(result["type"], "ERROR")
                self.assertIn("error", parser_state)
                self.assertEqual(parser_state["error"], "Unexpected end of input")
                mock_create_error.assert_called_once()

    def test_unknown_token_type(self):
        """测试未知 token 类型。"""
        tokens = [{"type": "PLUS", "value": "+", "line": 1, "column": 1}]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch.object(_create_error_node, '__module__', _create_error_node.__module__):
            with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_unary_expr_package._parse_primary_expr_package._create_error_node_package._create_error_node_src._create_error_node') as mock_create_error:
                mock_create_error.return_value = {"type": "ERROR", "value": "error", "line": 1, "column": 1, "children": []}
                
                result = _parse_primary_expr(parser_state)
                
                self.assertEqual(result["type"], "ERROR")
                self.assertIn("error", parser_state)
                self.assertIn("Unexpected token: PLUS", parser_state["error"])
                mock_create_error.assert_called_once()

    @patch.object(_parse_unary_expr, '__module__', _parse_unary_expr.__module__)
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_missing_rparen(self, mock_parse_unary):
        """测试缺少右括号的情况。"""
        inner_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        mock_parse_unary.return_value = inner_ast
        
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(len(result["children"]), 1)
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["error"], "Missing closing parenthesis")

    @patch.object(_parse_unary_expr, '__module__', _parse_unary_expr.__module__)
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_wrong_token_after_inner_expr(self, mock_parse_unary):
        """测试括号内表达式后遇到非 RPAREN 的 token。"""
        inner_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        mock_parse_unary.return_value = inner_ast
        
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(len(result["children"]), 1)
        self.assertIn("error", parser_state)
        self.assertIn("Expected RPAREN, got PLUS", parser_state["error"])


if __name__ == "__main__":
    unittest.main()
