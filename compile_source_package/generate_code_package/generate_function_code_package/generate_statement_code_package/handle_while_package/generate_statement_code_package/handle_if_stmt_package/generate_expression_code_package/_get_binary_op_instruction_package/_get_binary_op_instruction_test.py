# -*- coding: utf-8 -*-
"""
Unit tests for _get_binary_op_instruction function.
Tests ARM64 assembly instruction generation for binary operators.
"""

import pytest
from ._get_binary_op_instruction_src import _get_binary_op_instruction


class TestGetBinaryOpInstruction:
    """Test suite for _get_binary_op_instruction function."""

    # ==================== Comparison Operators ====================

    def test_eq_operator(self):
        """Test equality operator returns cmp+cset with eq condition."""
        result = _get_binary_op_instruction("eq")
        assert result == "cmp x1, x0\ncset x0, eq\n"

    def test_ne_operator(self):
        """Test not-equal operator returns cmp+cset with ne condition."""
        result = _get_binary_op_instruction("ne")
        assert result == "cmp x1, x0\ncset x0, ne\n"

    def test_lt_operator(self):
        """Test less-than operator returns cmp+cset with lt condition."""
        result = _get_binary_op_instruction("lt")
        assert result == "cmp x1, x0\ncset x0, lt\n"

    def test_le_operator(self):
        """Test less-than-or-equal operator returns cmp+cset with le condition."""
        result = _get_binary_op_instruction("le")
        assert result == "cmp x1, x0\ncset x0, le\n"

    def test_gt_operator(self):
        """Test greater-than operator returns cmp+cset with gt condition."""
        result = _get_binary_op_instruction("gt")
        assert result == "cmp x1, x0\ncset x0, gt\n"

    def test_ge_operator(self):
        """Test greater-than-or-equal operator returns cmp+cset with ge condition."""
        result = _get_binary_op_instruction("ge")
        assert result == "cmp x1, x0\ncset x0, ge\n"

    # ==================== Logical Operators ====================

    def test_and_operator(self):
        """Test logical AND operator returns and instruction."""
        result = _get_binary_op_instruction("and")
        assert result == "and x0, x1, x0\n"

    def test_or_operator(self):
        """Test logical OR operator returns orr instruction."""
        result = _get_binary_op_instruction("or")
        assert result == "orr x0, x1, x0\n"

    # ==================== Arithmetic Operators ====================

    def test_add_operator(self):
        """Test addition operator returns add instruction."""
        result = _get_binary_op_instruction("add")
        assert result == "add x0, x1, x0\n"

    def test_sub_operator(self):
        """Test subtraction operator returns sub instruction."""
        result = _get_binary_op_instruction("sub")
        assert result == "sub x0, x1, x0\n"

    def test_mul_operator(self):
        """Test multiplication operator returns mul instruction."""
        result = _get_binary_op_instruction("mul")
        assert result == "mul x0, x1, x0\n"

    def test_div_operator(self):
        """Test division operator returns udiv instruction."""
        result = _get_binary_op_instruction("div")
        assert result == "udiv x0, x1, x0\n"

    # ==================== Error Cases ====================

    def test_unknown_operator_raises_value_error(self):
        """Test that unknown operator raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            _get_binary_op_instruction("unknown")
        assert "Unknown operator: unknown" in str(exc_info.value)

    def test_empty_string_raises_value_error(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            _get_binary_op_instruction("")
        assert "Unknown operator: " in str(exc_info.value)

    def test_case_sensitive_operator(self):
        """Test that operator matching is case-sensitive."""
        with pytest.raises(ValueError):
            _get_binary_op_instruction("EQ")
        with pytest.raises(ValueError):
            _get_binary_op_instruction("And")
        with pytest.raises(ValueError):
            _get_binary_op_instruction("ADD")

    def test_special_characters_raises_value_error(self):
        """Test that special characters raise ValueError."""
        with pytest.raises(ValueError):
            _get_binary_op_instruction("+")
        with pytest.raises(ValueError):
            _get_binary_op_instruction("-")
        with pytest.raises(ValueError):
            _get_binary_op_instruction("==")
        with pytest.raises(ValueError):
            _get_binary_op_instruction("!=")

    def test_whitespace_raises_value_error(self):
        """Test that whitespace-only strings raise ValueError."""
        with pytest.raises(ValueError):
            _get_binary_op_instruction(" ")
        with pytest.raises(ValueError):
            _get_binary_op_instruction("  add  ")
