"""单元测试：_parse_block 函数"""

import unittest
from unittest.mock import patch

from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """_parse_block 函数测试用例"""

    def test_empty_block(self):
        """测试空块：{}"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_single_statement(self):
        """测试块中包含单个语句"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "BREAK", "value": "break", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_stmt_node = {"type": "BREAK_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_stmt_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_stmt_node)
        self.assertEqual(parser_state["pos"], 3)

    def test_block_with_multiple_statements(self):
        """测试块中包含多个语句"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "BREAK", "value": "break", "line": 2, "column": 2},
            {"type": "CONTINUE", "value": "continue", "line": 3, "column": 2},
            {"type": "RETURN", "value": "return", "line": 4, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_break_node = {"type": "BREAK_STMT", "line": 2, "column": 2}
        mock_continue_node = {"type": "CONTINUE_STMT", "line": 3, "column": 2}
        mock_return_node = {"type": "RETURN_STMT", "line": 4, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = [
                (mock_break_node, 2),
                (mock_continue_node, 3),
                (mock_return_node, 4),
            ]
            
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], mock_break_node)
        self.assertEqual(result["children"][1], mock_continue_node)
        self.assertEqual(result["children"][2], mock_return_node)
        self.assertEqual(parser_state["pos"], 5)

    def test_missing_lbrace_raises_syntax_error(self):
        """测试缺少左花括号时抛出 SyntaxError"""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Expected '{'", str(context.exception))
        self.assertIn("test.src", str(context.exception))

    def test_missing_rbrace_raises_syntax_error(self):
        """测试缺少右花括号时抛出 SyntaxError"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "BREAK", "value": "break", "line": 1, "column": 3},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_stmt_node = {"type": "BREAK_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_stmt_node, 1)
            
            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)
        
        self.assertIn("Expected '}'", str(context.exception))
        self.assertIn("test.src", str(context.exception))

    def test_empty_tokens_raises_syntax_error(self):
        """测试空 tokens 列表时抛出 SyntaxError"""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Expected '{'", str(context.exception))
        self.assertIn("EOF", str(context.exception))

    def test_parser_state_pos_updated_correctly(self):
        """测试 parser_state 的 pos 被正确更新"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "BREAK", "value": "break", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_stmt_node = {"type": "BREAK_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_stmt_node, 2)
            
            _parse_block(parser_state)
        
        self.assertEqual(parser_state["pos"], 3)

    def test_block_start_position_recorded(self):
        """测试块的起始位置被正确记录"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "LBRACE", "value": "{", "line": 5, "column": 10},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 11},
        ]
        parser_state = {"tokens": tokens, "pos": 1, "filename": "test.src"}
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_statement_dispatch_for_if(self):
        """测试 IF 语句的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IF", "value": "if", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_if_node = {"type": "IF_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_if_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "IF_STMT")

    def test_statement_dispatch_for_while(self):
        """测试 WHILE 语句的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "WHILE", "value": "while", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_while_node = {"type": "WHILE_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_while_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "WHILE_STMT")

    def test_statement_dispatch_for_for(self):
        """测试 FOR 语句的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "FOR", "value": "for", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 7},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_for_node = {"type": "FOR_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_for_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "FOR_STMT")

    def test_statement_dispatch_for_return(self):
        """测试 RETURN 语句的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RETURN", "value": "return", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_return_node = {"type": "RETURN_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_return_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "RETURN_STMT")

    def test_statement_dispatch_for_break(self):
        """测试 BREAK 语句的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "BREAK", "value": "break", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_break_node = {"type": "BREAK_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_break_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "BREAK_STMT")

    def test_statement_dispatch_for_continue(self):
        """测试 CONTINUE 语句的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "CONTINUE", "value": "continue", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 12},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_continue_node = {"type": "CONTINUE_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_continue_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "CONTINUE_STMT")

    def test_statement_dispatch_for_var_decl(self):
        """测试变量声明的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "INT", "value": "int", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_var_decl_node = {"type": "VAR_DECL", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_var_decl_node, 3)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "VAR_DECL")

    def test_statement_dispatch_for_expr_stmt(self):
        """测试表达式语句的分发"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.src"}
        
        mock_expr_stmt_node = {"type": "EXPR_STMT", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = (mock_expr_stmt_node, 2)
            
            result = _parse_block(parser_state)
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "EXPR_STMT")

    def test_filename_in_error_message(self):
        """测试错误消息中包含文件名"""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 10, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "my_program.src"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("my_program.src", str(context.exception))
        self.assertIn("10", str(context.exception))
        self.assertIn("5", str(context.exception))

    def test_default_filename_when_not_provided(self):
        """测试未提供文件名时使用默认值"""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("<unknown>", str(context.exception))


if __name__ == "__main__":
    unittest.main()
