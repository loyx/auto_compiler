import unittest
from unittest.mock import patch, call, MagicMock


class TestParseBlock(unittest.TestCase):
    """单元测试：_parse_block 函数"""
    
    def test_empty_block(self):
        """测试解析空块 {}"""
        # 先 patch 所有依赖，再导入被测模块
        with patch('._parse_block_src._consume_token') as mock_consume, \
             patch('._parse_block_src._parse_if_stmt') as mock_if, \
             patch('._parse_block_src._parse_while_stmt') as mock_while, \
             patch('._parse_block_src._parse_for_stmt') as mock_for, \
             patch('._parse_block_src._parse_return_stmt') as mock_return, \
             patch('._parse_block_src._parse_break_continue_stmt') as mock_break_continue, \
             patch('._parse_block_src._parse_assign_stmt') as mock_assign, \
             patch('._parse_block_src._parse_expr_stmt') as mock_expr:
            
            from ._parse_block_src import _parse_block
            
            tokens = [
                {"type": "LBRACE", "line": 1, "column": 1},
                {"type": "RBRACE", "line": 1, "column": 2}
            ]
            
            parser_state = {
                "tokens": tokens,
                "filename": "test.py",
                "pos": 0
            }
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(result["statements"], [])
            self.assertEqual(parser_state["pos"], 2)
            
            mock_consume.assert_has_calls([
                call(parser_state, "LBRACE"),
                call(parser_state, "RBRACE")
            ])
    
    def test_block_with_single_statement(self):
        """测试解析包含单个语句的块"""
        mock_return_stmt = {"type": "RETURN", "value": None, "line": 1, "column": 3}
        
        with patch('._parse_block_src._consume_token') as mock_consume, \
             patch('._parse_block_src._parse_if_stmt') as mock_if, \
             patch('._parse_block_src._parse_while_stmt') as mock_while, \
             patch('._parse_block_src._parse_for_stmt') as mock_for, \
             patch('._parse_block_src._parse_return_stmt', return_value=mock_return_stmt) as mock_return, \
             patch('._parse_block_src._parse_break_continue_stmt') as mock_break_continue, \
             patch('._parse_block_src._parse_assign_stmt') as mock_assign, \
             patch('._parse_block_src._parse_expr_stmt') as mock_expr:
            
            from ._parse_block_src import _parse_block
            
            tokens = [
                {"type": "LBRACE", "line": 1, "column": 1},
                {"type": "RETURN", "line": 1, "column": 3},
                {"type": "RBRACE", "line": 1, "column": 10}
            ]
            
            parser_state = {
                "tokens": tokens,
                "filename": "test.py",
                "pos": 0
            }
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["statements"]), 1)
            self.assertEqual(result["statements"][0]["type"], "RETURN")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_block_with_multiple_statements(self):
        """测试解析包含多个语句的块"""
        mock_return_stmt = {"type": "RETURN", "value": None, "line": 1, "column": 3}
        mock_break_stmt = {"type": "BREAK", "line": 2, "column": 1}
        
        with patch('._parse_block_src._consume_token') as mock_consume, \
             patch('._parse_block_src._parse_if_stmt') as mock_if, \
             patch('._parse_block_src._parse_while_stmt') as mock_while, \
             patch('._parse_block_src._parse_for_stmt') as mock_for, \
             patch('._parse_block_src._parse_return_stmt', return_value=mock_return_stmt) as mock_return, \
             patch('._parse_block_src._parse_break_continue_stmt', return_value=mock_break_stmt) as mock_break_continue, \
             patch('._parse_block_src._parse_assign_stmt') as mock_assign, \
             patch('._parse_block_src._parse_expr_stmt') as mock_expr:
            
            from ._parse_block_src import _parse_block
            
            tokens = [
                {"type": "LBRACE", "line": 1, "column": 1},
                {"type": "RETURN", "line": 1, "column": 3},
                {"type": "SEMICOLON", "line": 1, "column": 10},
                {"type": "BREAK", "line": 2, "column": 1},
                {"type": "SEMICOLON", "line": 2, "column": 7},
                {"type": "RBRACE", "line": 3, "column": 1}
            ]
            
            parser_state = {
                "tokens": tokens,
                "filename": "test.py",
                "pos": 0
            }
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["statements"]), 2)
            self.assertEqual(result["statements"][0]["type"], "RETURN")
            self.assertEqual(result["statements"][1]["type"], "BREAK")
            self.assertEqual(parser_state["pos"], 6)
    
    def test_block_with_semicolons(self):
        """测试解析带分号的语句块"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "SEMICOLON", "line": 1, "column": 4},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
            {"type": "SEMICOLON", "line": 1, "column": 7},
            {"type": "RBRACE", "line": 1, "column": 9}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_expr_stmt1 = {"type": "EXPR_STMT", "line": 1, "column": 3}
        mock_expr_stmt2 = {"type": "EXPR_STMT", "line": 1, "column": 6}
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt', side_effect=[mock_expr_stmt1, mock_expr_stmt2]):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["statements"]), 2)
            self.assertEqual(parser_state["pos"], 6)
    
    def test_missing_opening_brace(self):
        """测试块不以 LBRACE 开头时的错误"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Expected '{'", str(context.exception))
        self.assertIn("test.py:1:1", str(context.exception))
    
    def test_end_of_input_expected_lbrace(self):
        """测试在期望 LBRACE 时输入结束的错误"""
        from ._parse_block_src import _parse_block
        
        tokens = []
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:0:0", str(context.exception))
    
    def test_unclosed_block(self):
        """测试块未闭合时的错误"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "RETURN", "line": 1, "column": 3}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_return_stmt = {"type": "RETURN", "value": None, "line": 1, "column": 3}
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_return_stmt_package._parse_return_stmt_src._parse_return_stmt', return_value=mock_return_stmt):
            
            consume_count = [0]
            def consume_impl(ps, expected_type):
                consume_count[0] += 1
                if consume_count[0] == 1:
                    ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)
            
            self.assertIn("Unclosed block", str(context.exception))
            self.assertIn("test.py:1:1", str(context.exception))
    
    def test_block_with_if_statement(self):
        """测试块中包含 if 语句"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "IF", "line": 1, "column": 3},
            {"type": "RBRACE", "line": 2, "column": 1}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_if_stmt = {
            "type": "IF",
            "condition": {"type": "EXPR"},
            "then_block": {"type": "BLOCK", "statements": []},
            "line": 1,
            "column": 3
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_if_stmt_package._parse_if_stmt_src._parse_if_stmt', return_value=mock_if_stmt):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["statements"]), 1)
            self.assertEqual(result["statements"][0]["type"], "IF")
    
    def test_block_with_while_statement(self):
        """测试块中包含 while 语句"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "WHILE", "line": 1, "column": 3},
            {"type": "RBRACE", "line": 2, "column": 1}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_while_stmt = {
            "type": "WHILE",
            "condition": {"type": "EXPR"},
            "body": {"type": "BLOCK"},
            "line": 1,
            "column": 3
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_while_stmt_package._parse_while_stmt_src._parse_while_stmt', return_value=mock_while_stmt):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(len(result["statements"]), 1)
            self.assertEqual(result["statements"][0]["type"], "WHILE")
    
    def test_block_with_for_statement(self):
        """测试块中包含 for 语句"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "FOR", "line": 1, "column": 3},
            {"type": "RBRACE", "line": 2, "column": 1}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_for_stmt = {
            "type": "FOR",
            "initializer": {"type": "ASSIGN"},
            "condition": {"type": "EXPR"},
            "increment": {"type": "EXPR"},
            "body": {"type": "BLOCK"},
            "line": 1,
            "column": 3
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_for_stmt_package._parse_for_stmt_src._parse_for_stmt', return_value=mock_for_stmt):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(len(result["statements"]), 1)
            self.assertEqual(result["statements"][0]["type"], "FOR")
    
    def test_block_with_continue_statement(self):
        """测试块中包含 continue 语句"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "CONTINUE", "line": 1, "column": 3},
            {"type": "RBRACE", "line": 1, "column": 12}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_continue_stmt = {"type": "CONTINUE", "line": 1, "column": 3}
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_break_continue_stmt_package._parse_break_continue_stmt_src._parse_break_continue_stmt', return_value=mock_continue_stmt):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(len(result["statements"]), 1)
            self.assertEqual(result["statements"][0]["type"], "CONTINUE")
    
    def test_block_with_assign_statement(self):
        """测试块中包含赋值语句"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "ASSIGN", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 7},
            {"type": "RBRACE", "line": 1, "column": 9}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_assign_stmt = {
            "type": "ASSIGN",
            "target": {"type": "IDENTIFIER", "value": "x"},
            "value": {"type": "NUMBER", "value": "5"},
            "line": 1,
            "column": 3
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_assign_stmt_package._parse_assign_stmt_src._parse_assign_stmt', return_value=mock_assign_stmt):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(len(result["statements"]), 1)
            self.assertEqual(result["statements"][0]["type"], "ASSIGN")
    
    def test_block_position_advancement(self):
        """测试 parser_state pos 正确推进"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "RETURN", "line": 1, "column": 3},
            {"type": "RBRACE", "line": 1, "column": 10}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_return_stmt = {"type": "RETURN", "line": 1, "column": 3}
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_return_stmt_package._parse_return_stmt_src._parse_return_stmt', return_value=mock_return_stmt):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            _parse_block(parser_state)
            
            self.assertEqual(parser_state["pos"], 3)
    
    def test_block_preserves_line_column_info(self):
        """测试块保留正确的行号和列号信息"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 5, "column": 10},
            {"type": "RBRACE", "line": 5, "column": 11}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_block_statements_order(self):
        """测试块中语句顺序保持正确"""
        from ._parse_block_src import _parse_block
        
        tokens = [
            {"type": "LBRACE", "line": 1, "column": 1},
            {"type": "RETURN", "line": 1, "column": 3},
            {"type": "BREAK", "line": 2, "column": 1},
            {"type": "CONTINUE", "line": 3, "column": 1},
            {"type": "RBRACE", "line": 4, "column": 1}
        ]
        
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0
        }
        
        mock_return = {"type": "RETURN", "line": 1, "column": 3}
        mock_break = {"type": "BREAK", "line": 2, "column": 1}
        mock_continue = {"type": "CONTINUE", "line": 3, "column": 1}
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume, \
             patch('._parse_return_stmt_package._parse_return_stmt_src._parse_return_stmt', return_value=mock_return), \
             patch('._parse_break_continue_stmt_package._parse_break_continue_stmt_src._parse_break_continue_stmt', side_effect=[mock_break, mock_continue]):
            
            def consume_impl(ps, expected_type):
                ps["pos"] += 1
            
            mock_consume.side_effect = consume_impl
            
            result = _parse_block(parser_state)
            
            self.assertEqual(len(result["statements"]), 3)
            self.assertEqual(result["statements"][0]["type"], "RETURN")
            self.assertEqual(result["statements"][1]["type"], "BREAK")
            self.assertEqual(result["statements"][2]["type"], "CONTINUE")


if __name__ == "__main__":
    unittest.main()
