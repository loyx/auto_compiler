import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._parse_break_stmt_src import _parse_break_stmt

Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseBreakStmt(unittest.TestCase):
    """Test cases for _parse_break_stmt function"""
    
    def test_parse_break_stmt_happy_path_with_semicolon(self):
        """Test parsing break statement with semicolon"""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_break_stmt_src._consume_token') as mock_consume:
            mock_consume.side_effect = [
                {"tokens": parser_state["tokens"], "pos": 1, "filename": "test.py"},
                {"tokens": parser_state["tokens"], "pos": 2, "filename": "test.py"}
            ]
            
            result = _parse_break_stmt(parser_state)
            
            self.assertEqual(result["type"], "BREAK")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            self.assertEqual(mock_consume.call_count, 2)
    
    def test_parse_break_stmt_without_semicolon(self):
        """Test parsing break statement without semicolon"""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_break_stmt_src._consume_token') as mock_consume:
            mock_consume.return_value = {
                "tokens": parser_state["tokens"],
                "pos": 1,
                "filename": "test.py"
            }
            
            result = _parse_break_stmt(parser_state)
            
            self.assertEqual(result["type"], "BREAK")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            mock_consume.assert_called_once()
    
    def test_parse_break_stmt_error_case(self):
        """Test parsing break statement when consume_token fails"""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.return_value = {
                "tokens": parser_state["tokens"],
                "pos": 0,
                "filename": "test.py",
                "error": "Expected BREAK token"
            }
            
            result = _parse_break_stmt(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["value"], "Expected BREAK token")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
    
    def test_parse_break_stmt_empty_tokens(self):
        """Test parsing break statement with empty tokens list"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.return_value = {
                "tokens": [],
                "pos": 0,
                "filename": "test.py"
            }
            
            result = _parse_break_stmt(parser_state)
            
            self.assertEqual(result["type"], "BREAK")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)
    
    def test_parse_break_stmt_pos_out_of_bounds(self):
        """Test parsing break statement when pos is out of bounds"""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.return_value = {
                "tokens": parser_state["tokens"],
                "pos": 5,
                "filename": "test.py"
            }
            
            result = _parse_break_stmt(parser_state)
            
            self.assertEqual(result["type"], "BREAK")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)
    
    def test_parse_break_stmt_different_position(self):
        """Test parsing break statement at different position in token stream"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "BREAK", "value": "break", "line": 2, "column": 3},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 8}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = [
                {"tokens": parser_state["tokens"], "pos": 2, "filename": "test.py"},
                {"tokens": parser_state["tokens"], "pos": 3, "filename": "test.py"}
            ]
            
            result = _parse_break_stmt(parser_state)
            
            self.assertEqual(result["type"], "BREAK")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 3)
            self.assertEqual(mock_consume.call_count, 2)
    
    def test_parse_break_stmt_consume_token_called_with_correct_args(self):
        """Test that _consume_token is called with correct arguments"""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.return_value = {
                "tokens": parser_state["tokens"],
                "pos": 1,
                "filename": "test.py"
            }
            
            _parse_break_stmt(parser_state)
            
            mock_consume.assert_called_once_with(parser_state, "BREAK")
    
    def test_parse_break_stmt_multiple_semicolons(self):
        """Test parsing break statement - only first semicolon is consumed"""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            mock_consume.side_effect = [
                {"tokens": parser_state["tokens"], "pos": 1, "filename": "test.py"},
                {"tokens": parser_state["tokens"], "pos": 2, "filename": "test.py"}
            ]
            
            result = _parse_break_stmt(parser_state)
            
            self.assertEqual(result["type"], "BREAK")
            self.assertEqual(mock_consume.call_count, 2)


if __name__ == '__main__':
    unittest.main()
