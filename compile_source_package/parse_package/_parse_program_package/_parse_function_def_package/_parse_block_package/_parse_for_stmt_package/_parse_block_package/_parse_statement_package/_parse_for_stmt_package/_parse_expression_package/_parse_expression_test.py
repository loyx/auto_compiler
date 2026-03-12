import unittest
from unittest.mock import patch

# Relative imports for the function under test
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""

    def test_number_literal(self):
        """测试数字字面量表达式"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 5}],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "LITERAL",
            "value": 42,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 5)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LITERAL")
                self.assertEqual(result["value"], 42)
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 5)

    def test_string_literal(self):
        """测试字符串字面量表达式"""
        parser_state = {
            "tokens": [{"type": "STRING", "value": "hello", "line": 2, "column": 10}],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "LITERAL",
            "value": "hello",
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(2, 10)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LITERAL")
                self.assertEqual(result["value"], "hello")
                self.assertEqual(result["line"], 2)
                self.assertEqual(result["column"], 10)

    def test_identifier(self):
        """测试标识符表达式"""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "IDENTIFIER")
                self.assertEqual(result["value"], "x")
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)

    def test_binary_operation(self):
        """测试二元运算表达式"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2}
            ]
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], "+")
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                self.assertEqual(len(result["children"]), 2)

    def test_unary_operation(self):
        """测试一元运算表达式"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "UNARY_OP",
            "value": "-",
            "children": [
                {"type": "LITERAL", "value": 5}
            ]
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "UNARY_OP")
                self.assertEqual(result["value"], "-")
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                self.assertEqual(len(result["children"]), 1)

    def test_syntax_error_propagation(self):
        """测试语法错误传播"""
        parser_state = {
            "tokens": [{"type": "OPERATOR", "value": "+", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", side_effect=SyntaxError("Invalid expression at line 1")):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                with self.assertRaises(SyntaxError) as context:
                    _parse_expression(parser_state)
                
                self.assertIn("Invalid expression", str(context.exception))

    def test_empty_tokens(self):
        """测试空 token 列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "LITERAL",
            "value": None,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(0, 0)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LITERAL")
                self.assertEqual(result["value"], None)
                self.assertEqual(result["line"], 0)
                self.assertEqual(result["column"], 0)

    def test_boolean_true(self):
        """测试布尔值 true"""
        parser_state = {
            "tokens": [{"type": "TRUE", "value": "true", "line": 3, "column": 5}],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "LITERAL",
            "value": True,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(3, 5)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LITERAL")
                self.assertEqual(result["value"], True)
                self.assertEqual(result["line"], 3)
                self.assertEqual(result["column"], 5)

    def test_boolean_false(self):
        """测试布尔值 false"""
        parser_state = {
            "tokens": [{"type": "FALSE", "value": "false", "line": 4, "column": 7}],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "LITERAL",
            "value": False,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(4, 7)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LITERAL")
                self.assertEqual(result["value"], False)
                self.assertEqual(result["line"], 4)
                self.assertEqual(result["column"], 7)

    def test_nested_expression(self):
        """测试嵌套表达式"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2}
            ]
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], "+")
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)

    def test_pos_modified_by_parse_or_expr(self):
        """测试 pos 由_parse_or_expr 修改"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "LITERAL",
            "value": 42,
            "children": []
        }
        
        def mock_parse_or_expr(state):
            state["pos"] = 1  # _parse_or_expr 会修改 pos
            return mock_ast
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", side_effect=mock_parse_or_expr):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                result = _parse_expression(parser_state)
                
                # pos 应该被修改（由_parse_or_expr 修改）
                self.assertEqual(parser_state["pos"], 1)
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)

    def test_float_literal(self):
        """测试浮点数字面量"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "3.14", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "LITERAL",
            "value": 3.14,
            "children": []
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "LITERAL")
                self.assertEqual(result["value"], 3.14)
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)

    def test_complex_expression(self):
        """测试复杂表达式（逻辑运算）"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "and", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        mock_ast = {
            "type": "BINARY_OP",
            "value": "and",
            "children": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "IDENTIFIER", "value": "b"}
            ]
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr", return_value=mock_ast):
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_expression_package._get_current_position_package._get_current_position_src._get_current_position", return_value=(1, 1)):
                result = _parse_expression(parser_state)
                
                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], "and")
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)


if __name__ == '__main__':
    unittest.main()
