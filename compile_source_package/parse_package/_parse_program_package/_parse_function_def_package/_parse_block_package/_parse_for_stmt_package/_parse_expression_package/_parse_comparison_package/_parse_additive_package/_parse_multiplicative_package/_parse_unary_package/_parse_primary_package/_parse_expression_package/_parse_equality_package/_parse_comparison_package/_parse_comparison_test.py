# -*- coding: utf-8 -*-
"""Unit tests for _parse_comparison function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Relative import for the function under test
from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_single_term_no_comparison(self):
        """Test parsing a single term without comparison operators."""
        term_ast: Dict[str, Any] = {
            "type": "Identifier",
            "value": "x",
            "line": 1,
            "column": 1
        }

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = [self._create_token("IDENTIFIER", "x")]
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.return_value = term_ast

            result = _parse_comparison(parser_state)

            mock_parse_term.assert_called_once_with(parser_state)
            self.assertEqual(result, term_ast)
            self.assertEqual(parser_state["pos"], 0)

    def test_simple_comparison_less_than(self):
        """Test parsing a simple comparison with < operator."""
        left_term: Dict[str, Any] = {
            "type": "Identifier",
            "value": "a",
            "line": 1,
            "column": 1
        }
        right_term: Dict[str, Any] = {
            "type": "Identifier",
            "value": "b",
            "line": 1,
            "column": 3
        }

        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 3)
        ]

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = tokens
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = [left_term, right_term]

            result = _parse_comparison(parser_state)

            self.assertEqual(mock_parse_term.call_count, 2)
            self.assertEqual(result["type"], "Binary")
            self.assertEqual(result["operator"], "<")
            self.assertEqual(result["left"], left_term)
            self.assertEqual(result["right"], right_term)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 2)
            self.assertEqual(parser_state["pos"], 3)

    def test_simple_comparison_all_operators(self):
        """Test parsing comparisons with all comparison operators."""
        for op in ["<", "<=", ">", ">="]:
            with self.subTest(operator=op):
                left_term: Dict[str, Any] = {
                    "type": "Identifier",
                    "value": "x",
                    "line": 1,
                    "column": 1
                }
                right_term: Dict[str, Any] = {
                    "type": "Number",
                    "value": "5",
                    "line": 1,
                    "column": 3
                }

                tokens = [
                    self._create_token("IDENTIFIER", "x", 1, 1),
                    self._create_token("OPERATOR", op, 1, 2),
                    self._create_token("NUMBER", "5", 1, 3)
                ]

                parser_state = self.base_parser_state.copy()
                parser_state["tokens"] = tokens
                parser_state["pos"] = 0

                with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
                    mock_parse_term.side_effect = [left_term, right_term]

                    result = _parse_comparison(parser_state)

                    self.assertEqual(result["type"], "Binary")
                    self.assertEqual(result["operator"], op)
                    self.assertEqual(parser_state["pos"], 3)

    def test_chained_comparison(self):
        """Test parsing chained comparisons like a < b <= c."""
        term_a: Dict[str, Any] = {
            "type": "Identifier",
            "value": "a",
            "line": 1,
            "column": 1
        }
        term_b: Dict[str, Any] = {
            "type": "Identifier",
            "value": "b",
            "line": 1,
            "column": 3
        }
        term_c: Dict[str, Any] = {
            "type": "Identifier",
            "value": "c",
            "line": 1,
            "column": 6
        }

        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 3),
            self._create_token("OPERATOR", "<=", 1, 5),
            self._create_token("IDENTIFIER", "c", 1, 6)
        ]

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = tokens
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = [term_a, term_b, term_c]

            result = _parse_comparison(parser_state)

            # Should create left-associative tree: (a < b) <= c
            self.assertEqual(result["type"], "Binary")
            self.assertEqual(result["operator"], "<=")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)

            # Left side should be the first comparison: a < b
            left_side = result["left"]
            self.assertEqual(left_side["type"], "Binary")
            self.assertEqual(left_side["operator"], "<")
            self.assertEqual(left_side["left"], term_a)
            self.assertEqual(left_side["right"], term_b)

            # Right side should be c
            self.assertEqual(result["right"], term_c)

            # Position should be at end
            self.assertEqual(parser_state["pos"], 5)

    def test_error_in_first_term(self):
        """Test that error in first term parsing is propagated."""
        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = [self._create_token("IDENTIFIER", "x")]
        parser_state["pos"] = 0
        parser_state["error"] = "Parse error"

        error_ast: Dict[str, Any] = {
            "type": "Error",
            "message": "Parse error"
        }

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.return_value = error_ast

            result = _parse_comparison(parser_state)

            mock_parse_term.assert_called_once()
            self.assertEqual(result, error_ast)
            self.assertEqual(parser_state["error"], "Parse error")

    def test_error_in_second_term(self):
        """Test that error in second term parsing stops comparison."""
        left_term: Dict[str, Any] = {
            "type": "Identifier",
            "value": "a",
            "line": 1,
            "column": 1
        }
        error_ast: Dict[str, Any] = {
            "type": "Error",
            "message": "Term error"
        }

        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "<", 1, 2),
            self._create_token("IDENTIFIER", "b", 1, 3)
        ]

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = tokens
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = [left_term, error_ast]

            result = _parse_comparison(parser_state)

            self.assertEqual(mock_parse_term.call_count, 2)
            self.assertEqual(result, left_term)

    def test_no_tokens(self):
        """Test parsing with empty token list."""
        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = []
        parser_state["pos"] = 0

        empty_ast: Dict[str, Any] = {
            "type": "Empty"
        }

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.return_value = empty_ast

            result = _parse_comparison(parser_state)

            mock_parse_term.assert_called_once()
            self.assertEqual(result, empty_ast)

    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = [self._create_token("IDENTIFIER", "x")]
        parser_state["pos"] = 1  # Already at end

        term_ast: Dict[str, Any] = {
            "type": "Identifier",
            "value": "x"
        }

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.return_value = term_ast

            result = _parse_comparison(parser_state)

            self.assertEqual(result, term_ast)
            self.assertEqual(parser_state["pos"], 1)

    def test_non_comparison_operator(self):
        """Test that non-comparison operators are not consumed."""
        left_term: Dict[str, Any] = {
            "type": "Identifier",
            "value": "a",
            "line": 1,
            "column": 1
        }

        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 2),  # Not a comparison operator
            self._create_token("NUMBER", "1", 1, 3)
        ]

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = tokens
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.return_value = left_term

            result = _parse_comparison(parser_state)

            mock_parse_term.assert_called_once()
            self.assertEqual(result, left_term)
            self.assertEqual(parser_state["pos"], 0)

    def test_position_preserved_on_non_comparison(self):
        """Test that position is not advanced when next token is not comparison operator."""
        left_term: Dict[str, Any] = {
            "type": "Identifier",
            "value": "x"
        }

        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "==", 1, 2),  # Equality, not comparison
            self._create_token("NUMBER", "5", 1, 3)
        ]

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = tokens
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.return_value = left_term

            result = _parse_comparison(parser_state)

            self.assertEqual(result, left_term)
            self.assertEqual(parser_state["pos"], 0)

    def test_line_column_from_operator_token(self):
        """Test that Binary node line/column come from operator token."""
        left_term: Dict[str, Any] = {
            "type": "Identifier",
            "value": "a",
            "line": 1,
            "column": 1
        }
        right_term: Dict[str, Any] = {
            "type": "Number",
            "value": "10",
            "line": 2,
            "column": 1
        }

        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", ">", 2, 5),  # Operator on line 2, column 5
            self._create_token("NUMBER", "10", 2, 1)
        ]

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = tokens
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = [left_term, right_term]

            result = _parse_comparison(parser_state)

            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)

    def test_multiple_chained_comparisons_complex(self):
        """Test complex chained comparison with multiple different operators."""
        terms: List[Dict[str, Any]] = [
            {"type": "Identifier", "value": f"var{i}", "line": 1, "column": i * 2}
            for i in range(1, 5)
        ]
        operators = ["<", "<=", ">", ">="]

        tokens = []
        for i, term in enumerate(terms):
            tokens.append(self._create_token("IDENTIFIER", term["value"], 1, term["column"]))
            if i < len(operators):
                tokens.append(self._create_token("OPERATOR", operators[i], 1, term["column"] + 1))

        parser_state = self.base_parser_state.copy()
        parser_state["tokens"] = tokens
        parser_state["pos"] = 0

        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = terms

            result = _parse_comparison(parser_state)

            # Verify left-associative structure: (((var1 < var2) <= var3) > var4) >= var5
            self.assertEqual(result["operator"], ">=")
            self.assertEqual(result["right"], terms[3])

            left = result["left"]
            self.assertEqual(left["operator"], ">")
            self.assertEqual(left["right"], terms[2])

            left2 = left["left"]
            self.assertEqual(left2["operator"], "<=")
            self.assertEqual(left2["right"], terms[1])

            left3 = left2["left"]
            self.assertEqual(left3["operator"], "<")
            self.assertEqual(left3["left"], terms[0])
            self.assertEqual(left3["right"], terms[1])

            # Position should be at end (4 terms + 3 operators = 7 tokens)
            self.assertEqual(parser_state["pos"], 7)


if __name__ == "__main__":
    unittest.main()
