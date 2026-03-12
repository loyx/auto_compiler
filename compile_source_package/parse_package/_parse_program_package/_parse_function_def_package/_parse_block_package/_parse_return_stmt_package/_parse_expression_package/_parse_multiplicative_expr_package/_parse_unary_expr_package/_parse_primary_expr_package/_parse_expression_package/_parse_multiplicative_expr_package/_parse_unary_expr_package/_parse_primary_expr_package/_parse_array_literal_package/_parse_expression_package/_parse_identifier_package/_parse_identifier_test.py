import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Relative import for the function under test
from ._parse_identifier_src import _parse_identifier


def create_token(type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create test tokens."""
    return {"type": type, "value": value, "line": line, "column": column}


def create_parser_state(tokens: List[Dict], pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create parser state."""
    return {"tokens": tokens, "pos": pos, "filename": filename, "error": ""}


class TestParseIdentifier(unittest.TestCase):
    """Test cases for _parse_identifier function."""

    def test_simple_identifier(self):
        """Test parsing a simple identifier."""
        tokens = [create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "Identifier")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "")

    def test_function_call_no_args(self):
        """Test parsing function call with no arguments."""
        tokens = [
            create_token("IDENTIFIER", "foo", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 4),
            create_token("RIGHT_PAREN", ")", 1, 5)
        ]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "CallExpression")
        self.assertEqual(result["value"], "foo")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(parser_state["error"], "")

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_function_call_single_arg(self, mock_parse_expression):
        """Test parsing function call with single argument."""
        mock_arg = {"type": "Literal", "value": 42, "line": 1, "column": 6, "children": []}
        mock_parse_expression.return_value = mock_arg
        
        tokens = [
            create_token("IDENTIFIER", "bar", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 4),
            create_token("LITERAL", "42", 1, 5),
            create_token("RIGHT_PAREN", ")", 1, 7)
        ]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "CallExpression")
        self.assertEqual(result["value"], "bar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_arg)
        self.assertEqual(parser_state["pos"], 4)
        self.assertEqual(parser_state["error"], "")
        mock_parse_expression.assert_called_once()

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_function_call_multiple_args(self, mock_parse_expression):
        """Test parsing function call with multiple arguments."""
        mock_arg1 = {"type": "Literal", "value": 1, "line": 1, "column": 6, "children": []}
        mock_arg2 = {"type": "Literal", "value": 2, "line": 1, "column": 8, "children": []}
        mock_parse_expression.side_effect = [mock_arg1, mock_arg2]
        
        tokens = [
            create_token("IDENTIFIER", "baz", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 4),
            create_token("LITERAL", "1", 1, 5),
            create_token("COMMA", ",", 1, 6),
            create_token("LITERAL", "2", 1, 7),
            create_token("RIGHT_PAREN", ")", 1, 8)
        ]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "CallExpression")
        self.assertEqual(result["value"], "baz")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], mock_arg1)
        self.assertEqual(result["children"][1], mock_arg2)
        self.assertEqual(parser_state["error"], "")
        self.assertEqual(mock_parse_expression.call_count, 2)

    def test_unexpected_eof(self):
        """Test parsing when pos is at or beyond token list length."""
        tokens = [create_token("IDENTIFIER", "x", 1, 1)]
        parser_state = create_parser_state(tokens, pos=1)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "Error")
        self.assertEqual(result["value"], "Unexpected EOF")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_function_call_missing_right_paren(self):
        """Test parsing function call with missing RIGHT_PAREN."""
        tokens = [
            create_token("IDENTIFIER", "func", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 5),
            create_token("LITERAL", "42", 1, 6)
        ]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "CallExpression")
        self.assertEqual(result["value"], "func")
        self.assertEqual(parser_state["error"], "Expected RIGHT_PAREN in function call")

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_function_call_unexpected_token_after_arg(self, mock_parse_expression):
        """Test parsing function call with unexpected token after argument."""
        mock_arg = {"type": "Literal", "value": 1, "line": 1, "column": 6, "children": []}
        mock_parse_expression.return_value = mock_arg
        
        tokens = [
            create_token("IDENTIFIER", "func", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 5),
            create_token("LITERAL", "1", 1, 6),
            create_token("IDENTIFIER", "unexpected", 1, 7)
        ]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "CallExpression")
        self.assertEqual(result["value"], "func")
        self.assertIn("Expected COMMA or RIGHT_PAREN", parser_state["error"])

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_function_call_eof_in_args(self, mock_parse_expression):
        """Test parsing function call when EOF occurs during argument parsing."""
        mock_arg = {"type": "Literal", "value": 1, "line": 1, "column": 6, "children": []}
        mock_parse_expression.return_value = mock_arg
        
        tokens = [
            create_token("IDENTIFIER", "func", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 5),
            create_token("LITERAL", "1", 1, 6)
        ]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "CallExpression")
        self.assertEqual(result["value"], "func")
        self.assertEqual(parser_state["error"], "Unexpected end of input in function call")

    def test_identifier_at_end_of_tokens(self):
        """Test parsing identifier that is the last token."""
        tokens = [
            create_token("LITERAL", "5", 1, 1),
            create_token("IDENTIFIER", "y", 1, 3)
        ]
        parser_state = create_parser_state(tokens, pos=1)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["type"], "Identifier")
        self.assertEqual(result["value"], "y")
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(parser_state["error"], "")

    def test_function_call_with_position_tracking(self):
        """Test that line and column are correctly preserved from identifier token."""
        tokens = [
            create_token("IDENTIFIER", "test", 5, 10),
            create_token("LEFT_PAREN", "(", 5, 14),
            create_token("RIGHT_PAREN", ")", 5, 15)
        ]
        parser_state = create_parser_state(tokens)
        
        result = _parse_identifier(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()
