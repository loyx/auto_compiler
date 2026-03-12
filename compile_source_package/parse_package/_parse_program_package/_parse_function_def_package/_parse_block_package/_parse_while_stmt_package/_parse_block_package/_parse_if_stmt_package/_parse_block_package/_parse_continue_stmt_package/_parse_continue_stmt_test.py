import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_continue_stmt_src import _parse_continue_stmt


class TestParseContinueStmt(unittest.TestCase):
    """Test cases for _parse_continue_stmt function."""
    
    def test_parse_continue_stmt_basic(self):
        """Test parsing a basic continue statement without semicolon."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _consume_token to advance position
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_continue_stmt_package._parse_continue_stmt_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda state: {**state, "pos": state["pos"] + 1}
            
            result = _parse_continue_stmt(parser_state)
            
            self.assertEqual(result["type"], "CONTINUE")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            mock_consume.assert_called_once()
    
    def test_parse_continue_stmt_with_semicolon(self):
        """Test parsing continue statement followed by semicolon."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def consume_side_effect(state):
            call_count[0] += 1
            return {**state, "pos": state["pos"] + 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_continue_stmt_package._parse_continue_stmt_src._consume_token") as mock_consume:
            mock_consume.side_effect = consume_side_effect
            
            result = _parse_continue_stmt(parser_state)
            
            self.assertEqual(result["type"], "CONTINUE")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            self.assertEqual(mock_consume.call_count, 2)
    
    def test_parse_continue_stmt_different_position(self):
        """Test parsing continue statement at different token position."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "CONTINUE", "value": "continue", "line": 2, "column": 10},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 18}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_continue_stmt_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda state: {**state, "pos": state["pos"] + 1}
            
            result = _parse_continue_stmt(parser_state)
            
            self.assertEqual(result["type"], "CONTINUE")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 10)
    
    def test_parse_continue_stmt_no_semicolon_next_token(self):
        """Test parsing continue when next token is not semicolon."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 1, "column": 5},
                {"type": "IF", "value": "if", "line": 1, "column": 14}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_continue_stmt_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda state: {**state, "pos": state["pos"] + 1}
            
            result = _parse_continue_stmt(parser_state)
            
            self.assertEqual(result["type"], "CONTINUE")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            mock_consume.assert_called_once()
    
    def test_parse_continue_stmt_end_of_input(self):
        """Test parsing continue when pos is at or beyond token list length."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue", "line": 1, "column": 5}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        result = _parse_continue_stmt(parser_state)
        
        self.assertEqual(result["type"], "CONTINUE")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["error"], "Unexpected end of input")
    
    def test_parse_continue_stmt_empty_tokens(self):
        """Test parsing continue with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_continue_stmt(parser_state)
        
        self.assertEqual(result["type"], "CONTINUE")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["error"], "Unexpected end of input")
    
    def test_parse_continue_stmt_token_missing_line_column(self):
        """Test parsing continue when token lacks line/column info."""
        parser_state = {
            "tokens": [
                {"type": "CONTINUE", "value": "continue"}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_continue_stmt_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda state: {**state, "pos": state["pos"] + 1}
            
            result = _parse_continue_stmt(parser_state)
            
            self.assertEqual(result["type"], "CONTINUE")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)


if __name__ == "__main__":
    unittest.main()
