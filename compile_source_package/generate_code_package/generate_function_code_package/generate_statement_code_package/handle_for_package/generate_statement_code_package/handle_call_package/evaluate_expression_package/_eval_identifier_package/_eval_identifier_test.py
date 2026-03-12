"""Unit tests for _eval_identifier function."""

import pytest

from ._eval_identifier_src import _eval_identifier, VarOffsets


class TestEvalIdentifierHappyPath:
    """Test happy path scenarios for _eval_identifier."""

    def test_single_variable_with_offset(self):
        """Test loading a variable with a specific offset."""
        var_offsets: VarOffsets = {"x": 4}
        result = _eval_identifier("x", var_offsets)
        assert result == "LDR R0, [FP, #-4]"

    def test_variable_with_larger_offset(self):
        """Test loading a variable with a larger offset."""
        var_offsets: VarOffsets = {"y": 16}
        result = _eval_identifier("y", var_offsets)
        assert result == "LDR R0, [FP, #-16]"

    def test_variable_with_zero_offset(self):
        """Test loading a variable with zero offset."""
        var_offsets: VarOffsets = {"z": 0}
        result = _eval_identifier("z", var_offsets)
        assert result == "LDR R0, [FP, #-0]"

    def test_multiple_variables_select_first(self):
        """Test selecting first variable from multiple options."""
        var_offsets: VarOffsets = {"a": 4, "b": 8, "c": 12}
        result = _eval_identifier("a", var_offsets)
        assert result == "LDR R0, [FP, #-4]"

    def test_multiple_variables_select_middle(self):
        """Test selecting middle variable from multiple options."""
        var_offsets: VarOffsets = {"a": 4, "b": 8, "c": 12}
        result = _eval_identifier("b", var_offsets)
        assert result == "LDR R0, [FP, #-8]"

    def test_multiple_variables_select_last(self):
        """Test selecting last variable from multiple options."""
        var_offsets: VarOffsets = {"a": 4, "b": 8, "c": 12}
        result = _eval_identifier("c", var_offsets)
        assert result == "LDR R0, [FP, #-12]"

    def test_variable_with_underscore_in_name(self):
        """Test variable name with underscore."""
        var_offsets: VarOffsets = {"my_var": 20}
        result = _eval_identifier("my_var", var_offsets)
        assert result == "LDR R0, [FP, #-20]"

    def test_variable_with_number_in_name(self):
        """Test variable name with number."""
        var_offsets: VarOffsets = {"var1": 24}
        result = _eval_identifier("var1", var_offsets)
        assert result == "LDR R0, [FP, #-24]"


class TestEvalIdentifierErrorCases:
    """Test error cases for _eval_identifier."""

    def test_undefined_variable_raises_valueerror(self):
        """Test that undefined variable raises ValueError."""
        var_offsets: VarOffsets = {"x": 4}
        with pytest.raises(ValueError) as exc_info:
            _eval_identifier("y", var_offsets)
        assert "Undefined variable: y" in str(exc_info.value)

    def test_undefined_variable_with_empty_dict_raises_valueerror(self):
        """Test that undefined variable with empty dict raises ValueError."""
        var_offsets: VarOffsets = {}
        with pytest.raises(ValueError) as exc_info:
            _eval_identifier("x", var_offsets)
        assert "Undefined variable: x" in str(exc_info.value)

    def test_undefined_variable_error_message_contains_name(self):
        """Test that error message contains the undefined variable name."""
        var_offsets: VarOffsets = {"existing": 8}
        with pytest.raises(ValueError) as exc_info:
            _eval_identifier("nonexistent", var_offsets)
        assert "nonexistent" in str(exc_info.value)

    def test_case_sensitive_variable_lookup(self):
        """Test that variable lookup is case-sensitive."""
        var_offsets: VarOffsets = {"X": 4}
        with pytest.raises(ValueError) as exc_info:
            _eval_identifier("x", var_offsets)
        assert "Undefined variable: x" in str(exc_info.value)


class TestEvalIdentifierEdgeCases:
    """Test edge cases for _eval_identifier."""

    def test_empty_var_offsets_dict(self):
        """Test behavior with empty var_offsets dictionary."""
        var_offsets: VarOffsets = {}
        with pytest.raises(ValueError):
            _eval_identifier("any_var", var_offsets)

    def test_large_offset_value(self):
        """Test with a large offset value."""
        var_offsets: VarOffsets = {"big_var": 1024}
        result = _eval_identifier("big_var", var_offsets)
        assert result == "LDR R0, [FP, #-1024]"

    def test_output_format_no_trailing_newline(self):
        """Test that output has no trailing newline."""
        var_offsets: VarOffsets = {"x": 4}
        result = _eval_identifier("x", var_offsets)
        assert not result.endswith("\n")
        assert result.count("\n") == 0

    def test_output_is_single_line(self):
        """Test that output is a single line."""
        var_offsets: VarOffsets = {"x": 4}
        result = _eval_identifier("x", var_offsets)
        assert "\n" not in result

    def test_output_starts_with_ldr_instruction(self):
        """Test that output starts with LDR instruction."""
        var_offsets: VarOffsets = {"x": 4}
        result = _eval_identifier("x", var_offsets)
        assert result.startswith("LDR")

    def test_output_uses_r0_register(self):
        """Test that output uses R0 register."""
        var_offsets: VarOffsets = {"x": 4}
        result = _eval_identifier("x", var_offsets)
        assert "R0" in result

    def test_output_uses_fp_base_pointer(self):
        """Test that output uses FP base pointer."""
        var_offsets: VarOffsets = {"x": 4}
        result = _eval_identifier("x", var_offsets)
        assert "FP" in result

    def test_output_uses_negative_offset_syntax(self):
        """Test that output uses negative offset syntax."""
        var_offsets: VarOffsets = {"x": 4}
        result = _eval_identifier("x", var_offsets)
        assert "#-" in result
