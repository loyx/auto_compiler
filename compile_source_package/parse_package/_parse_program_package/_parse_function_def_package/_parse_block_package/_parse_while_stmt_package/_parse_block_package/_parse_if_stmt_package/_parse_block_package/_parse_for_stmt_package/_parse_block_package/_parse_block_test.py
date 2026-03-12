import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Import the function under test using relative import
from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    
    def create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.txt") -> Dict[str, Any]:
        """Helper to create a parser state dict"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def test_empty_block(self):
        """Test parsing an empty block {}"""
        tokens = [
            self.create_token("LBRACE", "{", 1, 1),
            self.create_token("RBRACE", "}", 1, 2)
        ]
        parser_state = self.create_parser_state(tokens, 0)
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["statements"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_block_with_single_statement(self):
        """Test parsing a block with one statement"""
        tokens = [
            self.create_token("LBRACE", "{", 1, 1),
            self.create_token("IDENT", "x", 1, 2),
            self.create_token("RBRACE", "}", 1, 3)
        ]
        parser_state = self.create_parser_state(tokens, 0)
        
        mock_stmt = MagicMock()
        mock_stmt.return_value = {"type": "ASSIGN", "line": 1, "column": 2}
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement", mock_stmt):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["statements"]), 1)
        self.assertEqual(result["statements"][0]["type"], "ASSIGN")
        self.assertEqual(parser_state["pos"], 2)
        mock_stmt.assert_called_once()
    
    def test_block_with_multiple_statements(self):
        """Test parsing a block with multiple statements"""
        tokens = [
            self.create_token("LBRACE", "{", 1, 1),
            self.create_token("IDENT", "x", 1, 2),
            self.create_token("IDENT", "y", 1, 3),
            self.create_token("IDENT", "z", 1, 4),
            self.create_token("RBRACE", "}", 1, 5)
        ]
        parser_state = self.create_parser_state(tokens, 0)
        
        mock_stmt = MagicMock()
        mock_stmt.side_effect = [
            {"type": "ASSIGN", "line": 1, "column": 2},
            {"type": "ASSIGN", "line": 1, "column": 3},
            {"type": "ASSIGN", "line": 1, "column": 4}
        ]
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement", mock_stmt):
            result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["statements"]), 3)
        self.assertEqual(parser_state["pos"], 4)
        self.assertEqual(mock_stmt.call_count, 3)
    
    def test_missing_lbrace(self):
        """Test error when first token is not LBRACE"""
        tokens = [
            self.create_token("IDENT", "x", 1, 1)
        ]
        parser_state = self.create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Expected '{'", str(context.exception))
    
    def test_unexpected_end_of_input(self):
        """Test error when input ends before LBRACE"""
        tokens = []
        parser_state = self.create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_position_updated_correctly(self):
        """Test that parser_state pos is updated correctly"""
        tokens = [
            self.create_token("LBRACE", "{", 1, 1),
            self.create_token("RBRACE", "}", 1, 2)
        ]
        parser_state = self.create_parser_state(tokens, 0)
        
        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_stmt:
            _parse_block(parser_state)
        
        self.assertEqual(parser_state["pos"], 2)
    
    def test_ast_structure(self):
        """Test that returned AST has correct structure"""
        tokens = [
            self.create_token("LBRACE", "{", 5, 10),
            self.create_token("RBRACE", "}", 5, 11)
        ]
        parser_state = self.create_parser_state(tokens, 0)
        
        result = _parse_block(parser_state)
        
        self.assertIn("type", result)
        self.assertIn("statements", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
