# === Test file for _parse_primary ===
# Location: _parse_primary_package/test_parse_primary.py

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Relative import for the function under test
from ._parse_primary_src import _parse_primary


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.whale",
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== Happy Path Tests ====================

    def test_parse_identifier_variable(self):
        """Test parsing a simple identifier (variable reference)."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["name"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)  # pos advanced

    def test_parse_identifier_at_end(self):
        """Test parsing identifier when it's the last token."""
        tokens = [self._create_token("IDENTIFIER", "var", line=2, column=5)]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["name"], "var")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_function_call_detected(self):
        """Test that identifier followed by LPAREN triggers function call parsing."""
        tokens = [
            self._create_token("IDENTIFIER", "func"),
            self._create_token("LPAREN", "("),
            self._create_token("RPAREN", ")")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_function_call_result = {
            "type": "CALL",
            "callee": {"type": "IDENTIFIER", "name": "func"},
            "arguments": []
        }
        
        with patch('._parse_function_call_package._parse_function_call_src._parse_function_call') as mock_parse_call:
            mock_parse_call.return_value = mock_function_call_result
            
            result = _parse_primary(parser_state)
            
            mock_parse_call.assert_called_once()
            # Verify the identifier_ast was passed
            call_args = mock_parse_call.call_args
            self.assertEqual(call_args[0][1]["name"], "func")
            self.assertEqual(call_args[0][2]["type"], "LPAREN")
            self.assertEqual(result, mock_function_call_result)

    def test_parse_number_literal(self):
        """Test parsing NUMBER literal."""
        tokens = [self._create_token("NUMBER", "42", line=1, column=10)]
        parser_state = self._create_parser_state(tokens)
        
        mock_literal_result = {
            "type": "NUMBER",
            "value": 42,
            "line": 1,
            "column": 10
        }
        
        with patch('._parse_literal_package._parse_literal_src._parse_literal') as mock_parse_literal:
            mock_parse_literal.return_value = mock_literal_result
            
            result = _parse_primary(parser_state)
            
            mock_parse_literal.assert_called_once()
            self.assertEqual(result, mock_literal_result)

    def test_parse_string_literal(self):
        """Test parsing STRING literal."""
        tokens = [self._create_token("STRING", '"hello"', line=3, column=7)]
        parser_state = self._create_parser_state(tokens)
        
        mock_literal_result = {
            "type": "STRING",
            "value": "hello",
            "line": 3,
            "column": 7
        }
        
        with patch('._parse_literal_package._parse_literal_src._parse_literal') as mock_parse_literal:
            mock_parse_literal.return_value = mock_literal_result
            
            result = _parse_primary(parser_state)
            
            mock_parse_literal.assert_called_once()
            self.assertEqual(result, mock_literal_result)

    def test_parse_boolean_literal_true(self):
        """Test parsing BOOLEAN literal (true)."""
        tokens = [self._create_token("BOOLEAN", "true", line=5, column=1)]
        parser_state = self._create_parser_state(tokens)
        
        mock_literal_result = {
            "type": "BOOLEAN",
            "value": True,
            "line": 5,
            "column": 1
        }
        
        with patch('._parse_literal_package._parse_literal_src._parse_literal') as mock_parse_literal:
            mock_parse_literal.return_value = mock_literal_result
            
            result = _parse_primary(parser_state)
            
            mock_parse_literal.assert_called_once()
            self.assertEqual(result, mock_literal_result)

    def test_parse_boolean_literal_false(self):
        """Test parsing BOOLEAN literal (false)."""
        tokens = [self._create_token("BOOLEAN", "false")]
        parser_state = self._create_parser_state(tokens)
        
        mock_literal_result = {
            "type": "BOOLEAN",
            "value": False
        }
        
        with patch('._parse_literal_package._parse_literal_src._parse_literal') as mock_parse_literal:
            mock_parse_literal.return_value = mock_literal_result
            
            result = _parse_primary(parser_state)
            
            mock_parse_literal.assert_called_once()
            self.assertEqual(result["value"], False)

    def test_parse_parenthesized_expression(self):
        """Test parsing parenthesized expression."""
        tokens = [
            self._create_token("LPAREN", "(", line=1, column=1),
            self._create_token("NUMBER", "5", line=1, column=2),
            self._create_token("RPAREN", ")", line=1, column=3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_inner_expr = {
            "type": "NUMBER",
            "value": 5,
            "line": 1,
            "column": 2
        }
        
        with patch('._parse_expression._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            
            result = _parse_primary(parser_state)
            
            mock_parse_expr.assert_called_once()
            self.assertEqual(result, mock_inner_expr)
            self.assertEqual(parser_state["pos"], 3)  # LPAREN + expr + RPAREN consumed

    def test_parse_nested_parentheses(self):
        """Test parsing nested parenthesized expressions."""
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("LPAREN", "("),
            self._create_token("NUMBER", "10"),
            self._create_token("RPAREN", ")"),
            self._create_token("RPAREN", ")")
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_inner_expr = {
            "type": "NUMBER",
            "value": 10
        }
        
        with patch('._parse_expression._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            
            result = _parse_primary(parser_state)
            
            mock_parse_expr.assert_called_once()
            self.assertEqual(result, mock_inner_expr)
            self.assertEqual(parser_state["pos"], 5)

    # ==================== Boundary Case Tests ====================

    def test_empty_tokens_list(self):
        """Test parsing when tokens list is empty."""
        parser_state = self._create_parser_state([])
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_beyond_tokens_length(self):
        """Test parsing when pos is beyond tokens length."""
        tokens = [self._create_token("NUMBER", "1")]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_at_tokens_length(self):
        """Test parsing when pos equals tokens length."""
        tokens = [self._create_token("NUMBER", "1")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_missing_rparen_in_parenthesized_expr(self):
        """Test error when RPAREN is missing in parenthesized expression."""
        tokens = [
            self._create_token("LPAREN", "(", line=2, column=3),
            self._create_token("NUMBER", "7", line=2, column=4)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_inner_expr = {"type": "NUMBER", "value": 7}
        
        with patch('._parse_expression._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            mock_parse_expr.side_effect = lambda state: state.__setitem__("pos", 1) or mock_inner_expr
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))

    def test_wrong_token_after_lparen(self):
        """Test error when wrong token follows LPAREN instead of RPAREN."""
        tokens = [
            self._create_token("LPAREN", "(", line=1, column=1),
            self._create_token("COMMA", ",", line=1, column=2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_inner_expr = {"type": "IDENTIFIER", "name": "x"}
        
        with patch('._parse_expression._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            mock_parse_expr.side_effect = lambda state: state.__setitem__("pos", 1) or mock_inner_expr
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))
            self.assertIn("COMMA", str(context.exception))

    # ==================== Error Case Tests ====================

    def test_invalid_token_type_operator(self):
        """Test error when operator token is encountered."""
        tokens = [self._create_token("PLUS", "+", line=4, column=8)]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("PLUS", str(context.exception))
        self.assertIn("line 4", str(context.exception))
        self.assertIn("column 8", str(context.exception))

    def test_invalid_token_type_keyword(self):
        """Test error when keyword token is encountered."""
        tokens = [self._create_token("IF", "if", line=10, column=1)]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token 'if'", str(context.exception))
        self.assertIn("IF", str(context.exception))

    def test_invalid_token_type_eof_marker(self):
        """Test error when EOF token is encountered."""
        tokens = [self._create_token("EOF", "", line=15, column=20)]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token", str(context.exception))
        self.assertIn("EOF", str(context.exception))

    # ==================== Side Effect Tests ====================

    def test_pos_advancement_identifier(self):
        """Test that pos is advanced correctly for identifier."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        _parse_primary(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)

    def test_pos_advancement_parenthesized(self):
        """Test that pos is advanced correctly for parenthesized expression."""
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("NUMBER", "3"),
            self._create_token("RPAREN", ")")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch('._parse_expression._parse_expression') as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: state.__setitem__("pos", 1) or {"type": "NUMBER"}
            
            _parse_primary(parser_state)
            
            self.assertEqual(parser_state["pos"], 3)

    def test_parser_state_unchanged_on_error(self):
        """Test that parser state pos is not changed on error."""
        tokens = [self._create_token("PLUS", "+")]
        parser_state = self._create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]
        
        try:
            _parse_primary(parser_state)
        except SyntaxError:
            pass
        
        self.assertEqual(parser_state["pos"], original_pos)

    # ==================== Integration-style Tests ====================

    def test_multiple_primary_expressions_sequential(self):
        """Test parsing multiple primary expressions in sequence."""
        tokens = [
            self._create_token("IDENTIFIER", "a"),
            self._create_token("IDENTIFIER", "b"),
            self._create_token("IDENTIFIER", "c")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Parse first identifier
        result1 = _parse_primary(parser_state)
        self.assertEqual(result1["name"], "a")
        self.assertEqual(parser_state["pos"], 1)
        
        # Parse second identifier
        result2 = _parse_primary(parser_state)
        self.assertEqual(result2["name"], "b")
        self.assertEqual(parser_state["pos"], 2)
        
        # Parse third identifier
        result3 = _parse_primary(parser_state)
        self.assertEqual(result3["name"], "c")
        self.assertEqual(parser_state["pos"], 3)

    def test_identifier_not_function_call_when_no_lparen(self):
        """Test that identifier is not treated as function call when next token is not LPAREN."""
        tokens = [
            self._create_token("IDENTIFIER", "x"),
            self._create_token("PLUS", "+")
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["name"], "x")
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
