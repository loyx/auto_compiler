#!/usr/bin/env python3
"""Unit tests for handle_while_stmt function."""

from typing import Dict
from unittest.mock import patch

# Import the function under test using relative import
from .handle_while_stmt_src import handle_while_stmt


class TestHandleWhileStmt:
    """Test cases for handle_while_stmt function."""

    def test_simple_while_loop(self):
        """Test basic while loop with single body statement."""
        stmt = {
            "condition": {"type": "binary_op", "op": "<", "left": {"type": "var", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": [
                {"type": "assign", "var": "i", "expr": {"type": "binary_op", "op": "+", "left": {"type": "var", "name": "i"}, "right": {"type": "literal", "value": 1}}}
            ]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 1

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            mock_gen_expr.return_value = ("    cmp x0, x1", 1)
            mock_gen_stmt.return_value = ("    add x0, x0, #1", 2)

            assembly_code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify label counter was incremented in-place
            assert label_counter["while_cond"] == 1
            assert label_counter["while_end"] == 1

            # Verify labels are generated correctly
            assert "test_func_while_cond_1:" in assembly_code
            assert "test_func_while_end_1:" in assembly_code

            # Verify loop structure
            assert "    cmp x0, x1" in assembly_code
            assert "    cbz x0, test_func_while_end_1" in assembly_code
            assert "    add x0, x0, #1" in assembly_code
            assert "    b test_func_while_cond_1" in assembly_code

            # Verify offset propagation
            assert new_offset == 2

    def test_multiple_body_statements(self):
        """Test while loop with multiple body statements."""
        stmt = {
            "condition": {"type": "var", "name": "flag"},
            "body": [
                {"type": "assign", "var": "a", "expr": {"type": "literal", "value": 1}},
                {"type": "assign", "var": "b", "expr": {"type": "literal", "value": 2}},
                {"type": "assign", "var": "c", "expr": {"type": "literal", "value": 3}}
            ]
        }
        func_name = "multi_stmt"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets = {"flag": 0, "a": 1, "b": 2, "c": 3}
        next_offset = 4

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            mock_gen_expr.return_value = ("    ldr x0, [sp, #0]", 4)
            mock_gen_stmt.side_effect = [
                ("    mov x0, #1", 5),
                ("    mov x0, #2", 6),
                ("    mov x0, #3", 7)
            ]

            assembly_code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify all three body statements are included
            assert "    mov x0, #1" in assembly_code
            assert "    mov x0, #2" in assembly_code
            assert "    mov x0, #3" in assembly_code

            # Verify final offset
            assert new_offset == 7

    def test_label_counter_increment(self):
        """Test that label counter increments correctly for multiple while loops."""
        stmt = {"condition": {"type": "literal", "value": 1}, "body": []}
        func_name = "loop"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            mock_gen_expr.return_value = ("", 0)
            mock_gen_stmt.return_value = ("", 0)

            # First while loop
            handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            assert label_counter["while_cond"] == 1
            assert label_counter["while_end"] == 1

            # Second while loop
            handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)
            assert label_counter["while_cond"] == 2
            assert label_counter["while_end"] == 2

    def test_empty_body(self):
        """Test while loop with empty body."""
        stmt = {"condition": {"type": "literal", "value": 1}, "body": []}
        func_name = "empty_loop"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #1", 0)

            assembly_code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify structure with empty body
            assert "empty_loop_while_cond_1:" in assembly_code
            assert "    mov x0, #1" in assembly_code
            assert "    cbz x0, empty_loop_while_end_1" in assembly_code
            assert "    b empty_loop_while_cond_1" in assembly_code
            assert "empty_loop_while_end_1:" in assembly_code

            # Empty body should result in empty string between cbz and b
            lines = assembly_code.split("\n")
            cbz_idx = next(i for i, line in enumerate(lines) if "cbz" in line)
            b_idx = next(i for i, line in enumerate(lines) if "    b " in line)
            # There should be no body lines between cbz and b
            assert b_idx == cbz_idx + 2

    def test_custom_initial_counter(self):
        """Test while loop with non-zero initial label counter."""
        stmt = {"condition": {"type": "literal", "value": 1}, "body": []}
        func_name = "custom"
        label_counter: Dict[str, int] = {"while_cond": 5, "while_end": 5}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("", 0)

            assembly_code, _ = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify labels start from 6 (5 + 1)
            assert "custom_while_cond_6:" in assembly_code
            assert "custom_while_end_6:" in assembly_code
            assert label_counter["while_cond"] == 6
            assert label_counter["while_end"] == 6

    def test_next_offset_propagation(self):
        """Test that next_offset is properly propagated through all calls."""
        stmt = {
            "condition": {"type": "literal", "value": 1},
            "body": [
                {"type": "nop"},
                {"type": "nop"}
            ]
        }
        func_name = "offset_test"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            # Expression code increases offset from 0 to 5
            mock_gen_expr.return_value = ("    mov x0, #1", 5)
            # First statement increases offset from 5 to 10
            # Second statement increases offset from 10 to 15
            mock_gen_stmt.side_effect = [
                ("    nop", 10),
                ("    nop", 15)
            ]

            _, final_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify final offset is 15
            assert final_offset == 15

    def test_label_counter_in_place_modification(self):
        """Test that label_counter is modified in-place, not replaced."""
        stmt = {"condition": {"type": "literal", "value": 1}, "body": []}
        func_name = "inplace"
        label_counter: Dict[str, int] = {"while_cond": 3, "while_end": 3}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        # Keep reference to original dict
        original_id = id(label_counter)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("", 0)

            handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify same dict object is modified
            assert id(label_counter) == original_id
            assert label_counter["while_cond"] == 4
            assert label_counter["while_end"] == 4

    def test_assembly_code_structure(self):
        """Test the complete structure of generated assembly code."""
        stmt = {
            "condition": {"type": "literal", "value": 1},
            "body": [{"type": "nop"}]
        }
        func_name = "struct"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            mock_gen_expr.return_value = ("    cond_code", 0)
            mock_gen_stmt.return_value = ("    body_code", 0)

            assembly_code, _ = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            lines = assembly_code.split("\n")

            # Verify exact structure order
            assert lines[0] == "struct_while_cond_1:"
            assert lines[1] == "    cond_code"
            assert lines[2] == "    cbz x0, struct_while_end_1"
            assert lines[3] == "    body_code"
            assert lines[4] == "    b struct_while_cond_1"
            assert lines[5] == "struct_while_end_1:"

    def test_missing_label_counter_keys(self):
        """Test when label_counter doesn't have initial keys (uses get with default)."""
        stmt = {"condition": {"type": "literal", "value": 1}, "body": []}
        func_name = "missing_keys"
        label_counter: Dict[str, int] = {}  # Empty dict
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("", 0)

            assembly_code, _ = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            # Should default to 0 and increment to 1
            assert "missing_keys_while_cond_1:" in assembly_code
            assert "missing_keys_while_end_1:" in assembly_code
            assert label_counter["while_cond"] == 1
            assert label_counter["while_end"] == 1

    def test_complex_condition_expression(self):
        """Test while loop with complex condition expression."""
        stmt = {
            "condition": {
                "type": "binary_op",
                "op": "&&",
                "left": {
                    "type": "binary_op",
                    "op": ">",
                    "left": {"type": "var", "name": "x"},
                    "right": {"type": "literal", "value": 0}
                },
                "right": {
                    "type": "binary_op",
                    "op": "<",
                    "left": {"type": "var", "name": "x"},
                    "right": {"type": "literal", "value": 100}
                }
            },
            "body": [{"type": "assign", "var": "x", "expr": {"type": "var", "name": "x"}}]
        }
        func_name = "complex"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0}
        next_offset = 1

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            mock_gen_expr.return_value = ("    complex_cond_code", 1)
            mock_gen_stmt.return_value = ("    complex_body_code", 2)

            assembly_code, new_offset = handle_while_stmt(stmt, func_name, label_counter, var_offsets, next_offset)

            assert "complex_while_cond_1:" in assembly_code
            assert "    complex_cond_code" in assembly_code
            assert "    cbz x0, complex_while_end_1" in assembly_code
            assert "    complex_body_code" in assembly_code
            assert "    b complex_while_cond_1" in assembly_code
            assert "complex_while_end_1:" in assembly_code
            assert new_offset == 2
