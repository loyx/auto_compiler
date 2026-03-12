"""
Unit tests for _check_unary_op function.
Tests the unary operator checking logic for token parsing.
"""

import unittest
from typing import Dict, Any

# Relative import from the same package
from ._check_unary_op_src import _check_unary_op


class TestCheckUnaryOp(unittest.TestCase):
    """Test cases for _check_unary_op function."""

    def test_minus_operator(self):
        """Test MINUS token is recognized as unary operator."""
        token: Dict[str, Any] = {
            "type": "MINUS",
            "value": "-",
            "line": 1,
            "column": 5
        }
        self.assertTrue(_check_unary_op(token))

    def test_plus_operator(self):
        """Test PLUS token is recognized as unary operator."""
        token: Dict[str, Any] = {
            "type": "PLUS",
            "value": "+",
            "line": 1,
            "column": 5
        }
        self.assertTrue(_check_unary_op(token))

    def test_tilde_operator(self):
        """Test TILDE token is recognized as unary operator."""
        token: Dict[str, Any] = {
            "type": "TILDE",
            "value": "~",
            "line": 1,
            "column": 5
        }
        self.assertTrue(_check_unary_op(token))

    def test_not_operator(self):
        """Test NOT token is recognized as unary operator."""
        token: Dict[str, Any] = {
            "type": "NOT",
            "value": "!",
            "line": 1,
            "column": 5
        }
        self.assertTrue(_check_unary_op(token))

    def test_not_keyword_operator(self):
        """Test NOT token with 'not' keyword value is recognized."""
        token: Dict[str, Any] = {
            "type": "NOT",
            "value": "not",
            "line": 1,
            "column": 5
        }
        self.assertTrue(_check_unary_op(token))

    def test_none_token(self):
        """Test None input returns False."""
        self.assertFalse(_check_unary_op(None))

    def test_binary_operator(self):
        """Test binary operator (e.g., STAR) is not recognized as unary."""
        token: Dict[str, Any] = {
            "type": "STAR",
            "value": "*",
            "line": 1,
            "column": 5
        }
        self.assertFalse(_check_unary_op(token))

    def test_identifier_token(self):
        """Test IDENTIFIER token is not recognized as unary."""
        token: Dict[str, Any] = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 5
        }
        self.assertFalse(_check_unary_op(token))

    def test_number_token(self):
        """Test NUMBER token is not recognized as unary."""
        token: Dict[str, Any] = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 5
        }
        self.assertFalse(_check_unary_op(token))

    def test_empty_dict(self):
        """Test empty dict returns False."""
        token: Dict[str, Any] = {}
        self.assertFalse(_check_unary_op(token))

    def test_missing_type_key(self):
        """Test dict without 'type' key returns False."""
        token: Dict[str, Any] = {
            "value": "-",
            "line": 1,
            "column": 5
        }
        self.assertFalse(_check_unary_op(token))

    def test_unknown_operator_type(self):
        """Test unknown operator type returns False."""
        token: Dict[str, Any] = {
            "type": "UNKNOWN_OP",
            "value": "?",
            "line": 1,
            "column": 5
        }
        self.assertFalse(_check_unary_op(token))

    def test_case_sensitive_type(self):
        """Test that type matching is case-sensitive."""
        token: Dict[str, Any] = {
            "type": "minus",  # lowercase
            "value": "-",
            "line": 1,
            "column": 5
        }
        self.assertFalse(_check_unary_op(token))

    def test_minimal_token_dict(self):
        """Test minimal token dict with only type key."""
        token: Dict[str, Any] = {"type": "MINUS"}
        self.assertTrue(_check_unary_op(token))


if __name__ == "__main__":
    unittest.main()
