# === imports ===
import unittest
from typing import Any, Dict

# === relative import of target function ===
from ._parse_expression_src import _parse_expression


# === test cases ===
class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def _make_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _make_parser_state(self, tokens: list, pos: int = 0, filename: str = "") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    # === Happy Path Tests ===

    def test_parse_number_literal(self):
        """Test parsing a NUMBER token."""
        tokens = [self._make_token("NUMBER", "42")]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing a STRING token."""
        tokens = [self._make_token("STRING", '"hello"')]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_identifier(self):
        """Test parsing an IDENT token."""
        tokens = [self._make_token("IDENT", "myVar")]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression: ( expr )."""
        tokens = [
            self._make_token("LPAREN", "(", column=1),
            self._make_token("NUMBER", "10", column=2),
            self._make_token("RPAREN", ")", column=3)
        ]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "NUMBER")
        self.assertEqual(result["children"][0]["value"], "10")
        self.assertEqual(state["pos"], 3)

    def test_parse_unary_minus(self):
        """Test parsing a unary minus expression: -expr."""
        tokens = [
            self._make_token("MINUS", "-", column=1),
            self._make_token("NUMBER", "5", column=2)
        ]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "UNARY_MINUS")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "NUMBER")
        self.assertEqual(result["children"][0]["value"], "5")
        self.assertEqual(state["pos"], 2)

    def test_parse_nested_parentheses(self):
        """Test parsing nested parentheses: (( expr ))."""
        tokens = [
            self._make_token("LPAREN", "(", column=1),
            self._make_token("LPAREN", "(", column=2),
            self._make_token("NUMBER", "7", column=3),
            self._make_token("RPAREN", ")", column=4),
            self._make_token("RPAREN", ")", column=5)
        ]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "PAREN_EXPR")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "PAREN_EXPR")
        self.assertEqual(result["children"][0]["children"][0]["type"], "NUMBER")
        self.assertEqual(state["pos"], 5)

    def test_parse_unary_minus_with_parentheses(self):
        """Test parsing unary minus with parentheses: -( expr )."""
        tokens = [
            self._make_token("MINUS", "-", column=1),
            self._make_token("LPAREN", "(", column=2),
            self._make_token("NUMBER", "3", column=3),
            self._make_token("RPAREN", ")", column=4)
        ]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "UNARY_MINUS")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "PAREN_EXPR")
        self.assertEqual(state["pos"], 4)

    # === Boundary Value Tests ===

    def test_parse_at_non_zero_position(self):
        """Test parsing expression when pos is not at 0."""
        tokens = [
            self._make_token("IDENT", "skip"),
            self._make_token("NUMBER", "99")
        ]
        state = self._make_parser_state(tokens, pos=1)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "99")
        self.assertEqual(state["pos"], 2)

    def test_parse_with_custom_line_column(self):
        """Test parsing preserves line and column information."""
        tokens = [self._make_token("IDENT", "var", line=10, column=25)]
        state = self._make_parser_state(tokens, pos=0)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    # === Error Case Tests ===

    def test_parse_empty_tokens_raises(self):
        """Test that empty tokens list raises SyntaxError."""
        tokens = []
        state = self._make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unexpected end", str(context.exception))

    def test_parse_pos_beyond_tokens_raises(self):
        """Test that pos beyond tokens length raises SyntaxError."""
        tokens = [self._make_token("NUMBER", "1")]
        state = self._make_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unexpected end", str(context.exception))

    def test_parse_missing_closing_paren_raises(self):
        """Test that missing RPAREN raises SyntaxError."""
        tokens = [
            self._make_token("LPAREN", "("),
            self._make_token("NUMBER", "5")
        ]
        state = self._make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Expected closing parenthesis", str(context.exception))

    def test_parse_missing_closing_paren_at_end_raises(self):
        """Test that missing RPAREN at end of tokens raises SyntaxError."""
        tokens = [
            self._make_token("LPAREN", "("),
            self._make_token("NUMBER", "5"),
        ]
        state = self._make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Expected closing parenthesis", str(context.exception))

    def test_parse_unexpected_token_type_raises(self):
        """Test that unexpected token type raises SyntaxError."""
        tokens = [self._make_token("PLUS", "+")]
        state = self._make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unexpected token in expression", str(context.exception))
        self.assertIn("PLUS", str(context.exception))

    def test_parse_unknown_token_type_raises(self):
        """Test that unknown token type raises SyntaxError."""
        tokens = [self._make_token("UNKNOWN", "???")]
        state = self._make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unexpected token in expression", str(context.exception))
        self.assertIn("UNKNOWN", str(context.exception))

    # === State Change Tests ===

    def test_parse_updates_pos_correctly_for_number(self):
        """Test that pos is updated correctly after parsing NUMBER."""
        tokens = [self._make_token("NUMBER", "123")]
        state = self._make_parser_state(tokens, pos=0)
        
        _parse_expression(state)
        
        self.assertEqual(state["pos"], 1)

    def test_parse_updates_pos_correctly_for_paren_expr(self):
        """Test that pos is updated correctly after parsing PAREN_EXPR."""
        tokens = [
            self._make_token("LPAREN", "("),
            self._make_token("IDENT", "x"),
            self._make_token("RPAREN", ")")
        ]
        state = self._make_parser_state(tokens, pos=0)
        
        _parse_expression(state)
        
        self.assertEqual(state["pos"], 3)

    def test_parse_does_not_modify_other_state_fields(self):
        """Test that parsing does not modify other parser_state fields."""
        tokens = [self._make_token("NUMBER", "1")]
        state = self._make_parser_state(tokens, pos=0, filename="test.py")
        state["error"] = "some error"
        
        _parse_expression(state)
        
        self.assertEqual(state["filename"], "test.py")
        self.assertEqual(state["error"], "some error")
        self.assertEqual(len(state["tokens"]), 1)


# === test runner ===
if __name__ == "__main__":
    unittest.main()
