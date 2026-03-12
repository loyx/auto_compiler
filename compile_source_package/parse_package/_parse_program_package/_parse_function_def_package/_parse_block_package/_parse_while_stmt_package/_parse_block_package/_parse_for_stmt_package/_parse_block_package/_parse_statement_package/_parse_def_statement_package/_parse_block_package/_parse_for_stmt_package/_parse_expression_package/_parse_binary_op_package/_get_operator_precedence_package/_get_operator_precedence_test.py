#!/usr/bin/env python3
"""Unit tests for _get_operator_precedence function."""

import unittest
from typing import Any, Dict

from ._get_operator_precedence_src import _get_operator_precedence

Token = Dict[str, Any]


class TestGetOperatorPrecedence(unittest.TestCase):
    """Test cases for _get_operator_precedence function."""

    def test_logical_and_uppercase(self):
        """Test AND operator (uppercase) returns precedence 1."""
        token: Token = {"type": "KEYWORD", "value": "AND", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 1)

    def test_logical_and_lowercase(self):
        """Test and operator (lowercase) returns precedence 1."""
        token: Token = {"type": "KEYWORD", "value": "and", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 1)

    def test_logical_and_mixed_case(self):
        """Test And operator (mixed case) returns precedence 1."""
        token: Token = {"type": "KEYWORD", "value": "And", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 1)

    def test_logical_or_uppercase(self):
        """Test OR operator (uppercase) returns precedence 1."""
        token: Token = {"type": "KEYWORD", "value": "OR", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 1)

    def test_logical_or_lowercase(self):
        """Test or operator (lowercase) returns precedence 1."""
        token: Token = {"type": "KEYWORD", "value": "or", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 1)

    def test_comparison_eq(self):
        """Test == operator returns precedence 2."""
        token: Token = {"type": "OP", "value": "==", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 2)

    def test_comparison_ne(self):
        """Test != operator returns precedence 2."""
        token: Token = {"type": "OP", "value": "!=", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 2)

    def test_comparison_lt(self):
        """Test < operator returns precedence 2."""
        token: Token = {"type": "OP", "value": "<", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 2)

    def test_comparison_gt(self):
        """Test > operator returns precedence 2."""
        token: Token = {"type": "OP", "value": ">", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 2)

    def test_comparison_le(self):
        """Test <= operator returns precedence 2."""
        token: Token = {"type": "OP", "value": "<=", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 2)

    def test_comparison_ge(self):
        """Test >= operator returns precedence 2."""
        token: Token = {"type": "OP", "value": ">=", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 2)

    def test_arithmetic_add(self):
        """Test + operator returns precedence 3."""
        token: Token = {"type": "OP", "value": "+", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 3)

    def test_arithmetic_sub(self):
        """Test - operator returns precedence 3."""
        token: Token = {"type": "OP", "value": "-", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 3)

    def test_arithmetic_mul(self):
        """Test * operator returns precedence 4."""
        token: Token = {"type": "OP", "value": "*", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 4)

    def test_arithmetic_div(self):
        """Test / operator returns precedence 4."""
        token: Token = {"type": "OP", "value": "/", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 4)

    def test_invalid_operator_unknown(self):
        """Test unknown operator returns precedence 0."""
        token: Token = {"type": "OP", "value": "%", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 0)

    def test_invalid_operator_empty_string(self):
        """Test empty string operator returns precedence 0."""
        token: Token = {"type": "OP", "value": "", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 0)

    def test_missing_value_field(self):
        """Test token without value field returns precedence 0."""
        token: Token = {"type": "OP", "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 0)

    def test_empty_token_dict(self):
        """Test empty token dict returns precedence 0."""
        token: Token = {}
        self.assertEqual(_get_operator_precedence(token), 0)

    def test_minimal_token_only_value(self):
        """Test token with only value field works correctly."""
        token: Token = {"value": "+"}
        self.assertEqual(_get_operator_precedence(token), 3)

    def test_none_value_field(self):
        """Test token with None value returns precedence 0."""
        token: Token = {"type": "OP", "value": None, "line": 1, "column": 1}
        self.assertEqual(_get_operator_precedence(token), 0)


if __name__ == "__main__":
    unittest.main()
