import unittest

# Relative import from the same package
from ._parse_break_stmt_src import _parse_break_stmt


class TestParseBreakStmt(unittest.TestCase):
    """Test cases for _parse_break_stmt function."""
    
    def test_valid_break_stmt(self):
        """Test parsing valid break; statement."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_break_stmt(parser_state)
        
        # Verify AST node structure
        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        
        # Verify parser_state pos was advanced by 2 (BREAK + SEMICOLON)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_missing_semicolon_error(self):
        """Test error when semicolon is missing after break."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)
        
        self.assertIn("expected ';'", str(context.exception))
        self.assertIn("test.c:1:5", str(context.exception))
    
    def test_wrong_token_after_break_error(self):
        """Test error when wrong token follows break."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 10}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)
        
        self.assertIn("expected ';'", str(context.exception))
        self.assertIn("got 'x'", str(context.exception))
    
    def test_ast_node_structure(self):
        """Test AST node has correct structure with different line/column."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 3, "column": 15},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 20}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "example.c"
        }
        
        result = _parse_break_stmt(parser_state)
        
        # Verify all required fields exist
        self.assertIn("type", result)
        self.assertIn("children", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        
        # Verify values
        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 15)
    
    def test_pos_advancement(self):
        """Test that parser_state pos is correctly advanced."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 15}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_break_stmt(parser_state)
        
        # pos should advance from 0 to 2 (consume BREAK and SEMICOLON)
        self.assertEqual(parser_state["pos"], 2)
        
        # Verify the AST node is still correct
        self.assertEqual(result["type"], "BREAK_STMT")
    
    def test_break_at_end_of_file_with_semicolon(self):
        """Test break; at the very end of token stream."""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 5, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 6}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "end.c"
        }
        
        result = _parse_break_stmt(parser_state)
        
        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_break_with_different_token_types_after(self):
        """Test error with various wrong token types after break."""
        wrong_tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 10},
            {"type": "STRING", "value": "\"hello\"", "line": 1, "column": 10},
            {"type": "KEYWORD", "value": "if", "line": 1, "column": 10},
        ]
        
        for wrong_token in wrong_tokens:
            tokens = [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5},
                wrong_token
            ]
            parser_state = {
                "tokens": tokens,
                "pos": 0,
                "filename": "test.c"
            }
            
            with self.assertRaises(SyntaxError) as context:
                _parse_break_stmt(parser_state)
            
            self.assertIn("expected ';'", str(context.exception))


if __name__ == "__main__":
    unittest.main()
