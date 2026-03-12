#!/usr/bin/env python3
"""Unit tests for generate_binop function."""

import unittest

from .generate_binop_src import generate_binop, LabelCounter


class TestGenerateBinopArithmetic(unittest.TestCase):
    """Test arithmetic operators."""

    def test_add_operator(self):
        """Test addition operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("+", label_counter)
        self.assertEqual(result, "add r0, r1, r0")
        self.assertEqual(label_counter, {})

    def test_subtract_operator(self):
        """Test subtraction operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("-", label_counter)
        self.assertEqual(result, "sub r0, r1, r0")
        self.assertEqual(label_counter, {})

    def test_multiply_operator(self):
        """Test multiplication operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("*", label_counter)
        self.assertEqual(result, "mul r0, r1, r0")
        self.assertEqual(label_counter, {})

    def test_divide_operator(self):
        """Test division operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("/", label_counter)
        self.assertEqual(result, "sdiv r0, r1, r0")
        self.assertEqual(label_counter, {})


class TestGenerateBinopComparison(unittest.TestCase):
    """Test comparison operators."""

    def test_equal_operator(self):
        """Test equality operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("==", label_counter)
        expected = (
            "cmp r1, r0\n"
            "moveq r0, #1\n"
            "movne r0, #0"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {})

    def test_not_equal_operator(self):
        """Test inequality operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("!=", label_counter)
        expected = (
            "cmp r1, r0\n"
            "movne r0, #1\n"
            "moveq r0, #0"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {})

    def test_less_than_operator(self):
        """Test less than operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("<", label_counter)
        expected = (
            "cmp r1, r0\n"
            "movlt r0, #1\n"
            "movge r0, #0"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {})

    def test_greater_than_operator(self):
        """Test greater than operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop(">", label_counter)
        expected = (
            "cmp r1, r0\n"
            "movgt r0, #1\n"
            "movle r0, #0"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {})

    def test_less_than_or_equal_operator(self):
        """Test less than or equal operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop("<=", label_counter)
        expected = (
            "cmp r1, r0\n"
            "movle r0, #1\n"
            "movgt r0, #0"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {})

    def test_greater_than_or_equal_operator(self):
        """Test greater than or equal operator generates correct assembly."""
        label_counter: LabelCounter = {}
        result = generate_binop(">=", label_counter)
        expected = (
            "cmp r1, r0\n"
            "movge r0, #1\n"
            "movlt r0, #0"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {})


class TestGenerateBinopLogical(unittest.TestCase):
    """Test logical operators with short-circuit evaluation."""

    def test_and_operator_first_usage(self):
        """Test AND operator with first usage (counter=0)."""
        label_counter: LabelCounter = {}
        result = generate_binop("and", label_counter)
        expected = (
            "cmp r1, #0\n"
            "beq _and_false_0\n"
            "cmp r0, #0\n"
            "beq _and_false_0\n"
            "mov r0, #1\n"
            "b _and_end_0\n"
            "_and_false_0:\n"
            "mov r0, #0\n"
            "_and_end_0:"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {"and": 1})

    def test_and_operator_second_usage(self):
        """Test AND operator with second usage (counter=1)."""
        label_counter: LabelCounter = {"and": 1}
        result = generate_binop("and", label_counter)
        expected = (
            "cmp r1, #0\n"
            "beq _and_false_1\n"
            "cmp r0, #0\n"
            "beq _and_false_1\n"
            "mov r0, #1\n"
            "b _and_end_1\n"
            "_and_false_1:\n"
            "mov r0, #0\n"
            "_and_end_1:"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {"and": 2})

    def test_and_operator_with_existing_counter(self):
        """Test AND operator preserves other counter fields."""
        label_counter: LabelCounter = {"while_cond": 5, "and": 3}
        result = generate_binop("and", label_counter)
        self.assertIn("_and_false_3", result)
        self.assertIn("_and_end_3", result)
        self.assertEqual(label_counter, {"while_cond": 5, "and": 4})

    def test_or_operator_first_usage(self):
        """Test OR operator with first usage (counter=0)."""
        label_counter: LabelCounter = {}
        result = generate_binop("or", label_counter)
        expected = (
            "cmp r1, #0\n"
            "bne _or_true_0\n"
            "cmp r0, #0\n"
            "bne _or_true_0\n"
            "mov r0, #0\n"
            "b _or_end_0\n"
            "_or_true_0:\n"
            "mov r0, #1\n"
            "_or_end_0:"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {"or": 1})

    def test_or_operator_second_usage(self):
        """Test OR operator with second usage (counter=1)."""
        label_counter: LabelCounter = {"or": 1}
        result = generate_binop("or", label_counter)
        expected = (
            "cmp r1, #0\n"
            "bne _or_true_1\n"
            "cmp r0, #0\n"
            "bne _or_true_1\n"
            "mov r0, #0\n"
            "b _or_end_1\n"
            "_or_true_1:\n"
            "mov r0, #1\n"
            "_or_end_1:"
        )
        self.assertEqual(result, expected)
        self.assertEqual(label_counter, {"or": 2})

    def test_or_operator_with_existing_counter(self):
        """Test OR operator preserves other counter fields."""
        label_counter: LabelCounter = {"if_end": 10, "or": 2}
        result = generate_binop("or", label_counter)
        self.assertIn("_or_true_2", result)
        self.assertIn("_or_end_2", result)
        self.assertEqual(label_counter, {"if_end": 10, "or": 3})

    def test_mixed_and_or_operators(self):
        """Test mixed AND and OR operators increment各自 counters."""
        label_counter: LabelCounter = {}
        result_and = generate_binop("and", label_counter)
        result_or = generate_binop("or", label_counter)
        result_and2 = generate_binop("and", label_counter)
        
        self.assertIn("_and_false_0", result_and)
        self.assertIn("_or_true_0", result_or)
        self.assertIn("_and_false_1", result_and2)
        self.assertEqual(label_counter, {"and": 2, "or": 1})


class TestGenerateBinopErrorCases(unittest.TestCase):
    """Test error handling for invalid inputs."""

    def test_unknown_operator_raises_value_error(self):
        """Test that unknown operator raises ValueError."""
        label_counter: LabelCounter = {}
        with self.assertRaises(ValueError) as context:
            generate_binop("%", label_counter)
        self.assertIn("Unknown binary operator: %", str(context.exception))
        self.assertEqual(label_counter, {})

    def test_empty_string_operator_raises_value_error(self):
        """Test that empty string operator raises ValueError."""
        label_counter: LabelCounter = {}
        with self.assertRaises(ValueError) as context:
            generate_binop("", label_counter)
        self.assertIn("Unknown binary operator: ", str(context.exception))

    def test_invalid_string_operator_raises_value_error(self):
        """Test that invalid string operator raises ValueError."""
        label_counter: LabelCounter = {}
        with self.assertRaises(ValueError) as context:
            generate_binop("invalid", label_counter)
        self.assertIn("Unknown binary operator: invalid", str(context.exception))
        self.assertEqual(label_counter, {})

    def test_unknown_operator_does_not_modify_counter(self):
        """Test that unknown operator does not modify label_counter."""
        label_counter: LabelCounter = {"and": 5}
        try:
            generate_binop("^^", label_counter)
        except ValueError:
            pass
        self.assertEqual(label_counter, {"and": 5})


class TestGenerateBinopEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_label_counter_starts_at_zero_when_missing(self):
        """Test that label counter defaults to 0 when key is missing."""
        label_counter: LabelCounter = {}
        result = generate_binop("and", label_counter)
        self.assertIn("_and_false_0", result)
        self.assertEqual(label_counter["and"], 1)

    def test_label_counter_with_high_existing_value(self):
        """Test label counter with high existing value."""
        label_counter: LabelCounter = {"and": 100}
        result = generate_binop("and", label_counter)
        self.assertIn("_and_false_100", result)
        self.assertIn("_and_end_100", result)
        self.assertEqual(label_counter["and"], 101)

    def test_result_is_string_type(self):
        """Test that all operators return string type."""
        label_counter: LabelCounter = {}
        operators = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "and", "or"]
        for op in operators:
            result = generate_binop(op, label_counter.copy())
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)

    def test_arithmetic_operators_do_not_modify_counter(self):
        """Test that arithmetic operators do not modify label_counter."""
        label_counter: LabelCounter = {"while_cond": 3}
        original = label_counter.copy()
        for op in ["+", "-", "*", "/"]:
            generate_binop(op, label_counter)
            self.assertEqual(label_counter, original)

    def test_comparison_operators_do_not_modify_counter(self):
        """Test that comparison operators do not modify label_counter."""
        label_counter: LabelCounter = {"if_end": 7}
        original = label_counter.copy()
        for op in ["==", "!=", "<", ">", "<=", ">="]:
            generate_binop(op, label_counter)
            self.assertEqual(label_counter, original)


if __name__ == "__main__":
    unittest.main()
