import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 0, column: int = 0) -> Dict[str, Any]:
        """Helper to create an AST node."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    def test_no_comparison_operator_returns_left_operand(self):
        """Test when there's no comparison operator - should return left operand as-is."""
        token = self._create_token("IDENTIFIER", "x")
        state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive:
            left_node = self._create_ast_node("IDENTIFIER", "x")
            mock_additive.return_value = (left_node, state)

            result_ast, result_state = _parse_comparison(state)

            self.assertEqual(result_ast, left_node)
            self.assertEqual(result_state["pos"], 0)

    def test_equality_operator(self):
        """Test parsing == operator."""
        left_token = self._create_token("IDENTIFIER", "x", line=1, column=1)
        op_token = self._create_token("OPERATOR", "==", line=1, column=3)
        right_token = self._create_token("NUMBER", "5", line=1, column=6)

        state = {
            "tokens": [left_token, op_token, right_token],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive:
            left_node = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
            right_node = self._create_ast_node("NUMBER", 5, line=1, column=6)

            intermediate_state = {
                "tokens": state["tokens"],
                "pos": 1,
                "filename": "test.py",
                "error": ""
            }
            final_state = {
                "tokens": state["tokens"],
                "pos": 3,
                "filename": "test.py",
                "error": ""
            }

            mock_additive.side_effect = [
                (left_node, intermediate_state),
                (right_node, final_state)
            ]

            result_ast, result_state = _parse_comparison(state)

            self.assertEqual(result_ast["type"], "BINARY_OP")
            self.assertEqual(result_ast["value"], "==")
            self.assertEqual(len(result_ast["children"]), 2)
            self.assertEqual(result_ast["children"][0], left_node)
            self.assertEqual(result_ast["children"][1], right_node)
            self.assertEqual(result_ast["line"], 1)
            self.assertEqual(result_ast["column"], 3)

    def test_all_comparison_operators(self):
        """Test all comparison operators: ==, !=, <, >, <=, >="""
        operators = ["==", "!=", "<", ">", "<=", ">="]

        for op in operators:
            with self.subTest(operator=op):
                left_token = self._create_token("IDENTIFIER", "a")
                op_token = self._create_token("OPERATOR", op)
                right_token = self._create_token("IDENTIFIER", "b")

                state = {
                    "tokens": [left_token, op_token, right_token],
                    "pos": 0,
                    "filename": "test.py",
                    "error": ""
                }

                with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive:
                    left_node = self._create_ast_node("IDENTIFIER", "a")
                    right_node = self._create_ast_node("IDENTIFIER", "b")

                    intermediate_state = {
                        "tokens": state["tokens"],
                        "pos": 1,
                        "filename": "test.py",
                        "error": ""
                    }
                    final_state = {
                        "tokens": state["tokens"],
                        "pos": 3,
                        "filename": "test.py",
                        "error": ""
                    }

                    mock_additive.side_effect = [
                        (left_node, intermediate_state),
                        (right_node, final_state)
                    ]

                    result_ast, result_state = _parse_comparison(state)

                    self.assertEqual(result_ast["type"], "BINARY_OP")
                    self.assertEqual(result_ast["value"], op)

    def test_end_of_tokens(self):
        """Test when position is at or beyond token list length."""
        token = self._create_token("IDENTIFIER", "x")
        state = {
            "tokens": [token],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }

        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive:
            left_node = self._create_ast_node("IDENTIFIER", "x")
            mock_additive.return_value = (left_node, state)

            result_ast, result_state = _parse_comparison(state)

            self.assertEqual(result_ast, left_node)

    def test_non_comparison_operator(self):
        """Test when current token is not a comparison operator."""
        left_token = self._create_token("IDENTIFIER", "x")
        op_token = self._create_token("OPERATOR", "+")
        right_token = self._create_token("NUMBER", "5")

        state = {
            "tokens": [left_token, op_token, right_token],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive:
            left_node = self._create_ast_node("IDENTIFIER", "x")
            mock_additive.return_value = (left_node, state)

            result_ast, result_state = _parse_comparison(state)

            self.assertEqual(result_ast, left_node)
            self.assertEqual(result_state["pos"], 0)

    def test_preserves_parser_state_fields(self):
        """Test that other parser state fields are preserved."""
        left_token = self._create_token("IDENTIFIER", "x")
        op_token = self._create_token("OPERATOR", "==")
        right_token = self._create_token("NUMBER", "5")

        state = {
            "tokens": [left_token, op_token, right_token],
            "pos": 0,
            "filename": "test_file.py",
            "error": ""
        }

        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive:
            left_node = self._create_ast_node("IDENTIFIER", "x")
            right_node = self._create_ast_node("NUMBER", 5)

            intermediate_state = {
                "tokens": state["tokens"],
                "pos": 1,
                "filename": "test_file.py",
                "error": ""
            }
            final_state = {
                "tokens": state["tokens"],
                "pos": 3,
                "filename": "test_file.py",
                "error": ""
            }

            mock_additive.side_effect = [
                (left_node, intermediate_state),
                (right_node, final_state)
            ]

            result_ast, result_state = _parse_comparison(state)

            self.assertEqual(result_state["filename"], "test_file.py")
            self.assertEqual(result_state["error"], "")


if __name__ == "__main__":
    unittest.main()
