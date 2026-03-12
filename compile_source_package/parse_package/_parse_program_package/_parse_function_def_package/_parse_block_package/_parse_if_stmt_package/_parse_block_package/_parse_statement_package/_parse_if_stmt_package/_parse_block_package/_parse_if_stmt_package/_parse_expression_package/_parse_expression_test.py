# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "filename": filename,
            "pos": pos
        }

    def _create_token(self, token_type: str, value: Any, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_calls_binary_expression(self, mock_parse_binary):
        """Test that _parse_expression delegates to _parse_binary_expression with min_precedence=0."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "literal", "value": 42}
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        mock_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_identifier(self, mock_parse_binary):
        """Test parsing an identifier expression."""
        tokens = [self._create_token("IDENT", "x")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "identifier", "value": "x", "line": 1, "column": 1}
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "x")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_number_literal(self, mock_parse_binary):
        """Test parsing a number literal expression."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "literal", "value": 42, "line": 1, "column": 1}
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], 42)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_string_literal(self, mock_parse_binary):
        """Test parsing a string literal expression."""
        tokens = [self._create_token("STRING", "hello")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "literal", "value": "hello", "line": 1, "column": 1}
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], "hello")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_binary_operation(self, mock_parse_binary):
        """Test parsing a binary operation expression."""
        tokens = [
            self._create_token("NUMBER", "1"),
            self._create_token("PLUS", "+"),
            self._create_token("NUMBER", "2")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {
            "type": "binary_op",
            "op": "PLUS",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["op"], "PLUS")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_parenthesized(self, mock_parse_binary):
        """Test parsing a parenthesized expression."""
        tokens = [
            self._create_token("LPAREN", "("),
            self._create_token("NUMBER", "42"),
            self._create_token("RPAREN", ")")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "literal", "value": 42}
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], 42)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_function_call(self, mock_parse_binary):
        """Test parsing a function call expression."""
        tokens = [
            self._create_token("IDENT", "foo"),
            self._create_token("LPAREN", "("),
            self._create_token("RPAREN", ")")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "call", "function": "foo", "args": []}
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "call")
        self.assertEqual(result["function"], "foo")

    def test_parse_expression_empty_tokens_raises_syntax_error(self):
        """Test that parsing with empty tokens raises SyntaxError."""
        parser_state = self._create_parser_state(tokens=[], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input in expression", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_parse_expression_pos_at_end_raises_syntax_error(self):
        """Test that parsing when pos is at end of tokens raises SyntaxError."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input in expression", str(context.exception))

    def test_parse_expression_pos_beyond_end_raises_syntax_error(self):
        """Test that parsing when pos is beyond end of tokens raises SyntaxError."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input in expression", str(context.exception))

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_updates_pos(self, mock_parse_binary):
        """Test that parser_state pos is updated after parsing."""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        def side_effect(state, min_prec):
            state["pos"] = 1
            return {"type": "literal", "value": 42}
        
        mock_parse_binary.side_effect = side_effect
        
        _parse_expression(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_with_custom_filename(self, mock_parse_binary):
        """Test that error message includes custom filename."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0, filename="custom_file.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("custom_file.py", str(context.exception))

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_binary_expression")
    def test_parse_expression_complex_expression(self, mock_parse_binary):
        """Test parsing a complex expression with multiple operators."""
        tokens = [
            self._create_token("IDENT", "x"),
            self._create_token("PLUS", "+"),
            self._create_token("IDENT", "y"),
            self._create_token("MUL", "*"),
            self._create_token("IDENT", "z")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        expected_ast = {
            "type": "binary_op",
            "op": "PLUS",
            "left": {"type": "identifier", "value": "x"},
            "right": {
                "type": "binary_op",
                "op": "MUL",
                "left": {"type": "identifier", "value": "y"},
                "right": {"type": "identifier", "value": "z"}
            }
        }
        mock_parse_binary.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["op"], "PLUS")


if __name__ == "__main__":
    unittest.main()
