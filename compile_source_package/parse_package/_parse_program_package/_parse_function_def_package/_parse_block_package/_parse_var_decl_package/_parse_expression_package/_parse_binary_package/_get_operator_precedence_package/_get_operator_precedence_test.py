# -*- coding: utf-8 -*-
"""Unit tests for _get_operator_precedence function."""

import unittest
from typing import Tuple

from ._get_operator_precedence_src import _get_operator_precedence


class TestGetOperatorPrecedence(unittest.TestCase):
    """Test cases for _get_operator_precedence function."""

    def test_assignment_operators_right_associative(self):
        """Test assignment operators have precedence 10 and are right associative."""
        assignment_ops = [
            "EQUAL",
            "PLUS_EQUAL",
            "MINUS_EQUAL",
            "STAR_EQUAL",
            "SLASH_EQUAL",
            "PERCENT_EQUAL",
        ]
        for op in assignment_ops:
            with self.subTest(operator=op):
                result: Tuple[int, bool] = _get_operator_precedence(op)
                self.assertEqual(result, (10, True))

    def test_logical_or_operators_left_associative(self):
        """Test logical OR operators have precedence 20 and are left associative."""
        or_ops = ["OR", "LOGICAL_OR"]
        for op in or_ops:
            with self.subTest(operator=op):
                result: Tuple[int, bool] = _get_operator_precedence(op)
                self.assertEqual(result, (20, False))

    def test_logical_and_operators_left_associative(self):
        """Test logical AND operators have precedence 30 and are left associative."""
        and_ops = ["AND", "LOGICAL_AND"]
        for op in and_ops:
            with self.subTest(operator=op):
                result: Tuple[int, bool] = _get_operator_precedence(op)
                self.assertEqual(result, (30, False))

    def test_comparison_operators_left_associative(self):
        """Test comparison operators have precedence 40 and are left associative."""
        comparison_ops = [
            "EQUAL_EQUAL",
            "NOT_EQUAL",
            "LESS",
            "GREATER",
            "LESS_EQUAL",
            "GREATER_EQUAL",
            "IN",
            "IS",
        ]
        for op in comparison_ops:
            with self.subTest(operator=op):
                result: Tuple[int, bool] = _get_operator_precedence(op)
                self.assertEqual(result, (40, False))

    def test_additive_operators_left_associative(self):
        """Test additive operators have precedence 50 and are left associative."""
        additive_ops = ["PLUS", "MINUS"]
        for op in additive_ops:
            with self.subTest(operator=op):
                result: Tuple[int, bool] = _get_operator_precedence(op)
                self.assertEqual(result, (50, False))

    def test_multiplicative_operators_left_associative(self):
        """Test multiplicative operators have precedence 60 and are left associative."""
        multiplicative_ops = ["STAR", "SLASH", "PERCENT"]
        for op in multiplicative_ops:
            with self.subTest(operator=op):
                result: Tuple[int, bool] = _get_operator_precedence(op)
                self.assertEqual(result, (60, False))

    def test_power_operators_right_associative(self):
        """Test power operators have precedence 70 and are right associative."""
        power_ops = ["POWER", "STAR_STAR"]
        for op in power_ops:
            with self.subTest(operator=op):
                result: Tuple[int, bool] = _get_operator_precedence(op)
                self.assertEqual(result, (70, True))

    def test_non_operator_returns_default(self):
        """Test that non-operator token types return (0, False)."""
        non_operators = [
            "IDENTIFIER",
            "NUMBER",
            "STRING",
            "LPAREN",
            "RPAREN",
            "LBRACE",
            "RBRACE",
            "COMMA",
            "SEMICOLON",
            "",
            "UNKNOWN_OPERATOR",
        ]
        for token in non_operators:
            with self.subTest(token=token):
                result: Tuple[int, bool] = _get_operator_precedence(token)
                self.assertEqual(result, (0, False))

    def test_return_type_is_tuple(self):
        """Test that the return type is always a tuple of (int, bool)."""
        test_tokens = ["PLUS", "EQUAL", "POWER", "IDENTIFIER"]
        for token in test_tokens:
            with self.subTest(token=token):
                result = _get_operator_precedence(token)
                self.assertIsInstance(result, tuple)
                self.assertEqual(len(result), 2)
                self.assertIsInstance(result[0], int)
                self.assertIsInstance(result[1], bool)

    def test_precedence_ordering(self):
        """Test that precedence levels follow expected ordering (higher binds tighter)."""
        # Verify the precedence hierarchy: power > multiplicative > additive > comparison > and > or > assignment
        power_prec = _get_operator_precedence("POWER")[0]
        mult_prec = _get_operator_precedence("STAR")[0]
        add_prec = _get_operator_precedence("PLUS")[0]
        comp_prec = _get_operator_precedence("EQUAL_EQUAL")[0]
        and_prec = _get_operator_precedence("AND")[0]
        or_prec = _get_operator_precedence("OR")[0]
        assign_prec = _get_operator_precedence("EQUAL")[0]
        non_op_prec = _get_operator_precedence("IDENTIFIER")[0]

        self.assertGreater(power_prec, mult_prec)
        self.assertGreater(mult_prec, add_prec)
        self.assertGreater(add_prec, comp_prec)
        self.assertGreater(comp_prec, and_prec)
        self.assertGreater(and_prec, or_prec)
        self.assertGreater(or_prec, assign_prec)
        self.assertGreater(assign_prec, non_op_prec)


if __name__ == "__main__":
    unittest.main()
