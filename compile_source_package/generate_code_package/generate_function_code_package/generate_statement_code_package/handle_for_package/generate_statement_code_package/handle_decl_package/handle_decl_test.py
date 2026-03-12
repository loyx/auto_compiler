# === std / third-party imports ===
from unittest.mock import patch
import pytest

# === relative imports ===
from .handle_decl_src import handle_decl


class TestHandleDecl:
    """Test suite for handle_decl ARM assembly generator."""

    def test_decl_no_init_value_int(self):
        """Test DECL statement without initialization for int type."""
        stmt = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int",
            "init_value": None
        }
        var_offsets = {}
        
        code, next_offset = handle_decl(
            stmt, "main", {}, var_offsets, 0
        )
        
        assert code == ""
        assert next_offset == 4
        assert var_offsets["x"] == 0

    def test_decl_no_init_value_char(self):
        """Test DECL statement without initialization for char type."""
        stmt = {
            "type": "DECL",
            "var_name": "c",
            "var_type": "char",
            "init_value": None
        }
        var_offsets = {}
        
        code, next_offset = handle_decl(
            stmt, "main", {}, var_offsets, 0
        )
        
        assert code == ""
        assert next_offset == 1
        assert var_offsets["c"] == 0

    def test_decl_no_init_value_double(self):
        """Test DECL statement without initialization for double type."""
        stmt = {
            "type": "DECL",
            "var_name": "d",
            "var_type": "double",
            "init_value": None
        }
        var_offsets = {}
        
        code, next_offset = handle_decl(
            stmt, "main", {}, var_offsets, 0
        )
        
        assert code == ""
        assert next_offset == 8
        assert var_offsets["d"] == 0

    def test_decl_with_init_value_int(self):
        """Test DECL statement with initialization for int type."""
        stmt = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int",
            "init_value": {"type": "LITERAL", "value": 42}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #42", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert "MOV R0, #42" in code
            assert "STR R0, [SP, #0]" in code
            assert next_offset == 4
            assert var_offsets["x"] == 0

    def test_decl_with_init_value_char(self):
        """Test DECL statement with initialization for char type."""
        stmt = {
            "type": "DECL",
            "var_name": "c",
            "var_type": "char",
            "init_value": {"type": "LITERAL", "value": 65}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #65", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert "MOV R0, #65" in code
            assert "STRB R0, [SP, #0]" in code
            assert next_offset == 1
            assert var_offsets["c"] == 0

    def test_decl_with_init_value_short(self):
        """Test DECL statement with initialization for short type."""
        stmt = {
            "type": "DECL",
            "var_name": "s",
            "var_type": "short",
            "init_value": {"type": "LITERAL", "value": 100}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #100", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert "MOV R0, #100" in code
            assert "STRH R0, [SP, #0]" in code
            assert next_offset == 2
            assert var_offsets["s"] == 0

    def test_decl_with_init_value_double(self):
        """Test DECL statement with initialization for double type."""
        stmt = {
            "type": "DECL",
            "var_name": "d",
            "var_type": "double",
            "init_value": {"type": "LITERAL", "value": 3.14}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #3", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert "MOV R0, #3" in code
            assert "STR R0, [SP, #0]" in code
            assert "STR R1, [SP, #4]" in code
            assert next_offset == 8
            assert var_offsets["d"] == 0

    def test_decl_with_init_value_float(self):
        """Test DECL statement with initialization for float type."""
        stmt = {
            "type": "DECL",
            "var_name": "f",
            "var_type": "float",
            "init_value": {"type": "LITERAL", "value": 2.5}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #2", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert "MOV R0, #2" in code
            assert "STR R0, [SP, #0]" in code
            assert next_offset == 4
            assert var_offsets["f"] == 0

    def test_decl_with_init_value_long(self):
        """Test DECL statement with initialization for long type."""
        stmt = {
            "type": "DECL",
            "var_name": "l",
            "var_type": "long",
            "init_value": {"type": "LITERAL", "value": 1000}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1000", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert "MOV R0, #1000" in code
            assert "STR R0, [SP, #0]" in code
            assert next_offset == 4
            assert var_offsets["l"] == 0

    def test_decl_with_init_value_pointer(self):
        """Test DECL statement with initialization for pointer type."""
        stmt = {
            "type": "DECL",
            "var_name": "ptr",
            "var_type": "pointer",
            "init_value": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #0", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert "MOV R0, #0" in code
            assert "STR R0, [SP, #0]" in code
            assert next_offset == 4
            assert var_offsets["ptr"] == 0

    def test_decl_with_non_zero_offset(self):
        """Test DECL statement with non-zero starting offset."""
        stmt = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int",
            "init_value": None
        }
        var_offsets = {}
        
        code, next_offset = handle_decl(
            stmt, "main", {}, var_offsets, 16
        )
        
        assert code == ""
        assert next_offset == 20
        assert var_offsets["x"] == 16

    def test_decl_multiple_variables(self):
        """Test multiple DECL statements updating var_offsets."""
        var_offsets = {}
        
        stmt1 = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int",
            "init_value": None
        }
        stmt2 = {
            "type": "DECL",
            "var_name": "y",
            "var_type": "char",
            "init_value": None
        }
        
        code1, offset1 = handle_decl(stmt1, "main", {}, var_offsets, 0)
        code2, offset2 = handle_decl(stmt2, "main", {}, var_offsets, offset1)
        
        assert var_offsets["x"] == 0
        assert var_offsets["y"] == 4
        assert offset1 == 4
        assert offset2 == 5

    def test_decl_unsupported_type_raises_valueerror(self):
        """Test DECL statement with unsupported type raises ValueError."""
        stmt = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "unsupported_type",
            "init_value": None
        }
        var_offsets = {}
        
        with pytest.raises(ValueError) as exc_info:
            handle_decl(stmt, "main", {}, var_offsets, 0)
        
        assert "Unsupported variable type: unsupported_type" in str(exc_info.value)
        assert "x" not in var_offsets

    def test_decl_default_type_int(self):
        """Test DECL statement with missing var_type defaults to int."""
        stmt = {
            "type": "DECL",
            "var_name": "x",
            "init_value": None
        }
        var_offsets = {}
        
        code, next_offset = handle_decl(
            stmt, "main", {}, var_offsets, 0
        )
        
        assert code == ""
        assert next_offset == 4
        assert var_offsets["x"] == 0

    def test_decl_expression_code_empty(self):
        """Test DECL when generate_expression_code returns empty code."""
        stmt = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int",
            "init_value": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {}
        
        with patch(
            ".generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("", 0)
            
            code, next_offset = handle_decl(
                stmt, "main", {}, var_offsets, 0
            )
            
            assert code == "STR R0, [SP, #0]"
            assert next_offset == 4
            assert var_offsets["x"] == 0

    def test_decl_var_offsets_modified_in_place(self):
        """Test that var_offsets is modified in-place."""
        stmt = {
            "type": "DECL",
            "var_name": "x",
            "var_type": "int",
            "init_value": None
        }
        var_offsets = {"existing_var": 100}
        original_id = id(var_offsets)
        
        handle_decl(stmt, "main", {}, var_offsets, 0)
        
        assert id(var_offsets) == original_id
        assert var_offsets["existing_var"] == 100
        assert var_offsets["x"] == 0
