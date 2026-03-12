import unittest
from unittest.mock import patch, MagicMock, call

from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """Test cases for _parse_block function."""
    
    def test_empty_block(self):
        """Test parsing an empty block {}."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            self.assertEqual(mock_consume.call_count, 2)
            mock_consume.assert_has_calls([
                call(parser_state, "LBRACE"),
                call(parser_state, "RBRACE")
            ])
    
    def test_block_with_single_statement(self):
        """Test parsing a block with one statement { stmt; }."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "IDENT", "value": "x", "line": 1, "column": 3},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        statement_ast = {"type": "ASSIGN", "line": 1, "column": 3}
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENT", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement', return_value=statement_ast):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], statement_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
    
    def test_block_with_multiple_statements(self):
        """Test parsing a block with multiple statements { stmt1; stmt2; stmt3; }."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "IDENT", "value": "x", "line": 1, "column": 3},
                {"type": "IDENT", "value": "y", "line": 2, "column": 1},
                {"type": "IDENT", "value": "z", "line": 3, "column": 1},
                {"type": "RBRACE", "value": "}", "line": 3, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        stmt1 = {"type": "ASSIGN", "value": "x", "line": 1, "column": 3}
        stmt2 = {"type": "ASSIGN", "value": "y", "line": 2, "column": 1}
        stmt3 = {"type": "ASSIGN", "value": "z", "line": 3, "column": 1}
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENT", "value": "x", "line": 1, "column": 3},
            {"type": "IDENT", "value": "y", "line": 2, "column": 1},
            {"type": "IDENT", "value": "z", "line": 3, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 3}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        mock_parse_stmt = MagicMock()
        mock_parse_stmt.side_effect = [stmt1, stmt2, stmt3]
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement', mock_parse_stmt):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["children"]), 3)
            self.assertEqual(result["children"], [stmt1, stmt2, stmt3])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
    
    def test_nested_blocks(self):
        """Test parsing nested blocks { { } }."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 3},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        inner_block = {"type": "BLOCK", "children": [], "line": 1, "column": 3}
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 7}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        mock_parse_stmt = MagicMock()
        mock_parse_stmt.return_value = inner_block
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement', mock_parse_stmt):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], inner_block)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
    
    def test_block_position_from_lbrace(self):
        """Test that BLOCK node position comes from LBRACE token."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 5, "column": 10},
                {"type": "RBRACE", "value": "}", "line": 5, "column": 11}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 5, "column": 10},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 11}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_consume_token_called_with_correct_types(self):
        """Test that _consume_token is called with LBRACE and RBRACE."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume):
            
            _parse_block(parser_state)
            
            self.assertEqual(mock_consume.call_count, 2)
            calls = mock_consume.call_args_list
            self.assertEqual(calls[0][0], (parser_state, "LBRACE"))
            self.assertEqual(calls[1][0], (parser_state, "RBRACE"))
    
    def test_peek_token_called_multiple_times(self):
        """Test that _peek_token is called for each iteration."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "IDENT", "value": "x", "line": 1, "column": 3},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENT", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement'):
            
            _parse_block(parser_state)
            
            self.assertEqual(mock_peek.call_count, 3)
    
    def test_parse_statement_called_for_each_statement(self):
        """Test that _parse_statement is called once per statement."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "IDENT", "value": "x", "line": 1, "column": 3},
                {"type": "IDENT", "value": "y", "line": 2, "column": 1},
                {"type": "RBRACE", "value": "}", "line": 2, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_peek = MagicMock()
        mock_peek.side_effect = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENT", "value": "x", "line": 1, "column": 3},
            {"type": "IDENT", "value": "y", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 2, "column": 3}
        ]
        
        mock_consume = MagicMock()
        mock_consume.side_effect = [parser_state, parser_state]
        
        mock_parse_stmt = MagicMock()
        mock_parse_stmt.side_effect = [
            {"type": "ASSIGN", "value": "x"},
            {"type": "ASSIGN", "value": "y"}
        ]
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._peek_token_package._peek_token_src._peek_token', mock_peek), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._consume_token', mock_consume), \
             patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement', mock_parse_stmt):
            
            _parse_block(parser_state)
            
            self.assertEqual(mock_parse_stmt.call_count, 2)


if __name__ == "__main__":
    unittest.main()
