# -*- coding: utf-8 -*-
"""Unit tests for calculate_stack_size function."""

import unittest
from .calculate_stack_size_src import (
    calculate_stack_size,
    _calculate_total_slots,
    _calculate_raw_size,
    _align_to_16_bytes,
)


class TestCalculateTotalSlots(unittest.TestCase):
    """Tests for _calculate_total_slots helper function."""

    def test_zero_params_zero_locals(self):
        """Test with zero parameters and zero local variables."""
        result = _calculate_total_slots(0, 0)
        self.assertEqual(result, 0)

    def test_some_params_zero_locals(self):
        """Test with some parameters and zero local variables."""
        result = _calculate_total_slots(5, 0)
        self.assertEqual(result, 5)

    def test_zero_params_some_locals(self):
        """Test with zero parameters and some local variables."""
        result = _calculate_total_slots(0, 3)
        self.assertEqual(result, 3)

    def test_both_params_and_locals(self):
        """Test with both parameters and local variables."""
        result = _calculate_total_slots(4, 6)
        self.assertEqual(result, 10)


class TestCalculateRawSize(unittest.TestCase):
    """Tests for _calculate_raw_size helper function."""

    def test_zero_slots(self):
        """Test with zero slots."""
        result = _calculate_raw_size(0)
        self.assertEqual(result, 0)

    def test_one_slot(self):
        """Test with one slot (8 bytes)."""
        result = _calculate_raw_size(1)
        self.assertEqual(result, 8)

    def test_multiple_slots(self):
        """Test with multiple slots."""
        result = _calculate_raw_size(10)
        self.assertEqual(result, 80)


class TestAlignTo16Bytes(unittest.TestCase):
    """Tests for _align_to_16_bytes helper function."""

    def test_already_aligned_zero(self):
        """Test zero is already aligned."""
        result = _align_to_16_bytes(0)
        self.assertEqual(result, 0)

    def test_already_aligned_16(self):
        """Test 16 is already aligned."""
        result = _align_to_16_bytes(16)
        self.assertEqual(result, 16)

    def test_already_aligned_32(self):
        """Test 32 is already aligned."""
        result = _align_to_16_bytes(32)
        self.assertEqual(result, 32)

    def test_needs_alignment_8(self):
        """Test 8 needs alignment to 16."""
        result = _align_to_16_bytes(8)
        self.assertEqual(result, 16)

    def test_needs_alignment_24(self):
        """Test 24 needs alignment to 32."""
        result = _align_to_16_bytes(24)
        self.assertEqual(result, 32)

    def test_needs_alignment_40(self):
        """Test 40 needs alignment to 48."""
        result = _align_to_16_bytes(40)
        self.assertEqual(result, 48)


class TestCalculateStackSize(unittest.TestCase):
    """Tests for calculate_stack_size main function."""

    def test_zero_params_zero_locals(self):
        """Test with zero parameters and zero local variables."""
        result = calculate_stack_size(0, 0)
        self.assertEqual(result, 0)

    def test_only_params_aligned(self):
        """Test with only parameters resulting in aligned size."""
        # 2 params = 2 slots = 16 bytes (already aligned)
        result = calculate_stack_size(2, 0)
        self.assertEqual(result, 16)

    def test_only_locals_aligned(self):
        """Test with only local variables resulting in aligned size."""
        # 4 locals = 4 slots = 32 bytes (already aligned)
        result = calculate_stack_size(0, 4)
        self.assertEqual(result, 32)

    def test_params_and_locals_aligned(self):
        """Test with both resulting in aligned size."""
        # 2 params + 2 locals = 4 slots = 32 bytes (already aligned)
        result = calculate_stack_size(2, 2)
        self.assertEqual(result, 32)

    def test_needs_alignment_one_slot(self):
        """Test with one slot needing alignment."""
        # 1 slot = 8 bytes -> aligned to 16
        result = calculate_stack_size(1, 0)
        self.assertEqual(result, 16)

    def test_needs_alignment_three_slots(self):
        """Test with three slots needing alignment."""
        # 3 slots = 24 bytes -> aligned to 32
        result = calculate_stack_size(1, 2)
        self.assertEqual(result, 32)

    def test_needs_alignment_five_slots(self):
        """Test with five slots needing alignment."""
        # 5 slots = 40 bytes -> aligned to 48
        result = calculate_stack_size(2, 3)
        self.assertEqual(result, 48)

    def test_larger_aligned_case(self):
        """Test with larger aligned case."""
        # 8 slots = 64 bytes (already aligned)
        result = calculate_stack_size(4, 4)
        self.assertEqual(result, 64)

    def test_larger_needs_alignment(self):
        """Test with larger case needing alignment."""
        # 9 slots = 72 bytes -> aligned to 80
        result = calculate_stack_size(5, 4)
        self.assertEqual(result, 80)

    def test_alignment_property(self):
        """Test that result is always 16-byte aligned."""
        test_cases = [
            (0, 0), (1, 0), (0, 1), (3, 5), (7, 9), (10, 15),
        ]
        for param_count, local_var_count in test_cases:
            with self.subTest(param_count=param_count, local_var_count=local_var_count):
                result = calculate_stack_size(param_count, local_var_count)
                self.assertEqual(result % 16, 0, f"Result {result} is not 16-byte aligned")


if __name__ == "__main__":
    unittest.main()
