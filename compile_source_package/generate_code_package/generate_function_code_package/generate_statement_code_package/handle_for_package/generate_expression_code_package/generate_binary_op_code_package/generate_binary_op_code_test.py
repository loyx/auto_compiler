import unittest
from unittest.mock import patch

# Relative import from the same package
from .generate_binary_op_code_src import generate_binary_op_code, LabelCounter, VarOffsets, ExprDict


class TestGenerateBinaryOpCode(unittest.TestCase):
    """Test cases for generate_binary_op_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter: LabelCounter = {
            "for_cond": 0,
            "for_end": 0,
            "for_update": 0,
            "skip": 0,
            "true": 0,
            "false": 0,
        }
        self.var_offsets: VarOffsets = {"x": 0, "y": 16}
        self.next_offset = 32

    def test_simple_addition_operator(self):
        """Test BINARY_OP with + operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            # Left operand generates code and returns offset 48
            mock_gen_expr.side_effect = [
                ("mov x0, #5", 48),  # left
                ("mov x0, #3", 64),  # right
            ]
            # Operator instruction
            mock_gen_op.return_value = ("add x0, x1, x0", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            # Verify generate_expression_code was called twice
            self.assertEqual(mock_gen_expr.call_count, 2)
            # Verify generate_operator_instruction was called once
            mock_gen_op.assert_called_once_with("+", self.func_name, self.label_counter, 64)

            # Verify code structure
            self.assertIn("mov x0, #5", code)
            self.assertIn("str x0, [sp, #-16]!", code)
            self.assertIn("mov x0, #3", code)
            self.assertIn("ldr x1, [sp], #16", code)
            self.assertIn("add x0, x1, x0", code)

            # Verify offset calculation: 32 + 16 (push) + 16 (right) - 16 (pop) = 48
            # But mock returned 64 for right, then op kept it at 64
            self.assertEqual(offset, 64)

    def test_subtraction_operator(self):
        """Test BINARY_OP with - operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "-",
            "left": {"type": "VARIABLE", "name": "x"},
            "right": {"type": "LITERAL", "value": 10},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("ldr x0, [sp, #0]", 48),
                ("mov x0, #10", 64),
            ]
            mock_gen_op.return_value = ("sub x0, x1, x0", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("sub x0, x1, x0", code)
            self.assertEqual(offset, 64)

    def test_multiplication_operator(self):
        """Test BINARY_OP with * operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "*",
            "left": {"type": "LITERAL", "value": 4},
            "right": {"type": "LITERAL", "value": 5},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("mov x0, #4", 48),
                ("mov x0, #5", 64),
            ]
            mock_gen_op.return_value = ("mul x0, x1, x0", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("mul x0, x1, x0", code)

    def test_division_operator(self):
        """Test BINARY_OP with / operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("mov x0, #20", 48),
                ("mov x0, #4", 64),
            ]
            mock_gen_op.return_value = ("sdiv x0, x1, x0", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("sdiv x0, x1, x0", code)

    def test_comparison_equal_operator(self):
        """Test BINARY_OP with == operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "==",
            "left": {"type": "VARIABLE", "name": "x"},
            "right": {"type": "LITERAL", "value": 0},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("ldr x0, [sp, #0]", 48),
                ("mov x0, #0", 64),
            ]
            mock_gen_op.return_value = ("cmp x1, x0\nset x0, eq", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("cmp x1, x0", code)

    def test_logical_and_short_circuit(self):
        """Test BINARY_OP with && operator (short-circuit)."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "&&",
            "left": {"type": "VARIABLE", "name": "a"},
            "right": {"type": "VARIABLE", "name": "b"},
        }

        # Create a fresh label counter to verify modification
        label_counter: LabelCounter = {"true": 0, "false": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("ldr x0, [sp, #0]", 48),
                ("ldr x0, [sp, #16]", 64),
            ]
            mock_gen_op.return_value = ("cbz x1, .L_test_func_false_0\n...", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            # Verify && generates short-circuit code
            self.assertIn("cbz x1, .L_test_func_false_0", code)
            # Label counter should be modified in-place for short-circuit
            self.assertEqual(label_counter["false"], 1)

    def test_logical_or_short_circuit(self):
        """Test BINARY_OP with || operator (short-circuit)."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": {"type": "VARIABLE", "name": "a"},
            "right": {"type": "VARIABLE", "name": "b"},
        }

        label_counter: LabelCounter = {"true": 0, "false": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("ldr x0, [sp, #0]", 48),
                ("ldr x0, [sp, #16]", 64),
            ]
            mock_gen_op.return_value = ("cbnz x1, .L_test_func_true_0\n...", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            # Verify || generates short-circuit code
            self.assertIn("cbnz x1, .L_test_func_true_0", code)
            # Label counter should be modified in-place for short-circuit
            self.assertEqual(label_counter["true"], 1)

    def test_bitwise_and_operator(self):
        """Test BINARY_OP with & operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "&",
            "left": {"type": "LITERAL", "value": 15},
            "right": {"type": "LITERAL", "value": 7},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("mov x0, #15", 48),
                ("mov x0, #7", 64),
            ]
            mock_gen_op.return_value = ("and x0, x1, x0", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("and x0, x1, x0", code)

    def test_bitwise_or_operator(self):
        """Test BINARY_OP with | operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "|",
            "left": {"type": "LITERAL", "value": 8},
            "right": {"type": "LITERAL", "value": 4},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("mov x0, #8", 48),
                ("mov x0, #4", 64),
            ]
            mock_gen_op.return_value = ("orr x0, x1, x0", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("orr x0, x1, x0", code)

    def test_nested_binary_operations(self):
        """Test nested BINARY_OP expressions."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {
                "type": "BINARY_OP",
                "operator": "*",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3},
            },
            "right": {"type": "LITERAL", "value": 4},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            # First call handles nested left expression, second handles right literal
            mock_gen_expr.side_effect = [
                ("mov x0, #2\nstr x0, [sp, #-16]!\nmov x0, #3\nldr x1, [sp], #16\nmul x0, x1, x0", 80),
                ("mov x0, #4", 96),
            ]
            mock_gen_op.return_value = ("add x0, x1, x0", 96)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            # Should generate code for nested expression first, then right operand
            self.assertEqual(mock_gen_expr.call_count, 2)
            self.assertIn("add x0, x1, x0", code)

    def test_offset_tracking_with_stack_operations(self):
        """Test that next_offset is correctly tracked through stack push/pop."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }

        initial_offset = 32

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            # Left: 32 -> 48 (offset increases by 16)
            # Push: 48 -> 64 (offset increases by 16)
            # Right: 64 -> 80 (offset increases by 16)
            # Pop: 80 -> 64 (offset decreases by 16)
            # Op: 64 -> 64 (no change)
            mock_gen_expr.side_effect = [
                ("mov x0, #1", 48),
                ("mov x0, #2", 80),
            ]
            mock_gen_op.return_value = ("add x0, x1, x0", 64)

            code, final_offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, initial_offset
            )

            # Verify offset tracking: push adds 16, pop subtracts 16
            # Final should match what generate_operator_instruction returns
            self.assertEqual(final_offset, 64)

    def test_code_line_ordering(self):
        """Test that code lines are in correct order: left, push, right, pop, op."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("LEFT_CODE", 48),
                ("RIGHT_CODE", 64),
            ]
            mock_gen_op.return_value = ("OP_CODE", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            lines = code.split("\n")
            # Verify ordering
            left_idx = next(i for i, line in enumerate(lines) if "LEFT_CODE" in line)
            push_idx = next(i for i, line in enumerate(lines) if "str x0, [sp, #-16]!" in line)
            right_idx = next(i for i, line in enumerate(lines) if "RIGHT_CODE" in line)
            pop_idx = next(i for i, line in enumerate(lines) if "ldr x1, [sp], #16" in line)
            op_idx = next(i for i, line in enumerate(lines) if "OP_CODE" in line)

            self.assertLess(left_idx, push_idx)
            self.assertLess(push_idx, right_idx)
            self.assertLess(right_idx, pop_idx)
            self.assertLess(pop_idx, op_idx)

    def test_empty_code_lines_handling(self):
        """Test handling when expression code generation returns empty strings."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("", 48),
                ("", 64),
            ]
            mock_gen_op.return_value = ("add x0, x1, x0", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            # Should still have stack operations and operator instruction
            self.assertIn("str x0, [sp, #-16]!", code)
            self.assertIn("ldr x1, [sp], #16", code)
            self.assertIn("add x0, x1, x0", code)

    def test_modulo_operator(self):
        """Test BINARY_OP with % operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "%",
            "left": {"type": "LITERAL", "value": 17},
            "right": {"type": "LITERAL", "value": 5},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("mov x0, #17", 48),
                ("mov x0, #5", 64),
            ]
            mock_gen_op.return_value = ("sdiv x2, x1, x0\nmsub x0, x2, x0, x1", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            # Modulo should generate division and multiply-subtract
            self.assertIn("sdiv", code)

    def test_less_than_operator(self):
        """Test BINARY_OP with < operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "<",
            "left": {"type": "VARIABLE", "name": "x"},
            "right": {"type": "LITERAL", "value": 100},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("ldr x0, [sp, #0]", 48),
                ("mov x0, #100", 64),
            ]
            mock_gen_op.return_value = ("cmp x1, x0\nset x0, lt", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("cmp x1, x0", code)

    def test_greater_than_operator(self):
        """Test BINARY_OP with > operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": ">",
            "left": {"type": "VARIABLE", "name": "x"},
            "right": {"type": "LITERAL", "value": 50},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("ldr x0, [sp, #0]", 48),
                ("mov x0, #50", 64),
            ]
            mock_gen_op.return_value = ("cmp x1, x0\nset x0, gt", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("cmp x1, x0", code)

    def test_not_equal_operator(self):
        """Test BINARY_OP with != operator."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "!=",
            "left": {"type": "VARIABLE", "name": "a"},
            "right": {"type": "VARIABLE", "name": "b"},
        }

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("ldr x0, [sp, #0]", 48),
                ("ldr x0, [sp, #16]", 64),
            ]
            mock_gen_op.return_value = ("cmp x1, x0\nset x0, ne", 64)

            code, offset = generate_binary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            self.assertIn("cmp x1, x0", code)

    def test_label_counter_not_modified_for_non_short_circuit(self):
        """Test that label_counter is not modified for non-short-circuit operators."""
        expr: ExprDict = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }

        label_counter: LabelCounter = {"true": 5, "false": 3}
        original_true = label_counter["true"]
        original_false = label_counter["false"]

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr, patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_operator_instruction_package.generate_operator_instruction_src.generate_operator_instruction"
        ) as mock_gen_op:

            mock_gen_expr.side_effect = [
                ("mov x0, #1", 48),
                ("mov x0, #2", 64),
            ]
            mock_gen_op.return_value = ("add x0, x1, x0", 64)

            generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            # Label counter should not be modified for + operator
            self.assertEqual(label_counter["true"], original_true)
            self.assertEqual(label_counter["false"], original_false)


if __name__ == "__main__":
    unittest.main()
