import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_return_statement_src import _parse_return_statement


Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseReturnStatement(unittest.TestCase):
    """单元测试 _parse_return_statement 函数"""
    
    def test_return_with_expression(self):
        """测试带表达式的 return 语句：return x;"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 8}
        ]
        
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_ast: AST = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 7
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_return_statement_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_expr_ast
            
            result = _parse_return_statement(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_expr_ast)
        self.assertEqual(parser_state["pos"], 3)
    
    def test_return_without_expression(self):
        """测试不带表达式的 return 语句：return;"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 2, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 11}
        ]
        
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_return_statement(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 0)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_missing_semicolon_after_expression(self):
        """测试缺少分号的情况：return x (无分号)"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7}
        ]
        
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_ast: AST = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 7
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_return_statement_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_return_statement(parser_state)
            
            self.assertEqual(str(context.exception), "Expected ';' after return statement")
    
    def test_missing_semicolon_no_expression(self):
        """测试缺少分号且无表达式的情况：return (无分号，无表达式)"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1}
        ]
        
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_statement(parser_state)
        
        self.assertEqual(str(context.exception), "Expected ';' after return statement")
    
    def test_parse_expression_called_with_correct_state(self):
        """测试 _parse_expression 被正确调用"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 8},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
        ]
        
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_ast: AST = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 8
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_return_statement_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_expr_ast
            
            _parse_return_statement(parser_state)
            
            mock_parse_expr.assert_called_once()
            called_state = mock_parse_expr.call_args[0][0]
            self.assertEqual(called_state["pos"], 1)
            self.assertEqual(called_state["tokens"], tokens)
    
    def test_return_at_end_of_file_no_semicolon(self):
        """测试 return 在文件末尾且无分号"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 10, "column": 1}
        ]
        
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_statement(parser_state)
        
        self.assertEqual(str(context.exception), "Expected ';' after return statement")
    
    def test_complex_expression_mock(self):
        """测试复杂表达式场景（mock 返回复杂 AST）"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 5, "column": 3},
            {"type": "IDENTIFIER", "value": "func", "line": 5, "column": 10},
            {"type": "LPAREN", "value": "(", "line": 5, "column": 14},
            {"type": "NUMBER", "value": "1", "line": 5, "column": 15},
            {"type": "RPAREN", "value": ")", "line": 5, "column": 16},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 17}
        ]
        
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_expr_ast: AST = {
            "type": "CALL_EXPR",
            "children": [
                {"type": "IDENTIFIER", "value": "func", "line": 5, "column": 10},
                {"type": "NUMBER", "value": "1", "line": 5, "column": 15}
            ],
            "line": 5,
            "column": 10
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_return_statement_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 5}) or mock_expr_ast
            
            result = _parse_return_statement(parser_state)
        
        self.assertEqual(result["type"], "RETURN_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "CALL_EXPR")
        self.assertEqual(parser_state["pos"], 6)


if __name__ == "__main__":
    unittest.main()
