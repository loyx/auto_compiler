# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._handle_identifier_src import _handle_identifier


class TestHandleIdentifier(unittest.TestCase):
    """Test cases for _handle_identifier function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser_state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_simple_identifier_variable_reference(self):
        """Test: identifier followed by non-LPAREN token returns IDENTIFIER node."""
        token = self._create_token("IDENTIFIER", "x", line=1, column=5)
        next_token = self._create_token("PLUS", "+", line=1, column=6)
        tokens = [token, next_token]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _handle_identifier(parser_state, token)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_identifier_at_end_of_tokens(self):
        """Test: identifier at end of token list returns IDENTIFIER node."""
        token = self._create_token("IDENTIFIER", "y", line=2, column=10)
        tokens = [token]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _handle_identifier(parser_state, token)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_function_call_with_arguments(self):
        """Test: identifier followed by LPAREN returns CALL node."""
        token = self._create_token("IDENTIFIER", "func", line=3, column=1)
        lparen_token = self._create_token("LPAREN", "(", line=3, column=5)
        rparen_token = self._create_token("RPAREN", ")", line=3, column=10)
        tokens = [token, lparen_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_arguments = [
            {"type": "LITERAL", "value": 42, "line": 3, "column": 6}
        ]

        with patch("._parse_argument_list_package._parse_argument_list_src._parse_argument_list") as mock_parse_args:
            mock_parse_args.return_value = mock_arguments

            result = _handle_identifier(parser_state, token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["function"]["type"], "IDENTIFIER")
        self.assertEqual(result["function"]["value"], "func")
        self.assertEqual(result["arguments"], mock_arguments)
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_function_call_empty_arguments(self):
        """Test: function call with empty argument list."""
        token = self._create_token("IDENTIFIER", "empty_func", line=1, column=1)
        lparen_token = self._create_token("LPAREN", "(", line=1, column=11)
        rparen_token = self._create_token("RPAREN", ")", line=1, column=12)
        tokens = [token, lparen_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_argument_list_package._parse_argument_list_src._parse_argument_list") as mock_parse_args:
            mock_parse_args.return_value = []

            result = _handle_identifier(parser_state, token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["function"]["value"], "empty_func")
        self.assertEqual(result["arguments"], [])

    def test_function_call_parse_error(self):
        """Test: function call with argument parse error returns ERROR node."""
        token = self._create_token("IDENTIFIER", "bad_func", line=5, column=3)
        lparen_token = self._create_token("LPAREN", "(", line=5, column=12)
        tokens = [token, lparen_token]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_argument_list_package._parse_argument_list_src._parse_argument_list") as mock_parse_args:
            with patch("._build_error_node_package._build_error_node_src._build_error_node") as mock_build_error:
                mock_parse_args.return_value = []
                parser_state["error"] = "解析失败"
                mock_build_error.return_value = {
                    "type": "ERROR",
                    "message": "函数调用参数解析失败",
                    "line": 5,
                    "column": 3
                }

                result = _handle_identifier(parser_state, token)

        self.assertEqual(result["type"], "ERROR")
        mock_build_error.assert_called_once_with(
            parser_state,
            "函数调用参数解析失败",
            5,
            3
        )

    def test_function_call_multiple_arguments(self):
        """Test: function call with multiple arguments."""
        token = self._create_token("IDENTIFIER", "multi_arg_func", line=10, column=1)
        lparen_token = self._create_token("LPAREN", "(", line=10, column=16)
        rparen_token = self._create_token("RPAREN", ")", line=10, column=30)
        tokens = [token, lparen_token, rparen_token]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_arguments = [
            {"type": "IDENTIFIER", "value": "a", "line": 10, "column": 17},
            {"type": "LITERAL", "value": 123, "line": 10, "column": 20},
            {"type": "CALL", "function": {"type": "IDENTIFIER", "value": "g"}, "arguments": [], "line": 10, "column": 23}
        ]

        with patch("._parse_argument_list_package._parse_argument_list_src._parse_argument_list") as mock_parse_args:
            mock_parse_args.return_value = mock_arguments

            result = _handle_identifier(parser_state, token)

        self.assertEqual(result["type"], "CALL")
        self.assertEqual(len(result["arguments"]), 3)
        self.assertEqual(result["arguments"], mock_arguments)

    def test_pos_mutation_direct(self):
        """Test: parser_state['pos'] is mutated directly."""
        token = self._create_token("IDENTIFIER", "var", line=1, column=1)
        next_token = self._create_token("SEMICOLON", ";", line=1, column=4)
        tokens = [token, next_token]
        parser_state = self._create_parser_state(tokens, pos=0)

        original_pos_ref = parser_state
        _handle_identifier(parser_state, token)

        self.assertEqual(original_pos_ref["pos"], 1)
        self.assertIs(original_pos_ref, parser_state)


if __name__ == "__main__":
    unittest.main()
