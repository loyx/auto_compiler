# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_src import _parse_unary_expr


# === Test Helper Types ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


# === Test Cases ===
class TestParseUnaryExpr(unittest.TestCase):
    """Test cases for _parse_unary_expr function."""

    def test_parse_unary_minus_simple(self):
        """Test parsing a simple unary minus expression: -x"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_unary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_unary_not_simple(self):
        """Test parsing a simple logical NOT expression: !x"""
        tokens = [
            {"type": "NOT", "value": "!", "line": 2, "column": 5},
            {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_unary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "flag",
                "line": 2,
                "column": 6
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_unary_empty_tokens(self):
        """Test parsing when tokens list is empty"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_unary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertIn("error", parser_state)
        self.assertIn("Unexpected end of input", parser_state["error"])

    def test_parse_unary_pos_at_end(self):
        """Test parsing when position is at the end of tokens"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        
        result = _parse_unary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertIn("error", parser_state)

    def test_parse_unary_delegates_to_primary(self):
        """Test that non-unary tokens are delegated to _parse_primary_expr"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        expected_ast = {
            "type": "IDENTIFIER",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch('._parse_unary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = expected_ast
            
            result = _parse_unary_expr(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
            self.assertEqual(parser_state["pos"], 0)

    def test_parse_unary_delegates_literal(self):
        """Test delegation for LITERAL token"""
        tokens = [
            {"type": "LITERAL", "value": "42", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_unary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "children": [],
                "value": "42",
                "line": 1,
                "column": 1
            }
            
            result = _parse_unary_expr(parser_state)
            
            mock_primary.assert_called_once()
            self.assertEqual(result["type"], "LITERAL")

    def test_parse_unary_delegates_lparen(self):
        """Test delegation for LPAREN token (parenthesized expression)"""
        tokens = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_unary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "PAREN_EXPR",
                "children": [],
                "value": None,
                "line": 1,
                "column": 1
            }
            
            result = _parse_unary_expr(parser_state)
            
            mock_primary.assert_called_once()
            self.assertEqual(result["type"], "PAREN_EXPR")

    def test_parse_unary_nested_minus(self):
        """Test parsing nested unary minus: --x"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        
        def mock_primary_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "UNARY_OP",
                    "children": [{"type": "IDENTIFIER", "children": [], "value": "x", "line": 1, "column": 3}],
                    "value": "-",
                    "line": 1,
                    "column": 2
                }
            else:
                return {
                    "type": "IDENTIFIER",
                    "children": [],
                    "value": "x",
                    "line": 1,
                    "column": 3
                }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.side_effect = mock_primary_side_effect
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_unary_error_propagation(self):
        """Test that errors from recursive unary parsing are propagated"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        def mock_primary_side_effect(state):
            state["error"] = "Recursive error"
            return {
                "type": "ERROR",
                "children": [],
                "value": None,
                "line": -1,
                "column": -1
            }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.side_effect = mock_primary_side_effect
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertIn("error", parser_state)

    def test_parse_unary_mixed_operators(self):
        """Test parsing mixed unary operators: -!x"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "NOT", "value": "!", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        
        def mock_primary_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "UNARY_OP",
                    "children": [{"type": "IDENTIFIER", "children": [], "value": "x", "line": 1, "column": 3}],
                    "value": "!",
                    "line": 1,
                    "column": 2
                }
            else:
                return {
                    "type": "IDENTIFIER",
                    "children": [],
                    "value": "x",
                    "line": 1,
                    "column": 3
                }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.side_effect = mock_primary_side_effect
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")
            self.assertEqual(result["children"][0]["value"], "!")
            self.assertEqual(parser_state["pos"], 2)

    def test_parse_unary_preserves_line_column(self):
        """Test that line and column information is preserved correctly"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 10, "column": 25},
            {"type": "IDENTIFIER", "value": "x", "line": 10, "column": 26},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 10,
                "column": 26
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 25)

    def test_parse_unary_token_missing_fields(self):
        """Test handling of tokens with missing line/column fields"""
        tokens = [
            {"type": "MINUS", "value": "-"},
            {"type": "IDENTIFIER", "value": "x"},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": -1,
                "column": -1
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["line"], -1)
            self.assertEqual(result["column"], -1)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
