import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_primary_src import _parse_primary


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""
    
    def test_parse_identifier(self):
        """Test parsing an identifier token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_number_integer(self):
        """Test parsing an integer number literal."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_number_float(self):
        """Test parsing a float number literal."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3.14", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_string(self):
        """Test parsing a string literal."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_true(self):
        """Test parsing a true boolean literal."""
        parser_state = {
            "tokens": [
                {"type": "TRUE", "value": "true", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_false(self):
        """Test parsing a false boolean literal."""
        parser_state = {
            "tokens": [
                {"type": "FALSE", "value": "false", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_nil(self):
        """Test parsing a nil literal."""
        parser_state = {
            "tokens": [
                {"type": "NIL", "value": "nil", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_parenthesized_expression(self, mock_parse_expression):
        """Test parsing a parenthesized expression."""
        mock_parse_expression.return_value = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
                {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "GROUPING")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["value"], 42)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 3)
        self.assertNotIn("error", parser_state)
        mock_parse_expression.assert_called_once()
    
    def test_parse_empty_tokens(self):
        """Test parsing with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unexpected_eof")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("error", parser_state)
    
    def test_parse_pos_at_end(self):
        """Test parsing when pos is at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unexpected_eof")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIn("error", parser_state)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_missing_right_paren(self, mock_parse_expression):
        """Test parsing parenthesized expression without closing paren."""
        mock_parse_expression.return_value = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "missing_right_paren")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertIn("error", parser_state)
        self.assertIn("Expected ')'", parser_state["error"])
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_missing_right_paren_eof(self, mock_parse_expression):
        """Test parsing parenthesized expression when EOF after expression."""
        mock_parse_expression.return_value = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        # Simulate _parse_expression consuming the NUMBER token
        def consume_token(state):
            state["pos"] = 2
            return {
                "type": "LITERAL",
                "value": 42,
                "line": 1,
                "column": 2
            }
        
        mock_parse_expression.side_effect = consume_token
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "missing_right_paren")
        self.assertIn("error", parser_state)
    
    def test_parse_unexpected_token(self):
        """Test parsing an unexpected token type."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unexpected_token")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("error", parser_state)
        self.assertIn("'+'", parser_state["error"])
    
    def test_parse_identifier_not_at_start(self):
        """Test parsing identifier when pos is not at start."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 2)
        self.assertNotIn("error", parser_state)
    
    def test_parse_number_zero(self):
        """Test parsing zero as number literal."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "0", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 0)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_negative_number(self):
        """Test parsing negative number (should be parsed as NUMBER token with '-' in value)."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "-42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], -42)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()
