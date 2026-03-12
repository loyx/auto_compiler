# -*- coding: utf-8 -*-
"""Unit tests for handle_while function."""

from typing import Dict
from unittest.mock import patch

# Relative import from the same package
from .handle_while_src import handle_while, _generate_expression_code


class TestHandleWhile:
    """Test cases for handle_while function."""

    def test_basic_while_loop(self):
        """Test basic while loop with condition and single body statement."""
        stmt = {
            "condition": {"type": "binary", "op": "<", "left": {"var": "i"}, "right": {"value": 10}},
            "body": [
                {"type": "ASSIGN", "var_name": "i", "value": {"type": "binary", "op": "+", "left": {"var": "i"}, "right": {"value": 1}}}
            ]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets = {"i": 0}
        next_offset = 0

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', return_value=("    @ body statement\n    mov r0, #1", 1)):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Verify label counter was updated
        assert label_counter["while_cond"] == 1
        assert label_counter["while_end"] == 1

        # Verify assembly structure
        assert "test_func_while_cond_0:" in assembly_code
        assert "test_func_while_end_0:" in assembly_code
        assert "cmp r0, #0" in assembly_code
        assert "beq test_func_while_end_0" in assembly_code
        assert "b test_func_while_cond_0" in assembly_code

    def test_while_loop_with_multiple_body_statements(self):
        """Test while loop with multiple statements in body."""
        stmt = {
            "condition": {"type": "binary", "op": "!=", "left": {"var": "x"}, "right": {"value": 0}},
            "body": [
                {"type": "ASSIGN", "var_name": "a", "value": {"value": 1}},
                {"type": "ASSIGN", "var_name": "b", "value": {"value": 2}},
                {"type": "ASSIGN", "var_name": "c", "value": {"value": 3}}
            ]
        }
        func_name = "loop_func"
        label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        var_offsets = {"x": 0, "a": 4, "b": 8, "c": 12}
        next_offset = 16

        mock_statements = [
            ("    @ stmt 1", 20),
            ("    @ stmt 2", 24),
            ("    @ stmt 3", 28)
        ]

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', side_effect=mock_statements):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Verify offset was updated through body processing
        assert offset == 28

        # Verify all body statements are in the assembly
        assert "@ stmt 1" in assembly_code
        assert "@ stmt 2" in assembly_code
        assert "@ stmt 3" in assembly_code

    def test_while_loop_with_existing_label_counter(self):
        """Test while loop when label counter already has values."""
        stmt = {
            "condition": {"type": "literal", "value": True},
            "body": []
        }
        func_name = "my_func"
        label_counter: Dict[str, int] = {"while_cond": 2, "while_end": 3, "if_end": 1}
        var_offsets = {}
        next_offset = 0

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', return_value=("", 0)):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Verify labels use the counter values before increment
        assert "my_func_while_cond_2:" in assembly_code
        assert "my_func_while_end_3:" in assembly_code

        # Verify label counter was incremented
        assert label_counter["while_cond"] == 3
        assert label_counter["while_end"] == 4
        # Other counters should remain unchanged
        assert label_counter["if_end"] == 1

    def test_while_loop_with_empty_body(self):
        """Test while loop with empty body."""
        stmt = {
            "condition": {"type": "literal", "value": False},
            "body": []
        }
        func_name = "empty_loop"
        label_counter: Dict[str, int] = {}
        var_offsets = {}
        next_offset = 0

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', return_value=("", 0)):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Should still have proper structure even with empty body
        assert "empty_loop_while_cond_0:" in assembly_code
        assert "empty_loop_while_end_0:" in assembly_code
        assert "cmp r0, #0" in assembly_code
        assert "beq empty_loop_while_end_0" in assembly_code
        assert "b empty_loop_while_cond_0" in assembly_code

    def test_while_loop_with_nested_while(self):
        """Test while loop with nested while statement in body."""
        stmt = {
            "condition": {"type": "literal", "value": True},
            "body": [
                {
                    "type": "WHILE",
                    "condition": {"type": "literal", "value": True},
                    "body": []
                }
            ]
        }
        func_name = "outer"
        label_counter: Dict[str, int] = {}
        var_offsets = {}
        next_offset = 0

        # Nested while should also allocate labels
        def mock_generate_statement_code(s, fn, lc, vo, off):
            if s.get("type") == "WHILE":
                # Simulate nested while processing
                cond_counter = lc.get("while_cond", 0)
                end_counter = lc.get("while_end", 0)
                lc["while_cond"] = cond_counter + 1
                lc["while_end"] = end_counter + 1
                return (f"    @ nested while {cond_counter}", off)
            return ("", off)

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', side_effect=mock_generate_statement_code):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Outer while should have allocated labels
        assert label_counter["while_cond"] >= 1
        assert label_counter["while_end"] >= 1

    def test_while_loop_offset_propagation(self):
        """Test that offset is properly propagated through body statements."""
        stmt = {
            "condition": {"type": "literal", "value": True},
            "body": [
                {"type": "ASSIGN", "var_name": "a", "value": {"value": 1}},
                {"type": "ASSIGN", "var_name": "b", "value": {"value": 2}}
            ]
        }
        func_name = "offset_test"
        label_counter: Dict[str, int] = {}
        var_offsets = {"a": 0, "b": 4}
        next_offset = 100

        # Mock statements that increment offset
        call_count = [0]

        def mock_gen_stmt(s, fn, lc, vo, off):
            call_count[0] += 1
            return (f"    @ stmt {call_count[0]}", off + 4)

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', side_effect=mock_gen_stmt):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Offset should be incremented by each statement (100 + 4 + 4 = 108)
        assert offset == 108

    def test_while_loop_missing_condition(self):
        """Test while loop with missing condition field."""
        stmt = {
            "body": [{"type": "ASSIGN", "var_name": "x", "value": {"value": 1}}]
        }
        func_name = "no_cond"
        label_counter: Dict[str, int] = {}
        var_offsets = {"x": 0}
        next_offset = 0

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', return_value=("", 0)):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Should still generate valid structure with empty condition handling
        assert "no_cond_while_cond_0:" in assembly_code
        assert "no_cond_while_end_0:" in assembly_code

    def test_while_loop_missing_body(self):
        """Test while loop with missing body field."""
        stmt = {
            "condition": {"type": "literal", "value": True}
        }
        func_name = "no_body"
        label_counter: Dict[str, int] = {}
        var_offsets = {}
        next_offset = 0

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', return_value=("", 0)):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Should still generate valid structure
        assert "no_body_while_cond_0:" in assembly_code
        assert "no_body_while_end_0:" in assembly_code
        assert "b no_body_while_cond_0" in assembly_code

    def test_label_counter_mutation(self):
        """Test that label_counter is mutated in-place."""
        stmt = {
            "condition": {"type": "literal", "value": True},
            "body": []
        }
        func_name = "mutation_test"
        label_counter: Dict[str, int] = {"while_cond": 5, "while_end": 5}
        var_offsets = {}
        next_offset = 0

        original_id = id(label_counter)

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', return_value=("", 0)):
            handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        # Verify same object was mutated
        assert id(label_counter) == original_id
        assert label_counter["while_cond"] == 6
        assert label_counter["while_end"] == 6

    def test_assembly_code_format(self):
        """Test that assembly code has proper formatting."""
        stmt = {
            "condition": {"type": "literal", "value": True},
            "body": []
        }
        func_name = "format_test"
        label_counter: Dict[str, int] = {}
        var_offsets = {}
        next_offset = 0

        with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_src.generate_statement_code', return_value=("", 0)):
            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        assembly_code, offset = result

        # Verify code is a string with newlines
        assert isinstance(assembly_code, str)
        assert "\n" in assembly_code

        # Verify instructions are indented
        lines = assembly_code.split("\n")
        for line in lines:
            if line and not line.endswith(":"):
                # Non-label lines should be indented
                assert line.startswith("    ") or line.startswith("    @")


class TestGenerateExpressionCode:
    """Test cases for _generate_expression_code helper function."""

    def test_expression_code_placeholder(self):
        """Test that expression code generator returns placeholder."""
        expr = {"type": "binary", "op": "+", "left": {"value": 1}, "right": {"value": 2}}
        func_name = "test"
        label_counter: Dict[str, int] = {}
        var_offsets = {}
        next_offset = 42

        result = _generate_expression_code(expr, func_name, label_counter, var_offsets, next_offset)

        code, offset = result

        # Placeholder should not modify offset
        assert offset == next_offset
        # Should contain placeholder comment
        assert "@ evaluate expression" in code or "placeholder" in code.lower()
