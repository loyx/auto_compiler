#!/usr/bin/env python3
"""Unit tests for generate_literal_code function."""

import unittest

from .generate_literal_code_src import generate_literal_code


class TestGenerateLiteralCode(unittest.TestCase):
    """Test cases for generate_literal_code function."""

    def test_bool_true(self) -> None:
        """Test boolean True value generates MOV R0, #1."""
        expr = {"type": "LITERAL", "value": True}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "MOV R0, #1")
        self.assertEqual(reg, 0)

    def test_bool_false(self) -> None:
        """Test boolean False value generates MOV R0, #0."""
        expr = {"type": "LITERAL", "value": False}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "MOV R0, #0")
        self.assertEqual(reg, 0)

    def test_int_zero(self) -> None:
        """Test integer 0 value generates MOV R0, #0."""
        expr = {"type": "LITERAL", "value": 0}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "MOV R0, #0")
        self.assertEqual(reg, 0)

    def test_int_positive_in_range(self) -> None:
        """Test positive integer within range generates MOV."""
        expr = {"type": "LITERAL", "value": 100}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "MOV R0, #100")
        self.assertEqual(reg, 0)

    def test_int_negative_in_range(self) -> None:
        """Test negative integer within range generates MOV."""
        expr = {"type": "LITERAL", "value": -100}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "MOV R0, #-100")
        self.assertEqual(reg, 0)

    def test_int_upper_boundary(self) -> None:
        """Test integer at upper boundary (4095) generates MOV."""
        expr = {"type": "LITERAL", "value": 4095}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "MOV R0, #4095")
        self.assertEqual(reg, 0)

    def test_int_lower_boundary(self) -> None:
        """Test integer at lower boundary (-4095) generates MOV."""
        expr = {"type": "LITERAL", "value": -4095}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "MOV R0, #-4095")
        self.assertEqual(reg, 0)

    def test_int_above_upper_boundary(self) -> None:
        """Test integer above upper boundary (4096) generates LDR."""
        expr = {"type": "LITERAL", "value": 4096}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "LDR R0, =4096")
        self.assertEqual(reg, 0)

    def test_int_below_lower_boundary(self) -> None:
        """Test integer below lower boundary (-4096) generates LDR."""
        expr = {"type": "LITERAL", "value": -4096}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "LDR R0, =-4096")
        self.assertEqual(reg, 0)

    def test_int_large_positive(self) -> None:
        """Test large positive integer generates LDR."""
        expr = {"type": "LITERAL", "value": 1000000}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "LDR R0, =1000000")
        self.assertEqual(reg, 0)

    def test_int_large_negative(self) -> None:
        """Test large negative integer generates LDR."""
        expr = {"type": "LITERAL", "value": -1000000}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "LDR R0, =-1000000")
        self.assertEqual(reg, 0)

    def test_float_positive(self) -> None:
        """Test positive float value generates LDR."""
        expr = {"type": "LITERAL", "value": 3.14}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "LDR R0, =3.14")
        self.assertEqual(reg, 0)

    def test_float_negative(self) -> None:
        """Test negative float value generates LDR."""
        expr = {"type": "LITERAL", "value": -2.5}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "LDR R0, =-2.5")
        self.assertEqual(reg, 0)

    def test_float_zero(self) -> None:
        """Test float 0.0 value generates LDR."""
        expr = {"type": "LITERAL", "value": 0.0}
        code, reg = generate_literal_code(expr)
        self.assertEqual(code, "LDR R0, =0.0")
        self.assertEqual(reg, 0)

    def test_none_value_raises_error(self) -> None:
        """Test None value raises ValueError."""
        expr = {"type": "LITERAL", "value": None}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr)
        self.assertIn("None is not supported", str(context.exception))

    def test_string_value_raises_error(self) -> None:
        """Test string value raises ValueError."""
        expr = {"type": "LITERAL", "value": "hello"}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr)
        self.assertIn("Unsupported literal value type: str", str(context.exception))

    def test_list_value_raises_error(self) -> None:
        """Test list value raises ValueError."""
        expr = {"type": "LITERAL", "value": [1, 2, 3]}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr)
        self.assertIn("Unsupported literal value type: list", str(context.exception))

    def test_dict_value_raises_error(self) -> None:
        """Test dict value raises ValueError."""
        expr = {"type": "LITERAL", "value": {"key": "value"}}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr)
        self.assertIn("Unsupported literal value type: dict", str(context.exception))

    def test_missing_value_key(self) -> None:
        """Test missing 'value' key returns None and raises ValueError."""
        expr = {"type": "LITERAL"}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr)
        self.assertIn("None is not supported", str(context.exception))

    def test_empty_dict(self) -> None:
        """Test empty dict raises ValueError."""
        expr = {}
        with self.assertRaises(ValueError) as context:
            generate_literal_code(expr)
        self.assertIn("None is not supported", str(context.exception))


if __name__ == "__main__":
    unittest.main()
