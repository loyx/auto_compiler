# === Test file for _parse_primary ===
import unittest
from unittest.mock import patch

# === Import UUT using relative import ===
from ._parse_primary_src import _parse_primary


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""

    def test_parse_ident(self):
        """Test parsing an identifier token."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_int(self):
        """Test parsing an integer number token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 10}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_float(self):
        """Test parsing a float number token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3.14", "line": 2, "column": 3}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_scientific_notation(self):
        """Test parsing a number in scientific notation (should become float)."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1e10", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 1e10)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string(self):
        """Test parsing a string literal token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello world", "line": 3, "column": 7}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_binary_expression_package._parse_primary_package._parse_binary_expression_package._parse_binary_expression_src:_parse_binary_expression', create=True)
    def test_parse_parenthesized_expression(self, mock_parse_binary):
        """Test parsing a parenthesized expression."""
        mock_parse_binary.return_value = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [],
            "line": 1,
            "column": 6
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
                {"type": "IDENT", "value": "a", "line": 1, "column": 6},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_binary.assert_called_once()
        call_args = mock_parse_binary.call_args
        self.assertEqual(call_args[0][0], parser_state)
        self.assertEqual(call_args[1]["min_precedence"], 0)

    def test_parse_empty_tokens(self):
        """Test parsing when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_parse_pos_beyond_tokens(self):
        """Test parsing when pos is beyond tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 5
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_unknown_token_type(self):
        """Test parsing an unknown token type."""
        parser_state = {
            "tokens": [
                {"type": "UNKNOWN", "value": "?", "line": 4, "column": 12}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Expected expression, found UNKNOWN", str(context.exception))
        self.assertIn("test.py:4:12", str(context.exception))

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_binary_expression_package._parse_primary_package._parse_binary_expression_package._parse_binary_expression_src:_parse_binary_expression', create=True)
    def test_parse_parenthesized_missing_rparen_eof(self, mock_parse_binary):
        """Test parsing parenthesized expression with missing RPAREN at EOF."""
        mock_parse_binary.return_value = {
            "type": "IDENT",
            "value": "x",
            "line": 1,
            "column": 6
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
                {"type": "IDENT", "value": "x", "line": 1, "column": 6}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Expected ')', found end of input", str(context.exception))
        self.assertIn("test.py:1:5", str(context.exception))

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_binary_expression_package._parse_primary_package._parse_binary_expression_package._parse_binary_expression_src:_parse_binary_expression', create=True)
    def test_parse_parenthesized_missing_rparen_wrong_token(self, mock_parse_binary):
        """Test parsing parenthesized expression with wrong token instead of RPAREN."""
        mock_parse_binary.return_value = {
            "type": "IDENT",
            "value": "x",
            "line": 1,
            "column": 6
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
                {"type": "IDENT", "value": "x", "line": 1, "column": 6},
                {"type": "COMMA", "value": ",", "line": 1, "column": 7}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Expected ')', found COMMA", str(context.exception))
        self.assertIn("test.py:1:7", str(context.exception))

    def test_parse_number_negative(self):
        """Test parsing a negative number (should still parse as NUMBER)."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "-42", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], -42)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_ident_at_non_zero_pos(self):
        """Test parsing an identifier when pos is not at 0."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENT", "value": "y", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 1
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "y")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_string_empty(self):
        """Test parsing an empty string literal."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_zero(self):
        """Test parsing zero."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "0", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], 0)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_missing_filename_uses_default(self):
        """Test that missing filename defaults to '<unknown>'."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("<unknown>:0:0", str(context.exception))


if __name__ == "__main__":
    unittest.main()
