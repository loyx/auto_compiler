import unittest
from unittest.mock import patch, call

from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    
    @patch('_parse_block_package._parse_statement_package._parse_statement_src._parse_statement')
    @patch('_parse_block_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_block_package._consume_token_package._consume_token_src._consume_token')
    def test_parse_block_with_braces_multiple_statements(self, mock_consume, mock_peek, mock_parse_stmt):
        """Test parsing a block with LBRACE and RBRACE containing multiple statements"""
        # Setup: LBRACE -> stmt1 -> stmt2 -> RBRACE
        lbrace_token = {"type": "LBRACE", "line": 1, "column": 0}
        stmt1_token = {"type": "IF", "line": 2, "column": 0}
        stmt2_token = {"type": "WHILE", "line": 3, "column": 0}
        rbrace_token = {"type": "RBRACE", "line": 4, "column": 0}
        
        mock_peek.side_effect = [lbrace_token, stmt1_token, stmt2_token, rbrace_token]
        
        stmt1_ast = {"type": "IF", "line": 2, "column": 0}
        stmt2_ast = {"type": "WHILE", "line": 3, "column": 0}
        mock_parse_stmt.side_effect = [stmt1_ast, stmt2_ast]
        
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        result = _parse_block(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 0)
        self.assertEqual(len(result["statements"]), 2)
        self.assertEqual(result["statements"][0], stmt1_ast)
        self.assertEqual(result["statements"][1], stmt2_ast)
        
        # Verify consume was called for LBRACE and RBRACE
        mock_consume.assert_has_calls([
            call(parser_state, "LBRACE"),
            call(parser_state, "RBRACE")
        ])
    
    @patch('_parse_block_package._parse_statement_package._parse_statement_src._parse_statement')
    @patch('_parse_block_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_block_package._consume_token_package._consume_token_src._consume_token')
    def test_parse_block_empty(self, mock_consume, mock_peek, mock_parse_stmt):
        """Test parsing an empty block: LBRACE immediately followed by RBRACE"""
        lbrace_token = {"type": "LBRACE", "line": 1, "column": 5}
        rbrace_token = {"type": "RBRACE", "line": 1, "column": 6}
        
        mock_peek.side_effect = [lbrace_token, rbrace_token]
        
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        result = _parse_block(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["statements"], [])
        
        # Verify consume was called for LBRACE and RBRACE
        mock_consume.assert_has_calls([
            call(parser_state, "LBRACE"),
            call(parser_state, "RBRACE")
        ])
        
        # Verify parse_statement was not called
        mock_parse_stmt.assert_not_called()
    
    @patch('_parse_block_package._peek_token_package._peek_token_src._peek_token')
    def test_parse_block_eof_immediately(self, mock_peek):
        """Test parsing when EOF is encountered immediately"""
        mock_peek.return_value = None
        
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected EOF", str(context.exception))
        self.assertIn("test.py", str(context.exception))
    
    @patch('_parse_block_package._parse_statement_package._parse_statement_src._parse_statement')
    @patch('_parse_block_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_block_package._consume_token_package._consume_token_src._consume_token')
    def test_parse_block_missing_rbrace(self, mock_consume, mock_peek, mock_parse_stmt):
        """Test parsing when RBRACE is missing (EOF before RBRACE)"""
        lbrace_token = {"type": "LBRACE", "line": 1, "column": 0}
        stmt_token = {"type": "IF", "line": 2, "column": 0}
        
        # LBRACE -> stmt -> EOF (no RBRACE)
        mock_peek.side_effect = [lbrace_token, stmt_token, None]
        
        stmt_ast = {"type": "IF", "line": 2, "column": 0}
        mock_parse_stmt.return_value = stmt_ast
        
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Expected RBRACE", str(context.exception))
        self.assertIn("EOF", str(context.exception))
        
        # Verify LBRACE was consumed
        mock_consume.assert_called_with(parser_state, "LBRACE")
    
    @patch('_parse_block_package._parse_statement_package._parse_statement_src._parse_statement')
    @patch('_parse_block_package._peek_token_package._peek_token_src._peek_token')
    def test_parse_block_single_statement_no_braces(self, mock_peek, mock_parse_stmt):
        """Test parsing a single statement without braces"""
        # Non-LBRACE token (e.g., IF statement)
        if_token = {"type": "IF", "line": 5, "column": 10}
        
        mock_peek.return_value = if_token
        
        stmt_ast = {"type": "IF", "line": 5, "column": 10}
        mock_parse_stmt.return_value = stmt_ast
        
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        result = _parse_block(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(len(result["statements"]), 1)
        self.assertEqual(result["statements"][0], stmt_ast)
        
        # Verify parse_statement was called once
        mock_parse_stmt.assert_called_once_with(parser_state)
    
    @patch('_parse_block_package._parse_statement_package._parse_statement_src._parse_statement')
    @patch('_parse_block_package._peek_token_package._peek_token_src._peek_token')
    def test_parse_block_single_assignment_no_braces(self, mock_peek, mock_parse_stmt):
        """Test parsing a single ASSIGN statement without braces"""
        assign_token = {"type": "ASSIGN", "line": 10, "column": 2}
        
        mock_peek.return_value = assign_token
        
        stmt_ast = {"type": "ASSIGN", "line": 10, "column": 2}
        mock_parse_stmt.return_value = stmt_ast
        
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        result = _parse_block(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 2)
        self.assertEqual(len(result["statements"]), 1)
        self.assertEqual(result["statements"][0], stmt_ast)
    
    @patch('_parse_block_package._parse_statement_package._parse_statement_src._parse_statement')
    @patch('_parse_block_package._peek_token_package._peek_token_src._peek_token')
    @patch('_parse_block_package._consume_token_package._consume_token_src._consume_token')
    def test_parse_block_preserves_line_column_from_first_token(self, mock_consume, mock_peek, mock_parse_stmt):
        """Test that BLOCK node preserves line/column from the first token (LBRACE)"""
        lbrace_token = {"type": "LBRACE", "line": 20, "column": 15}
        stmt_token = {"type": "RETURN", "line": 21, "column": 0}
        rbrace_token = {"type": "RBRACE", "line": 22, "column": 0}
        
        mock_peek.side_effect = [lbrace_token, stmt_token, rbrace_token]
        
        stmt_ast = {"type": "RETURN", "line": 21, "column": 0}
        mock_parse_stmt.return_value = stmt_ast
        
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        result = _parse_block(parser_state)
        
        # Verify line/column come from LBRACE, not from statement
        self.assertEqual(result["line"], 20)
        self.assertEqual(result["column"], 15)


if __name__ == '__main__':
    unittest.main()
