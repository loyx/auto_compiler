import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
    
    def test_parse_array_literal(self):
        """Test parsing array literal expression (LEFT_BRACKET token)."""
        token = {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "ARRAY", "children": []}
        
        with patch("._parse_array_literal_package._parse_array_literal_src._parse_array_literal") as mock_parse_array:
            mock_parse_array.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_array.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_parse_object_literal(self):
        """Test parsing object literal expression (LEFT_BRACE token)."""
        token = {"type": "LEFT_BRACE", "value": "{", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "OBJECT", "children": []}
        
        with patch("._parse_object_literal_package._parse_object_literal_src._parse_object_literal") as mock_parse_object:
            mock_parse_object.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_object.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_parse_string_literal(self):
        """Test parsing string literal expression."""
        token = {"type": "STRING", "value": '"hello"', "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "LITERAL", "value": "hello"}
        
        with patch("._parse_literal_package._parse_literal_src._parse_literal") as mock_parse_literal:
            mock_parse_literal.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_literal.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_parse_number_literal(self):
        """Test parsing number literal expression."""
        token = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "LITERAL", "value": 42}
        
        with patch("._parse_literal_package._parse_literal_src._parse_literal") as mock_parse_literal:
            mock_parse_literal.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_literal.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_parse_boolean_literal(self):
        """Test parsing boolean literal expression."""
        token = {"type": "BOOLEAN", "value": "true", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "LITERAL", "value": True}
        
        with patch("._parse_literal_package._parse_literal_src._parse_literal") as mock_parse_literal:
            mock_parse_literal.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_literal.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_parse_null_literal(self):
        """Test parsing null literal expression."""
        token = {"type": "NULL", "value": "null", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "LITERAL", "value": None}
        
        with patch("._parse_literal_package._parse_literal_src._parse_literal") as mock_parse_literal:
            mock_parse_literal.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_literal.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_parse_identifier(self):
        """Test parsing identifier expression."""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "IDENTIFIER", "value": "x"}
        
        with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_identifier:
            mock_parse_identifier.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_identifier.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_parse_grouped_expression(self):
        """Test parsing grouped expression (LEFT_PAREN token)."""
        token = {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        expected_ast = {"type": "GROUPED", "children": []}
        
        with patch("._parse_grouped_expression_package._parse_grouped_expression_src._parse_grouped_expression") as mock_parse_grouped:
            mock_parse_grouped.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_grouped.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
    
    def test_position_out_of_bounds(self):
        """Test error when position is beyond token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.cc", str(context.exception))
    
    def test_position_out_of_bounds_with_filename(self):
        """Test error when position is beyond token list with specific filename."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 5,
            "filename": "main.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("main.cc", str(context.exception))
    
    def test_unknown_token_type(self):
        """Test error when encountering unknown token type."""
        token = {"type": "UNKNOWN_TOKEN", "value": "?", "line": 3, "column": 5}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected token 'UNKNOWN_TOKEN'", str(context.exception))
        self.assertIn("line 3", str(context.exception))
        self.assertIn("column 5", str(context.exception))
        self.assertIn("test.cc", str(context.exception))
    
    def test_token_missing_type_field(self):
        """Test error when token is missing type field."""
        token = {"value": "something", "line": 2, "column": 3}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected token ''", str(context.exception))
    
    def test_parser_state_missing_filename(self):
        """Test error message when filename is not provided."""
        token = {"type": "INVALID", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("unknown", str(context.exception))
    
    def test_position_at_last_token(self):
        """Test parsing when position is at the last valid token."""
        token = {"type": "NUMBER", "value": "100", "line": 1, "column": 1}
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"first"', "line": 1, "column": 1},
                token
            ],
            "pos": 1,
            "filename": "test.cc"
        }
        expected_ast = {"type": "LITERAL", "value": 100}
        
        with patch("._parse_literal_package._parse_literal_src._parse_literal") as mock_parse_literal:
            mock_parse_literal.return_value = expected_ast
            result = _parse_expression(parser_state)
            mock_parse_literal.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)


if __name__ == "__main__":
    unittest.main()
