# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._parse_function_call_src import _parse_function_call


class TestParseFunctionCall(unittest.TestCase):
    """Test cases for _parse_function_call function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_identifier_ast(self, name: str = "foo") -> Dict[str, Any]:
        """Helper to create an identifier AST node."""
        return {
            "type": "IDENTIFIER",
            "name": name,
            "line": 1,
            "column": 1
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_empty_argument_list(self, mock_parse_expression: MagicMock) -> None:
        """Test function call with empty argument list: foo()"""
        lparen_token = self._create_token("LPAREN", "(", 1, 5)
        rparen_token = self._create_token("RPAREN", ")", 1, 6)
        tokens = [lparen_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        result = _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["callee"], identifier_ast)
        self.assertEqual(result["arguments"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)
        mock_parse_expression.assert_not_called()

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_single_argument(self, mock_parse_expression: MagicMock) -> None:
        """Test function call with single argument: foo(42)"""
        lparen_token = self._create_token("LPAREN", "(", 1, 5)
        arg_token = self._create_token("NUMBER", "42", 1, 6)
        rparen_token = self._create_token("RPAREN", ")", 1, 8)
        tokens = [lparen_token, arg_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        expected_arg_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 6}
        mock_parse_expression.return_value = expected_arg_ast

        result = _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["callee"], identifier_ast)
        self.assertEqual(len(result["arguments"]), 1)
        self.assertEqual(result["arguments"][0], expected_arg_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_expression.assert_called_once()

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_multiple_arguments(self, mock_parse_expression: MagicMock) -> None:
        """Test function call with multiple arguments: foo(1, 2, 3)"""
        lparen_token = self._create_token("LPAREN", "(", 1, 5)
        arg1_token = self._create_token("NUMBER", "1", 1, 6)
        comma1_token = self._create_token("COMMA", ",", 1, 7)
        arg2_token = self._create_token("NUMBER", "2", 1, 8)
        comma2_token = self._create_token("COMMA", ",", 1, 9)
        arg3_token = self._create_token("NUMBER", "3", 1, 10)
        rparen_token = self._create_token("RPAREN", ")", 1, 11)
        tokens = [lparen_token, arg1_token, comma1_token, arg2_token, comma2_token, arg3_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        arg1_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 6}
        arg2_ast = {"type": "NUMBER", "value": "2", "line": 1, "column": 8}
        arg3_ast = {"type": "NUMBER", "value": "3", "line": 1, "column": 10}
        mock_parse_expression.side_effect = [arg1_ast, arg2_ast, arg3_ast]

        result = _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["callee"], identifier_ast)
        self.assertEqual(len(result["arguments"]), 3)
        self.assertEqual(result["arguments"][0], arg1_ast)
        self.assertEqual(result["arguments"][1], arg2_ast)
        self.assertEqual(result["arguments"][2], arg3_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(mock_parse_expression.call_count, 3)

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_missing_closing_paren_raises_error(self, mock_parse_expression: MagicMock) -> None:
        """Test that missing RPAREN raises SyntaxError: foo(42"""
        lparen_token = self._create_token("LPAREN", "(", 1, 5)
        arg_token = self._create_token("NUMBER", "42", 1, 6)
        tokens = [lparen_token, arg_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        expected_arg_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 6}
        mock_parse_expression.return_value = expected_arg_ast

        with self.assertRaises(SyntaxError) as context:
            _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertIn("Unexpected end of input", str(context.exception))

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_invalid_token_after_argument_raises_error(self, mock_parse_expression: MagicMock) -> None:
        """Test that invalid token after argument raises SyntaxError: foo(42 +)"""
        lparen_token = self._create_token("LPAREN", "(", 1, 5)
        arg_token = self._create_token("NUMBER", "42", 1, 6)
        invalid_token = self._create_token("PLUS", "+", 1, 8)
        tokens = [lparen_token, arg_token, invalid_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        expected_arg_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 6}
        mock_parse_expression.return_value = expected_arg_ast

        with self.assertRaises(SyntaxError) as context:
            _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertIn("Expected ',' or ')'", str(context.exception))
        self.assertIn("+", str(context.exception))

    @patch('._parse_expression_package._parse_expression_src._parse_expression')
    def test_end_of_input_while_parsing_first_argument(self, mock_parse_expression: MagicMock) -> None:
        """Test that end of input while parsing first argument raises SyntaxError: foo("""
        lparen_token = self._create_token("LPAREN", "(", 1, 5)
        tokens = [lparen_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        with self.assertRaises(SyntaxError) as context:
            _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertIn("Unexpected end of input", str(context.exception))
        mock_parse_expression.assert_not_called()

    @patch('._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_end_of_input_after_comma(self, mock_parse_expression: MagicMock) -> None:
        """Test that end of input after comma raises SyntaxError: foo(1,"""
        lparen_token = self._create_token("LPAREN", "(", 1, 5)
        arg1_token = self._create_token("NUMBER", "1", 1, 6)
        comma_token = self._create_token("COMMA", ",", 1, 7)
        tokens = [lparen_token, arg1_token, comma_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        arg1_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 6}
        mock_parse_expression.return_value = arg1_ast

        with self.assertRaises(SyntaxError) as context:
            _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(mock_parse_expression.call_count, 1)

    @patch('._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parser_state_pos_advancement(self, mock_parse_expression: MagicMock) -> None:
        """Test that parser_state['pos'] is correctly advanced through parsing."""
        lparen_token = self._create_token("LPAREN", "(", 1, 1)
        arg1_token = self._create_token("IDENTIFIER", "x", 1, 2)
        comma_token = self._create_token("COMMA", ",", 1, 3)
        arg2_token = self._create_token("IDENTIFIER", "y", 1, 4)
        rparen_token = self._create_token("RPAREN", ")", 1, 5)
        tokens = [lparen_token, arg1_token, comma_token, arg2_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("foo")

        arg1_ast = {"type": "IDENTIFIER", "name": "x", "line": 1, "column": 2}
        arg2_ast = {"type": "IDENTIFIER", "name": "y", "line": 1, "column": 4}
        mock_parse_expression.side_effect = [arg1_ast, arg2_ast]

        result = _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(len(result["arguments"]), 2)

    @patch('._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_complex_expression_arguments(self, mock_parse_expression: MagicMock) -> None:
        """Test function call with complex expression arguments."""
        lparen_token = self._create_token("LPAREN", "(", 2, 10)
        rparen_token = self._create_token("RPAREN", ")", 2, 30)
        tokens = [lparen_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=1)
        identifier_ast = self._create_identifier_ast("calculate")

        complex_arg1 = {"type": "BINARY_OP", "operator": "+", "left": {"type": "NUMBER", "value": "1"}, "right": {"type": "NUMBER", "value": "2"}}
        complex_arg2 = {"type": "CALL", "callee": {"type": "IDENTIFIER", "name": "helper"}, "arguments": []}
        mock_parse_expression.side_effect = [complex_arg1, complex_arg2]

        arg1_token = self._create_token("NUMBER", "1", 2, 11)
        comma_token = self._create_token("COMMA", ",", 2, 20)
        arg2_token = self._create_token("IDENTIFIER", "helper", 2, 21)
        tokens = [lparen_token, arg1_token, comma_token, arg2_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_function_call(parser_state, identifier_ast, lparen_token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(len(result["arguments"]), 2)
        self.assertEqual(mock_parse_expression.call_count, 2)


if __name__ == "__main__":
    unittest.main()
