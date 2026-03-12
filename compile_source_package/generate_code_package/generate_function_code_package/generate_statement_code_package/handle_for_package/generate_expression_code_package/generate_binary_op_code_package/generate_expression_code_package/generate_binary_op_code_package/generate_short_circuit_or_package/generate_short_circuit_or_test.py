#!/usr/bin/env python3
"""Unit tests for generate_short_circuit_or function."""

from unittest.mock import patch

from .generate_short_circuit_or_src import generate_short_circuit_or


class TestGenerateShortCircuitOr:
    """Test cases for generate_short_circuit_or function."""
    
    def test_basic_short_circuit_or(self):
        """Test basic short-circuit OR with simple operands."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 0},
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #0\n", 0),
            ]
            
            code, offset = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert "cbnz x0, L_test_func_skip_0" in code
            assert "L_test_func_skip_0:" in code
            assert label_counter["skip"] == 1
            assert offset == 0
    
    def test_label_counter_increment(self):
        """Test that label counter is properly incremented."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {"skip": 5}
        var_offsets = {}
        next_offset = 10
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 10),
                ("    mov x0, #2\n", 10),
            ]
            
            code, offset = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert "L_test_func_skip_5" in code
            assert label_counter["skip"] == 6
    
    def test_multiple_short_circuit_or_calls(self):
        """Test multiple calls generate unique labels."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0),
                ("    mov x0, #3\n", 0),
                ("    mov x0, #4\n", 0),
            ]
            
            code1, _ = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            code2, _ = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert "L_test_func_skip_0" in code1
            assert "L_test_func_skip_1" in code2
            assert label_counter["skip"] == 2
    
    def test_nested_expressions(self):
        """Test short-circuit OR with nested expressions."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {
                "type": "binary_op",
                "operator": "&&",
                "left": {"type": "literal", "value": 1},
                "right": {"type": "literal", "value": 2},
            },
            "right": {
                "type": "binary_op",
                "operator": "&&",
                "left": {"type": "literal", "value": 3},
                "right": {"type": "literal", "value": 4},
            },
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    ; left nested code\n    mov x0, #1\n", 0),
                ("    ; right nested code\n    mov x0, #2\n", 0),
            ]
            
            code, offset = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert "cbnz x0, L_test_func_skip_0" in code
            assert "L_test_func_skip_0:" in code
            assert "; left nested code" in code
            assert "; right nested code" in code
    
    def test_code_structure_order(self):
        """Test that code follows correct structure: left, cbnz, right, label."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("LEFT_CODE\n", 0),
                ("RIGHT_CODE\n", 0),
            ]
            
            code, _ = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            lines = [line for line in code.split('\n') if line.strip()]
            
            left_idx = next(i for i, line in enumerate(lines) if "LEFT_CODE" in line)
            cbnz_idx = next(i for i, line in enumerate(lines) if "cbnz" in line)
            right_idx = next(i for i, line in enumerate(lines) if "RIGHT_CODE" in line)
            label_idx = next(i for i, line in enumerate(lines) if "L_test_func_skip_0:" in line)
            
            assert left_idx < cbnz_idx < right_idx < label_idx
    
    def test_next_offset_propagation(self):
        """Test that next_offset is properly propagated through calls."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 100
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 105),
                ("    mov x0, #2\n", 110),
            ]
            
            code, offset = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert offset == 110
    
    def test_empty_label_counter(self):
        """Test behavior when label_counter has no skip key."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0),
            ]
            
            code, offset = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert "L_test_func_skip_0" in code
            assert label_counter["skip"] == 1
    
    def test_return_value_format(self):
        """Test that return value is tuple of (code, offset)."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0),
            ]
            
            result = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert isinstance(result, tuple)
            assert len(result) == 2
            assert isinstance(result[0], str)
            assert isinstance(result[1], int)
    
    def test_code_ends_with_newline(self):
        """Test that generated code ends with newline."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0),
            ]
            
            code, _ = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert code.endswith("\n")
    
    def test_var_offsets_unchanged(self):
        """Test that var_offsets is not modified."""
        expr = {
            "type": "binary_op",
            "operator": "||",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {"x": 0, "y": 8}
        next_offset = 0
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_short_circuit_or_package.generate_expr_code_package.generate_expr_code_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0),
            ]
            
            original_var_offsets = var_offsets.copy()
            code, offset = generate_short_circuit_or(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            assert var_offsets == original_var_offsets
