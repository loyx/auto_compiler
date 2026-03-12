# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === relative imports ===
from ._parse_primary_expr_src import _parse_primary_expr


# === Test Helpers ===
def create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def mock_parse_expression_impl(state: Dict[str, Any]) -> Dict[str, Any]:
    """Mock implementation for _parse_expression."""
    return {"type": "MOCK_EXPR", "value": "mocked"}


# === Test Cases ===
class TestParsePrimaryExpr(unittest.TestCase):
    """Test cases for _parse_primary_expr function."""

    def test_parse_identifier(self):
        """Test parsing an IDENTIFIER token."""
        tokens = [create_token("IDENTIFIER", "x", line=1, column=1)]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_number(self):
        """Test parsing a LITERAL token (number)."""
        tokens = [create_token("LITERAL", "42", line=2, column=5)]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_string(self):
        """Test parsing a LITERAL token (string)."""
        tokens = [create_token("LITERAL", '"hello"', line=3, column=10)]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression (LPAREN ... RPAREN)."""
        inner_ast = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 3}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_expression', return_value=inner_ast):
            tokens = [
                create_token("LPAREN", "(", line=1, column=1),
                create_token("IDENTIFIER", "y", line=1, column=3),
                create_token("RPAREN", ")", line=1, column=4)
            ]
            parser_state = create_parser_state(tokens, pos=0)
            
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result, inner_ast)
            self.assertEqual(parser_state["pos"], 3)

    def test_parse_nested_parentheses(self):
        """Test parsing nested parenthesized expressions."""
        inner_ast = {"type": "LITERAL", "value": "100", "line": 1, "column": 5}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_expression', return_value=inner_ast):
            tokens = [
                create_token("LPAREN", "(", line=1, column=1),
                create_token("LPAREN", "(", line=1, column=2),
                create_token("LITERAL", "100", line=1, column=5),
                create_token("RPAREN", ")", line=1, column=8),
                create_token("RPAREN", ")", line=1, column=9)
            ]
            parser_state = create_parser_state(tokens, pos=0)
            
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result, inner_ast)
            self.assertEqual(parser_state["pos"], 1)

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = create_parser_state([], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos >= len(tokens) raises SyntaxError."""
        tokens = [create_token("IDENTIFIER", "x")]
        parser_state = create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unexpected_token_raises_syntax_error(self):
        """Test that unexpected token type raises SyntaxError."""
        tokens = [create_token("PLUS", "+", line=5, column=10)]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("line 5", str(context.exception))
        self.assertIn("column 10", str(context.exception))

    def test_lparen_without_rparen_raises_syntax_error(self):
        """Test that LPAREN without closing RPAREN raises SyntaxError."""
        tokens = [
            create_token("LPAREN", "(", line=2, column=1),
            create_token("IDENTIFIER", "z", line=2, column=2)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        def mock_impl(state):
            state["pos"] = 2
            return {"type": "IDENTIFIER", "value": "z"}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_expression', side_effect=mock_impl):
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))

    def test_lparen_with_wrong_closing_token_raises_syntax_error(self):
        """Test that LPAREN closed with wrong token raises SyntaxError."""
        tokens = [
            create_token("LPAREN", "(", line=3, column=1),
            create_token("IDENTIFIER", "a", line=3, column=2),
            create_token("PLUS", "+", line=3, column=3)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        def mock_impl(state):
            state["pos"] = 2
            return {"type": "IDENTIFIER", "value": "a"}
        
        with patch('._parse_primary_expr_src._parse_expression', side_effect=mock_impl):
            with self.assertRaises(SyntaxError) as context:
                _parse_primary_expr(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))
            self.assertIn("got '+'", str(context.exception))

    def test_multiple_calls_increment_pos_correctly(self):
        """Test that multiple calls correctly increment pos."""
        tokens = [
            create_token("IDENTIFIER", "a", line=1, column=1),
            create_token("LITERAL", "1", line=1, column=3),
            create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result1 = _parse_primary_expr(parser_state)
        self.assertEqual(result1["value"], "a")
        self.assertEqual(parser_state["pos"], 1)
        
        result2 = _parse_primary_expr(parser_state)
        self.assertEqual(result2["value"], "1")
        self.assertEqual(parser_state["pos"], 2)
        
        result3 = _parse_primary_expr(parser_state)
        self.assertEqual(result3["value"], "b")
        self.assertEqual(parser_state["pos"], 3)

    def test_preserves_original_position_on_error(self):
        """Test that pos is not incremented when error occurs."""
        tokens = [create_token("PLUS", "+", line=1, column=1)]
        parser_state = create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]
        
        try:
            _parse_primary_expr(parser_state)
        except SyntaxError:
            pass
        
        self.assertEqual(parser_state["pos"], original_pos)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
