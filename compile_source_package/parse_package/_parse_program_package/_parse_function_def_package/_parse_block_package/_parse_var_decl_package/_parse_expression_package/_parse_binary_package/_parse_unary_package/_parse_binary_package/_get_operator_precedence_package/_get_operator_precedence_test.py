#!/usr/bin/env python3
"""
Unit tests for _get_operator_precedence function.
Tests operator precedence and associativity mapping for all token types.
"""

import unittest
from ._get_operator_precedence_src import _get_operator_precedence


class TestGetOperatorPrecedence(unittest.TestCase):
    """Test cases for _get_operator_precedence function."""

    def test_star_star_operator(self):
        """Test STAR_STAR operator returns precedence 4 with right associativity."""
        token = {"type": "STAR_STAR", "value": "**", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (4, "right"))

    def test_star_operator(self):
        """Test STAR operator returns precedence 3 with left associativity."""
        token = {"type": "STAR", "value": "*", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (3, "left"))

    def test_slash_operator(self):
        """Test SLASH operator returns precedence 3 with left associativity."""
        token = {"type": "SLASH", "value": "/", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (3, "left"))

    def test_percent_operator(self):
        """Test PERCENT operator returns precedence 3 with left associativity."""
        token = {"type": "PERCENT", "value": "%", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (3, "left"))

    def test_plus_operator(self):
        """Test PLUS operator returns precedence 2 with left associativity."""
        token = {"type": "PLUS", "value": "+", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (2, "left"))

    def test_minus_operator(self):
        """Test MINUS operator returns precedence 2 with left associativity."""
        token = {"type": "MINUS", "value": "-", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (2, "left"))

    def test_equal_equal_operator(self):
        """Test EQUAL_EQUAL operator returns precedence 1 with left associativity."""
        token = {"type": "EQUAL_EQUAL", "value": "==", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (1, "left"))

    def test_bang_equal_operator(self):
        """Test BANG_EQUAL operator returns precedence 1 with left associativity."""
        token = {"type": "BANG_EQUAL", "value": "!=", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (1, "left"))

    def test_less_operator(self):
        """Test LESS operator returns precedence 1 with left associativity."""
        token = {"type": "LESS", "value": "<", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (1, "left"))

    def test_greater_operator(self):
        """Test GREATER operator returns precedence 1 with left associativity."""
        token = {"type": "GREATER", "value": ">", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (1, "left"))

    def test_less_equal_operator(self):
        """Test LESS_EQUAL operator returns precedence 1 with left associativity."""
        token = {"type": "LESS_EQUAL", "value": "<=", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (1, "left"))

    def test_greater_equal_operator(self):
        """Test GREATER_EQUAL operator returns precedence 1 with left associativity."""
        token = {"type": "GREATER_EQUAL", "value": ">=", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (1, "left"))

    def test_and_operator(self):
        """Test AND operator returns precedence 0 with left associativity."""
        token = {"type": "AND", "value": "and", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (0, "left"))

    def test_or_operator(self):
        """Test OR operator returns precedence 0 with left associativity."""
        token = {"type": "OR", "value": "or", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (0, "left"))

    def test_non_operator_identifier(self):
        """Test non-operator token (IDENTIFIER) returns precedence -1."""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (-1, "left"))

    def test_non_operator_number(self):
        """Test non-operator token (NUMBER) returns precedence -1."""
        token = {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (-1, "left"))

    def test_non_operator_string(self):
        """Test non-operator token (STRING) returns precedence -1."""
        token = {"type": "STRING", "value": "hello", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (-1, "left"))

    def test_non_operator_unknown_type(self):
        """Test unknown token type returns precedence -1."""
        token = {"type": "UNKNOWN_TYPE", "value": "???", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (-1, "left"))

    def test_empty_token(self):
        """Test empty token dict returns precedence -1."""
        token = {}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (-1, "left"))

    def test_token_missing_type_field(self):
        """Test token without type field returns precedence -1."""
        token = {"value": "test", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (-1, "left"))

    def test_token_with_empty_type(self):
        """Test token with empty type string returns precedence -1."""
        token = {"type": "", "value": "test", "line": 1, "column": 5}
        result = _get_operator_precedence(token)
        self.assertEqual(result, (-1, "left"))

    def test_token_ignores_extra_fields(self):
        """Test that extra fields in token do not affect result."""
        token = {
            "type": "PLUS",
            "value": "+",
            "line": 10,
            "column": 20,
            "extra_field": "ignored",
            "another": 123
        }
        result = _get_operator_precedence(token)
        self.assertEqual(result, (2, "left"))

    def test_precedence_ordering(self):
        """Test that precedence levels are correctly ordered (higher number = higher precedence)."""
        operators_by_precedence = [
            ("STAR_STAR", 4),
            ("STAR", 3),
            ("SLASH", 3),
            ("PERCENT", 3),
            ("PLUS", 2),
            ("MINUS", 2),
            ("EQUAL_EQUAL", 1),
            ("LESS", 1),
            ("AND", 0),
            ("OR", 0),
        ]
        for op_type, expected_precedence in operators_by_precedence:
            token = {"type": op_type, "value": "op", "line": 1, "column": 1}
            result = _get_operator_precedence(token)
            self.assertEqual(result[0], expected_precedence,
                           f"Precedence for {op_type} should be {expected_precedence}")

    def test_all_operators_are_left_associative_except_star_star(self):
        """Test that all operators except STAR_STAR are left associative."""
        left_associative_ops = [
            "STAR", "SLASH", "PERCENT",
            "PLUS", "MINUS",
            "EQUAL_EQUAL", "BANG_EQUAL", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL",
            "AND", "OR"
        ]
        for op_type in left_associative_ops:
            token = {"type": op_type, "value": "op", "line": 1, "column": 1}
            result = _get_operator_precedence(token)
            self.assertEqual(result[1], "left",
                           f"{op_type} should be left associative")

        # Verify STAR_STAR is right associative
        token = {"type": "STAR_STAR", "value": "**", "line": 1, "column": 1}
        result = _get_operator_precedence(token)
        self.assertEqual(result[1], "right", "STAR_STAR should be right associative")


if __name__ == "__main__":
    unittest.main()
