# === test file for _handle_literal ===
"""Unit tests for _handle_literal function."""

from ._handle_literal_src import _handle_literal


class TestHandleLiteralInt:
    """Test cases for integer literal handling."""

    def test_positive_int(self) -> None:
        """Test positive integer literal."""
        expr = {"type": "LITERAL", "value": 42}
        asm_code, next_offset, result_reg = _handle_literal(expr, 0)
        
        assert asm_code == "    mov x0, #42"
        assert next_offset == 0
        assert result_reg == "x0"

    def test_negative_int(self) -> None:
        """Test negative integer literal."""
        expr = {"type": "LITERAL", "value": -10}
        asm_code, next_offset, result_reg = _handle_literal(expr, 5)
        
        assert asm_code == "    mov x0, #-10"
        assert next_offset == 5
        assert result_reg == "x0"

    def test_zero_int(self) -> None:
        """Test zero integer literal."""
        expr = {"type": "LITERAL", "value": 0}
        asm_code, next_offset, result_reg = _handle_literal(expr, 10)
        
        assert asm_code == "    mov x0, #0"
        assert next_offset == 10
        assert result_reg == "x0"

    def test_large_int(self) -> None:
        """Test large integer literal."""
        expr = {"type": "LITERAL", "value": 999999}
        asm_code, next_offset, result_reg = _handle_literal(expr, 0)
        
        assert asm_code == "    mov x0, #999999"
        assert next_offset == 0
        assert result_reg == "x0"


class TestHandleLiteralFloat:
    """Test cases for float literal handling."""

    def test_float_zero(self) -> None:
        """Test float 0.0 literal - uses fmov instruction."""
        expr = {"type": "LITERAL", "value": 0.0}
        asm_code, next_offset, result_reg = _handle_literal(expr, 0)
        
        assert asm_code == "    fmov v0, #0.0"
        assert next_offset == 0
        assert result_reg == "v0"

    def test_float_positive(self) -> None:
        """Test positive float literal - uses ldr instruction."""
        expr = {"type": "LITERAL", "value": 3.14}
        asm_code, next_offset, result_reg = _handle_literal(expr, 0)
        
        assert asm_code == "    ldr v0, =3.14"
        assert next_offset == 0
        assert result_reg == "v0"

    def test_float_negative(self) -> None:
        """Test negative float literal - uses ldr instruction."""
        expr = {"type": "LITERAL", "value": -2.5}
        asm_code, next_offset, result_reg = _handle_literal(expr, 3)
        
        assert asm_code == "    ldr v0, =-2.5"
        assert next_offset == 3
        assert result_reg == "v0"

    def test_float_small_value(self) -> None:
        """Test small float value."""
        expr = {"type": "LITERAL", "value": 0.001}
        asm_code, next_offset, result_reg = _handle_literal(expr, 0)
        
        assert asm_code == "    ldr v0, =0.001"
        assert next_offset == 0
        assert result_reg == "v0"

    def test_float_large_value(self) -> None:
        """Test large float value."""
        expr = {"type": "LITERAL", "value": 123456.789}
        asm_code, next_offset, result_reg = _handle_literal(expr, 0)
        
        assert asm_code == "    ldr v0, =123456.789"
        assert next_offset == 0
        assert result_reg == "v0"


class TestHandleLiteralEdgeCases:
    """Edge case tests for _handle_literal."""

    def test_next_offset_unchanged(self) -> None:
        """Verify next_offset is passed through unchanged for all literal types."""
        # Test with int
        expr_int = {"type": "LITERAL", "value": 100}
        _, offset_int, _ = _handle_literal(expr_int, 42)
        assert offset_int == 42
        
        # Test with float 0.0
        expr_float_zero = {"type": "LITERAL", "value": 0.0}
        _, offset_float_zero, _ = _handle_literal(expr_float_zero, 42)
        assert offset_float_zero == 42
        
        # Test with float non-zero
        expr_float = {"type": "LITERAL", "value": 1.5}
        _, offset_float, _ = _handle_literal(expr_float, 42)
        assert offset_float == 42

    def test_missing_value_key(self) -> None:
        """Test that missing 'value' key raises KeyError."""
        expr = {"type": "LITERAL"}  # Missing 'value' key
        try:
            _handle_literal(expr, 0)
            assert False, "Expected KeyError"
        except KeyError:
            pass

    def test_result_register_type_consistency(self) -> None:
        """Verify result register type matches value type."""
        # Int should use x0
        expr_int = {"type": "LITERAL", "value": 5}
        _, _, reg_int = _handle_literal(expr_int, 0)
        assert reg_int == "x0"
        
        # Float should use v0
        expr_float = {"type": "LITERAL", "value": 5.0}
        _, _, reg_float = _handle_literal(expr_float, 0)
        assert reg_float == "v0"

    def test_asm_code_format(self) -> None:
        """Verify assembly code has proper indentation."""
        expr_int = {"type": "LITERAL", "value": 1}
        asm_int, _, _ = _handle_literal(expr_int, 0)
        assert asm_int.startswith("    ")  # 4 spaces indentation
        
        expr_float = {"type": "LITERAL", "value": 1.0}
        asm_float, _, _ = _handle_literal(expr_float, 0)
        assert asm_float.startswith("    ")  # 4 spaces indentation
