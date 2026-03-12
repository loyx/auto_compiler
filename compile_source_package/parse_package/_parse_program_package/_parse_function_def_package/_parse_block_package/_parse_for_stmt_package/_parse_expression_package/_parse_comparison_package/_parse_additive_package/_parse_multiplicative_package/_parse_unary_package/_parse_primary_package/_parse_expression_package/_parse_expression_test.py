# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === ADT type aliases ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === Import function under test using relative import ===
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Tests for _parse_expression function"""

    def test_simple_delegation_returns_equality_result(self):
        """Test that _parse_expression delegates to _parse_equality and returns its result"""
        mock_ast: AST = {
            "type": "binary",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": {"type": "number", "value": 2},
            "line": 1,
            "column": 1
        }

        parser_state: ParserState = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast

            result = _parse_expression(parser_state)

            mock_equality.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_error_propagation_from_equality(self):
        """Test that errors set by _parse_equality are preserved in parser_state"""
        parser_state: ParserState = {
            "tokens": [{"type": "INVALID", "value": "?", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }

        error_ast: AST = {"type": "error"}

        def set_error_and_return(state: ParserState) -> AST:
            state["error"] = "Invalid token at position 0"
            state["pos"] = 0
            return error_ast

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = set_error_and_return

            result = _parse_expression(parser_state)

            self.assertEqual(parser_state["error"], "Invalid token at position 0")
            self.assertEqual(result, error_ast)

    def test_position_updated_by_equality(self):
        """Test that parser_state position is updated by _parse_equality"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_ast: AST = {
            "type": "binary",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": {"type": "number", "value": 2}
        }

        def update_pos_and_return(state: ParserState) -> AST:
            state["pos"] = 3
            return mock_ast

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = update_pos_and_return

            result = _parse_expression(parser_state)

            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(result, mock_ast)

    def test_empty_token_list(self):
        """Test handling of empty token list"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        mock_ast: AST = {"type": "empty", "value": None}

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast

            result = _parse_expression(parser_state)

            mock_equality.assert_called_once_with(parser_state)
            self.assertEqual(result, mock_ast)

    def test_single_number_token(self):
        """Test parsing a single number expression"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_ast: AST = {
            "type": "number",
            "value": 42,
            "line": 1,
            "column": 1
        }

        def consume_token_and_return(state: ParserState) -> AST:
            state["pos"] = 1
            return mock_ast

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = consume_token_and_return

            result = _parse_expression(parser_state)

            self.assertEqual(parser_state["pos"], 1)
            self.assertEqual(result["type"], "number")
            self.assertEqual(result["value"], 42)

    def test_complex_nested_expression(self):
        """Test parsing of complex nested expression AST"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
                {"type": "STAR", "value": "*", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        mock_ast: AST = {
            "type": "binary",
            "operator": "*",
            "left": {
                "type": "binary",
                "operator": "+",
                "left": {"type": "number", "value": 1},
                "right": {"type": "number", "value": 2}
            },
            "right": {"type": "number", "value": 3}
        }

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast

            result = _parse_expression(parser_state)

            self.assertEqual(result["type"], "binary")
            self.assertEqual(result["operator"], "*")
            self.assertEqual(result["left"]["operator"], "+")

    def test_parser_state_not_mutated_except_pos_and_error(self):
        """Test that _parse_expression only modifies pos and error in parser_state"""
        parser_state: ParserState = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py",
            "custom_field": "should_not_change"
        }

        original_filename = parser_state["filename"]
        original_tokens = parser_state["tokens"]
        original_custom = parser_state["custom_field"]

        mock_ast: AST = {"type": "number", "value": 1}

        def minimal_update(state: ParserState) -> AST:
            state["pos"] = 1
            return mock_ast

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = minimal_update

            _parse_expression(parser_state)

            self.assertEqual(parser_state["filename"], original_filename)
            self.assertEqual(parser_state["tokens"], original_tokens)
            self.assertEqual(parser_state["custom_field"], original_custom)

    def test_multiple_calls_independent(self):
        """Test that multiple calls to _parse_expression are independent"""
        mock_ast1: AST = {"type": "number", "value": 1}
        mock_ast2: AST = {"type": "number", "value": 2}

        parser_state1: ParserState = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test1.py"
        }

        parser_state2: ParserState = {
            "tokens": [{"type": "NUMBER", "value": "2", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test2.py"
        }

        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = [mock_ast1, mock_ast2]

            result1 = _parse_expression(parser_state1)
            result2 = _parse_expression(parser_state2)

            self.assertEqual(result1["value"], 1)
            self.assertEqual(result2["value"], 2)


if __name__ == "__main__":
    unittest.main()
