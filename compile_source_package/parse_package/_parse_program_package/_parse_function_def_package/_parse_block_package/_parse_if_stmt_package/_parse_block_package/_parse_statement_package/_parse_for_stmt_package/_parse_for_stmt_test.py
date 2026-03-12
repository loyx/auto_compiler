import unittest
from unittest.mock import patch

from ._parse_for_stmt_src import _parse_for_stmt


class TestParseForStmt(unittest.TestCase):
    """单元测试：_parse_for_stmt 函数"""
    
    def test_complete_for_loop(self):
        """测试完整 for 循环：for (i = 0; i < 10; i++) { }"""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 6},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 8},
            {"type": "NUMBER", "value": "0", "line": 1, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11},
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 13},
            {"type": "LT", "value": "<", "line": 1, "column": 15},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 17},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 19},
            {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 21},
            {"type": "INCREMENT", "value": "++", "line": 1, "column": 23},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 25},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 27},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 28},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        init_ast = {"type": "ASSIGN_EXPR", "line": 1, "column": 6}
        cond_ast = {"type": "COMPARE_EXPR", "line": 1, "column": 13}
        update_ast = {"type": "INCREMENT_EXPR", "line": 1, "column": 21}
        body_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 27}
        
        with patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_expression') as mock_parse_expr, \
             patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_block') as mock_parse_block:
            
            mock_parse_expr.side_effect = [init_ast, cond_ast, update_ast]
            mock_parse_block.return_value = body_ast
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR_STMT")
            self.assertEqual(len(result["children"]), 4)
            self.assertEqual(result["children"][0], init_ast)
            self.assertEqual(result["children"][1], cond_ast)
            self.assertEqual(result["children"][2], update_ast)
            self.assertEqual(result["children"][3], body_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            self.assertEqual(mock_parse_expr.call_count, 3)
            mock_parse_block.assert_called_once()
            self.assertEqual(parser_state["pos"], 15)
    
    def test_empty_for_loop(self):
        """测试空 for 循环：for (;;) { }"""
        tokens = [
            {"type": "FOR", "value": "for", "line": 5, "column": 10},
            {"type": "LPAREN", "value": "(", "line": 5, "column": 14},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 15},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 17},
            {"type": "RPAREN", "value": ")", "line": 5, "column": 18},
            {"type": "LBRACE", "value": "{", "line": 5, "column": 20},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 21},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        body_ast = {"type": "BLOCK", "children": [], "line": 5, "column": 20}
        
        with patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_expression') as mock_parse_expr, \
             patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_block') as mock_parse_block:
            
            mock_parse_expr.return_value = None
            mock_parse_block.return_value = body_ast
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR_STMT")
            self.assertEqual(len(result["children"]), 4)
            self.assertIsNone(result["children"][0])
            self.assertIsNone(result["children"][1])
            self.assertIsNone(result["children"][2])
            self.assertEqual(result["children"][3], body_ast)
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
            
            self.assertEqual(mock_parse_expr.call_count, 3)
            self.assertEqual(parser_state["pos"], 7)
    
    def test_partial_for_loop_only_condition(self):
        """测试部分 for 循环：for (; i < 10; ) { }"""
        tokens = [
            {"type": "FOR", "value": "for", "line": 3, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 3, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 6},
            {"type": "IDENTIFIER", "value": "i", "line": 3, "column": 8},
            {"type": "LT", "value": "<", "line": 3, "column": 10},
            {"type": "NUMBER", "value": "10", "line": 3, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 14},
            {"type": "RPAREN", "value": ")", "line": 3, "column": 16},
            {"type": "LBRACE", "value": "{", "line": 3, "column": 18},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 19},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        cond_ast = {"type": "COMPARE_EXPR", "line": 3, "column": 8}
        body_ast = {"type": "BLOCK", "children": [], "line": 3, "column": 18}
        
        with patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_expression') as mock_parse_expr, \
             patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_block') as mock_parse_block:
            
            mock_parse_expr.side_effect = [None, cond_ast, None]
            mock_parse_block.return_value = body_ast
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR_STMT")
            self.assertIsNone(result["children"][0])
            self.assertEqual(result["children"][1], cond_ast)
            self.assertIsNone(result["children"][2])
            self.assertEqual(result["children"][3], body_ast)
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 1)
    
    def test_unexpected_eof_after_for(self):
        """测试错误：FOR 后文件结束"""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Unexpected end of file", str(context.exception))
        self.assertIn("test.c", str(context.exception))
    
    def test_wrong_token_type_after_for(self):
        """测试错误：FOR 后不是 LPAREN"""
        tokens = [
            {"type": "FOR", "value": "for", "line": 2, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 9},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "error.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected 'LPAREN'", str(context.exception))
        self.assertIn("error.c:2:9", str(context.exception))
        self.assertIn("found 'IDENTIFIER'", str(context.exception))
    
    def test_position_advancement(self):
        """测试 parser_state["pos"] 正确推进"""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 11},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 12},
            {"type": "IDENTIFIER", "value": "next", "line": 1, "column": 14},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        body_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 11}
        
        with patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_expression') as mock_parse_expr, \
             patch('compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_src._parse_block') as mock_parse_block:
            
            mock_parse_expr.return_value = None
            mock_parse_block.return_value = body_ast
            
            _parse_for_stmt(parser_state)
            
            self.assertEqual(parser_state["pos"], 7)


if __name__ == "__main__":
    unittest.main()
