import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """单元测试：_parse_block 函数"""
    
    def test_empty_block(self):
        """测试空块 {}"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_block_with_single_statement(self):
        """测试包含单个语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "VAR", "value": "var", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_var_decl = {
            "type": "VAR_DECL",
            "line": 2,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_var_decl_stmt_package._parse_var_decl_stmt_src._parse_var_decl_stmt", return_value=mock_var_decl):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "VAR_DECL")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_block_with_multiple_statements(self):
        """测试包含多个不同类型语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "VAR", "value": "var", "line": 2, "column": 1},
            {"type": "IF", "value": "if", "line": 3, "column": 1},
            {"type": "RETURN", "value": "return", "line": 4, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_var_decl = {"type": "VAR_DECL", "line": 2, "column": 1}
        mock_if_stmt = {"type": "IF", "line": 3, "column": 1}
        mock_return_stmt = {"type": "RETURN", "line": 4, "column": 1}
        
        def mock_dispatch(parser_state):
            token = parser_state["tokens"][parser_state["pos"]]
            if token["type"] == "VAR":
                return mock_var_decl
            elif token["type"] == "IF":
                return mock_if_stmt
            elif token["type"] == "RETURN":
                return mock_return_stmt
            return {"type": "UNKNOWN"}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_var_decl_stmt_package._parse_var_decl_stmt_src._parse_var_decl_stmt", side_effect=mock_dispatch), \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_if_stmt", side_effect=mock_dispatch), \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_return_stmt", side_effect=mock_dispatch):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0]["type"], "VAR_DECL")
        self.assertEqual(result["children"][1]["type"], "IF")
        self.assertEqual(result["children"][2]["type"], "RETURN")
        self.assertEqual(parser_state["pos"], 5)
    
    def test_nested_blocks(self):
        """测试嵌套块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "LBRACE", "value": "{", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        inner_block = {
            "type": "BLOCK",
            "children": [],
            "line": 2,
            "column": 1
        }
        
        call_count = [0]
        
        def mock_parse_block(parser_state):
            call_count[0] += 1
            if call_count[0] == 1:
                parser_state["pos"] = 3
                return inner_block
            else:
                return {"type": "BLOCK", "children": [inner_block], "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_block_src._parse_block", side_effect=mock_parse_block):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "BLOCK")
        self.assertEqual(parser_state["pos"], 4)
    
    def test_missing_rbrace_eof(self):
        """测试缺少 RBRACE（遇到 EOF）"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "VAR", "value": "var", "line": 2, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_var_decl = {"type": "VAR_DECL", "line": 2, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_var_decl_stmt_package._parse_var_decl_stmt_src._parse_var_decl_stmt", return_value=mock_var_decl):
            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)
            
            self.assertIn("未找到 RBRACE", str(context.exception))
            self.assertIn("test.c:1:1", str(context.exception))
    
    def test_block_with_for_statement(self):
        """测试包含 FOR 语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "FOR", "value": "for", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_for_stmt = {
            "type": "FOR",
            "line": 2,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_for_stmt_package._parse_for_stmt_src._parse_for_stmt", return_value=mock_for_stmt):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "FOR")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_block_with_while_statement(self):
        """测试包含 WHILE 语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "WHILE", "value": "while", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_while_stmt = {
            "type": "WHILE",
            "line": 2,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_while_stmt", return_value=mock_while_stmt):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "WHILE")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_block_with_break_statement(self):
        """测试包含 BREAK 语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "BREAK", "value": "break", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_break_stmt = {
            "type": "BREAK",
            "line": 2,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_break_stmt_package._parse_break_stmt_src._parse_break_stmt", return_value=mock_break_stmt):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "BREAK")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_block_with_continue_statement(self):
        """测试包含 CONTINUE 语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "CONTINUE", "value": "continue", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_continue_stmt = {
            "type": "CONTINUE",
            "line": 2,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_continue_stmt_package._parse_continue_stmt_src._parse_continue_stmt", return_value=mock_continue_stmt):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "CONTINUE")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_block_with_expression_statement(self):
        """测试包含表达式语句的块（未知 token type 走表达式语句路径）"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_stmt = {
            "type": "EXPRESSION_STMT",
            "line": 2,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_expression_stmt_package._parse_expression_stmt_src._parse_expression_stmt", return_value=mock_expr_stmt):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "EXPRESSION_STMT")
        self.assertEqual(parser_state["pos"], 3)
    
    def test_block_position_tracking(self):
        """测试 BLOCK AST 的 line/column 来自 LBRACE token"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 10, "column": 5},
            {"type": "RBRACE", "value": "}", "line": 10, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)


if __name__ == "__main__":
    unittest.main()
