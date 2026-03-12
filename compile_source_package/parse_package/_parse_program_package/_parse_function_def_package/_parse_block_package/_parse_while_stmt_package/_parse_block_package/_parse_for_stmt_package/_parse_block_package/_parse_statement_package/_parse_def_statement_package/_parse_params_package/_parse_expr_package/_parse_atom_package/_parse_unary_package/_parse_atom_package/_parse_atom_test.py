import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._parse_atom_src import _parse_atom


class TestParseAtom(unittest.TestCase):
    
    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.ccl",
            "error": None
        }
    
    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def test_parse_number_integer(self):
        """Test parsing integer number"""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "NUM")
        self.assertEqual(result["value"], 42)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_number_float(self):
        """Test parsing float number"""
        tokens = [self._create_token("NUMBER", "3.14")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "NUM")
        self.assertEqual(result["value"], 3.14)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_string(self):
        """Test parsing string literal"""
        tokens = [self._create_token("STRING", "hello")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "STR")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_ident(self):
        """Test parsing identifier"""
        tokens = [self._create_token("IDENT", "x")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["name"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_true(self):
        """Test parsing TRUE boolean"""
        tokens = [self._create_token("TRUE", "true")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "BOOL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_false(self):
        """Test parsing FALSE boolean"""
        tokens = [self._create_token("FALSE", "false")]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "BOOL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_parenthesized_expression(self, mock_parse_expression):
        """Test parsing parenthesized expression"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("NUMBER", "42", 1, 2),
            self._create_token("RPAREN", ")", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_expression to return a NUM AST
        mock_parse_expression.return_value = {
            "type": "NUM",
            "value": 42,
            "line": 1,
            "column": 2
        }
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "NUM")
        self.assertEqual(result["value"], 42)
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_expression.assert_called_once()
    
    def test_unexpected_end_of_input(self):
        """Test error when input ends unexpectedly"""
        tokens = []
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(ValueError) as context:
            _parse_atom(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_missing_rparen(self, mock_parse_expression):
        """Test error when RPAREN is missing"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("NUMBER", "42", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_expression to consume the NUMBER token
        def mock_impl(state):
            state["pos"] = 2
            return {"type": "NUM", "value": 42, "line": 1, "column": 2}
        
        mock_parse_expression.side_effect = mock_impl
        
        with self.assertRaises(ValueError) as context:
            _parse_atom(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_wrong_closing_token(self, mock_parse_expression):
        """Test error when closing token is not RPAREN"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("NUMBER", "42", 1, 2),
            self._create_token("IDENT", "x", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Mock _parse_expression to consume the NUMBER token
        def mock_impl(state):
            state["pos"] = 2
            return {"type": "NUM", "value": 42, "line": 1, "column": 2}
        
        mock_parse_expression.side_effect = mock_impl
        
        with self.assertRaises(ValueError) as context:
            _parse_atom(parser_state)
        
        self.assertIn("Expected ')'", str(context.exception))
        self.assertIn("IDENT", str(context.exception))
    
    def test_unexpected_token_type(self):
        """Test error when token type is not supported"""
        tokens = [self._create_token("PLUS", "+")]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(ValueError) as context:
            _parse_atom(parser_state)
        
        self.assertIn("Unexpected token type", str(context.exception))
        self.assertIn("PLUS", str(context.exception))
    
    def test_position_advancement(self):
        """Test that position is advanced after parsing"""
        tokens = [
            self._create_token("NUMBER", "1", 1, 1),
            self._create_token("NUMBER", "2", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(result["value"], 1)
        
        # Parse second atom
        result2 = _parse_atom(parser_state)
        
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(result2["value"], 2)
    
    def test_line_column_preservation(self):
        """Test that line and column information is preserved"""
        tokens = [self._create_token("IDENT", "var", 5, 10)]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == '__main__':
    unittest.main()
