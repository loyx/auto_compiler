"""Unit tests for _parse_primary function."""
import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_primary_src import _parse_primary


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {"type": token_type, "value": value, "line": line, "column": column}

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {"tokens": tokens, "pos": pos, "filename": filename}

    # ========== Happy Path Tests ==========

    def test_parse_identifier(self):
        """Test parsing an IDENTIFIER token."""
        token = self._create_token("IDENTIFIER", "myVar")
        parser_state = self._create_parser_state([token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_integer_number(self):
        """Test parsing an integer NUMBER token."""
        token = self._create_token("NUMBER", "42")
        parser_state = self._create_parser_state([token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_float_number(self):
        """Test parsing a float NUMBER token."""
        token = self._create_token("NUMBER", "3.14")
        parser_state = self._create_parser_state([token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string(self):
        """Test parsing a STRING token."""
        token = self._create_token("STRING", "hello world")
        parser_state = self._create_parser_state([token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_true_boolean(self):
        """Test parsing a TRUE token."""
        token = self._create_token("TRUE", "true")
        parser_state = self._create_parser_state([token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], True)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_false_boolean(self):
        """Test parsing a FALSE token."""
        token = self._create_token("FALSE", "false")
        parser_state = self._create_parser_state([token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "BOOLEAN")
        self.assertEqual(result["value"], False)
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_parenthesized_expression(self, mock_parse_expression):
        """Test parsing a parenthesized expression LPAREN...RPAREN."""
        lparen_token = self._create_token("LPAREN", "(")
        rparen_token = self._create_token("RPAREN", ")")
        expr_ast = {"type": "NUMBER", "value": 42, "line": 1, "column": 2}
        mock_parse_expression.return_value = expr_ast
        
        parser_state = self._create_parser_state([lparen_token, rparen_token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result, expr_ast)
        self.assertEqual(parser_state["pos"], 2)
        mock_parse_expression.assert_called_once()

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_list_elements_package._parse_list_elements_src._parse_list_elements')
    def test_parse_list_literal(self, mock_parse_list_elements):
        """Test parsing a list literal LBRACKET...RBRACKET."""
        lbracket_token = self._create_token("LBRACKET", "[")
        rbracket_token = self._create_token("RBRACKET", "]")
        elements = [
            {"type": "NUMBER", "value": 1, "line": 1, "column": 2},
            {"type": "NUMBER", "value": 2, "line": 1, "column": 4}
        ]
        mock_parse_list_elements.return_value = elements
        
        parser_state = self._create_parser_state([lbracket_token, rbracket_token])
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LIST")
        self.assertEqual(result["elements"], elements)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)
        mock_parse_list_elements.assert_called_once()

    # ========== Boundary/Edge Cases ==========

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = self._create_parser_state([])
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond tokens length raises SyntaxError."""
        token = self._create_token("IDENTIFIER", "x")
        parser_state = self._create_parser_state([token], pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unexpected_token_type_raises_syntax_error(self):
        """Test that unexpected token type raises SyntaxError."""
        token = self._create_token("PLUS", "+")
        parser_state = self._create_parser_state([token])
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("of type PLUS", str(context.exception))

    def test_missing_closing_paren_raises_syntax_error(self):
        """Test that missing RPAREN raises SyntaxError."""
        lparen_token = self._create_token("LPAREN", "(", line=5, column=10)
        parser_state = self._create_parser_state([lparen_token])
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {"type": "NUMBER", "value": 42}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Expected ')' to close parenthesis", str(context.exception))
            self.assertIn("5:10", str(context.exception))

    def test_missing_closing_bracket_raises_syntax_error(self):
        """Test that missing RBRACKET raises SyntaxError."""
        lbracket_token = self._create_token("LBRACKET", "[", line=3, column=7)
        parser_state = self._create_parser_state([lbracket_token])
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_list_elements_package._parse_list_elements_src._parse_list_elements') as mock_parse_list_elements:
            mock_parse_list_elements.return_value = []
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Expected ']' to close list", str(context.exception))
            self.assertIn("3:7", str(context.exception))

    def test_wrong_closing_token_for_paren_raises_syntax_error(self):
        """Test that wrong closing token for paren raises SyntaxError."""
        lparen_token = self._create_token("LPAREN", "(", line=2, column=3)
        wrong_close_token = self._create_token("RBRACKET", "]")
        parser_state = self._create_parser_state([lparen_token, wrong_close_token])
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {"type": "NUMBER", "value": 42}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Expected ')' to close parenthesis", str(context.exception))

    def test_wrong_closing_token_for_list_raises_syntax_error(self):
        """Test that wrong closing token for list raises SyntaxError."""
        lbracket_token = self._create_token("LBRACKET", "[", line=4, column=5)
        wrong_close_token = self._create_token("RPAREN", ")")
        parser_state = self._create_parser_state([lbracket_token, wrong_close_token])
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_list_elements_package._parse_list_elements_src._parse_list_elements') as mock_parse_list_elements:
            mock_parse_list_elements.return_value = []
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Expected ']' to close list", str(context.exception))

    # ========== Additional Edge Cases ==========

    def test_custom_filename_in_error_message(self):
        """Test that custom filename appears in error messages."""
        parser_state = self._create_parser_state([], filename="my_script.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("my_script.py", str(context.exception))

    def test_default_filename_when_not_provided(self):
        """Test that default filename '<unknown>' is used when not provided."""
        parser_state = {"tokens": [], "pos": 0}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("<unknown>", str(context.exception))

    def test_preserves_line_and_column_in_ast(self):
        """Test that line and column are preserved in AST for various token types."""
        test_cases = [
            ("IDENTIFIER", "var", 10, 20),
            ("NUMBER", "123", 15, 25),
            ("STRING", "text", 20, 30),
            ("TRUE", "true", 25, 35),
            ("FALSE", "false", 30, 40),
        ]
        
        for token_type, value, line, column in test_cases:
            with self.subTest(token_type=token_type):
                token = self._create_token(token_type, value, line, column)
                parser_state = self._create_parser_state([token])
                
                result = _parse_primary(parser_state)
                
                self.assertEqual(result["line"], line)
                self.assertEqual(result["column"], column)


if __name__ == "__main__":
    unittest.main()
