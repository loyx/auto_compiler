"""
Unit tests for evaluate_expression function.
Tests ARM32 assembly code generation for expression evaluation.
"""

import unittest

from .evaluate_expression_src import evaluate_expression


class TestEvaluateExpressionLiteral(unittest.TestCase):
    """Test LITERAL expression type."""
    
    def test_literal_zero(self):
        """Test literal with value 0."""
        expr = {"type": "LITERAL", "value": 0}
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        self.assertEqual(code, "mov r0, #0")
        self.assertEqual(offset, 0)
    
    def test_literal_positive(self):
        """Test literal with positive value."""
        expr = {"type": "LITERAL", "value": 42}
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        self.assertEqual(code, "mov r0, #42")
        self.assertEqual(offset, 0)
    
    def test_literal_negative(self):
        """Test literal with negative value."""
        expr = {"type": "LITERAL", "value": -10}
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        self.assertEqual(code, "mov r0, #-10")
        self.assertEqual(offset, 0)
    
    def test_literal_large_value(self):
        """Test literal with large value."""
        expr = {"type": "LITERAL", "value": 999999}
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        self.assertEqual(code, "mov r0, #999999")
        self.assertEqual(offset, 0)


class TestEvaluateExpressionVar(unittest.TestCase):
    """Test VAR expression type."""
    
    def test_var_simple(self):
        """Test simple variable lookup."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        self.assertEqual(code, "ldr r0, [sp, #8]")
        self.assertEqual(offset, 0)
    
    def test_var_multiple_vars(self):
        """Test variable lookup with multiple variables defined."""
        expr = {"type": "VAR", "name": "y"}
        var_offsets = {"x": 0, "y": 12, "z": 16}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        self.assertEqual(code, "ldr r0, [sp, #12]")
        self.assertEqual(offset, 0)
    
    def test_var_missing_keyerror(self):
        """Test that missing variable raises KeyError."""
        expr = {"type": "VAR", "name": "missing_var"}
        var_offsets = {"x": 0, "y": 4}
        with self.assertRaises(KeyError):
            evaluate_expression(expr, "test_func", var_offsets, 0)
    
    def test_var_zero_offset(self):
        """Test variable with zero offset."""
        expr = {"type": "VAR", "name": "a"}
        var_offsets = {"a": 0}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        self.assertEqual(code, "ldr r0, [sp, #0]")
        self.assertEqual(offset, 0)


class TestEvaluateExpressionBinop(unittest.TestCase):
    """Test BINOP expression type."""
    
    def test_binop_add_literals(self):
        """Test addition of two literals."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #5",
            "str r0, [sp, #0]",
            "mov r0, #3",
            "ldr r1, [sp, #0]",
            "add r0, r0, r1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_sub_literals(self):
        """Test subtraction of two literals."""
        expr = {
            "type": "BINOP",
            "op": "sub",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #10",
            "str r0, [sp, #0]",
            "mov r0, #4",
            "ldr r1, [sp, #0]",
            "sub r0, r0, r1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_mul_literals(self):
        """Test multiplication of two literals."""
        expr = {
            "type": "BINOP",
            "op": "mul",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #6",
            "str r0, [sp, #0]",
            "mov r0, #7",
            "ldr r1, [sp, #0]",
            "mul r0, r0, r1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_div_literals(self):
        """Test division of two literals."""
        expr = {
            "type": "BINOP",
            "op": "div",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #20",
            "str r0, [sp, #0]",
            "mov r0, #4",
            "ldr r1, [sp, #0]",
            "sdiv r0, r0, r1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_mod_literals(self):
        """Test modulo of two literals."""
        expr = {
            "type": "BINOP",
            "op": "mod",
            "left": {"type": "LITERAL", "value": 17},
            "right": {"type": "LITERAL", "value": 5}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #17",
            "str r0, [sp, #0]",
            "mov r0, #5",
            "ldr r1, [sp, #0]",
            "sdiv r2, r0, r1\nmsub r0, r2, r1, r0"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_and_literals(self):
        """Test logical AND of two literals."""
        expr = {
            "type": "BINOP",
            "op": "and",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 1}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #1",
            "str r0, [sp, #0]",
            "mov r0, #1",
            "ldr r1, [sp, #0]",
            "and r0, r0, r1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_or_literals(self):
        """Test logical OR of two literals."""
        expr = {
            "type": "BINOP",
            "op": "or",
            "left": {"type": "LITERAL", "value": 0},
            "right": {"type": "LITERAL", "value": 1}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #0",
            "str r0, [sp, #0]",
            "mov r0, #1",
            "ldr r1, [sp, #0]",
            "orr r0, r0, r1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_eq_comparison(self):
        """Test equality comparison."""
        expr = {
            "type": "BINOP",
            "op": "eq",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #5",
            "str r0, [sp, #0]",
            "mov r0, #5",
            "ldr r1, [sp, #0]",
            "cmp r0, r1\ncset r0, eq"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_ne_comparison(self):
        """Test not-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "ne",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 4}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #3",
            "str r0, [sp, #0]",
            "mov r0, #4",
            "ldr r1, [sp, #0]",
            "cmp r0, r1\ncset r0, ne"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_lt_comparison(self):
        """Test less-than comparison."""
        expr = {
            "type": "BINOP",
            "op": "lt",
            "left": {"type": "LITERAL", "value": 2},
            "right": {"type": "LITERAL", "value": 5}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #2",
            "str r0, [sp, #0]",
            "mov r0, #5",
            "ldr r1, [sp, #0]",
            "cmp r0, r1\ncset r0, lt"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_le_comparison(self):
        """Test less-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "le",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #5",
            "str r0, [sp, #0]",
            "mov r0, #5",
            "ldr r1, [sp, #0]",
            "cmp r0, r1\ncset r0, le"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_gt_comparison(self):
        """Test greater-than comparison."""
        expr = {
            "type": "BINOP",
            "op": "gt",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 3}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #10",
            "str r0, [sp, #0]",
            "mov r0, #3",
            "ldr r1, [sp, #0]",
            "cmp r0, r1\ncset r0, gt"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_ge_comparison(self):
        """Test greater-than-or-equal comparison."""
        expr = {
            "type": "BINOP",
            "op": "ge",
            "left": {"type": "LITERAL", "value": 7},
            "right": {"type": "LITERAL", "value": 7}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #7",
            "str r0, [sp, #0]",
            "mov r0, #7",
            "ldr r1, [sp, #0]",
            "cmp r0, r1\ncset r0, ge"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_unknown_op_valueerror(self):
        """Test that unknown binary operator raises ValueError."""
        expr = {
            "type": "BINOP",
            "op": "unknown_op",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        with self.assertRaises(ValueError):
            evaluate_expression(expr, "test_func", {}, 0)
    
    def test_binop_with_vars(self):
        """Test binary operation with variables."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {"type": "VAR", "name": "x"},
            "right": {"type": "VAR", "name": "y"}
        }
        var_offsets = {"x": 0, "y": 4}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        expected_lines = [
            "ldr r0, [sp, #0]",
            "str r0, [sp, #0]",
            "ldr r0, [sp, #4]",
            "ldr r1, [sp, #0]",
            "add r0, r0, r1"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 4)
    
    def test_binop_nested(self):
        """Test nested binary operations."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {
                "type": "BINOP",
                "op": "mul",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            },
            "right": {"type": "LITERAL", "value": 4}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        # Should evaluate (2 * 3) + 4
        # Offset should increment for nested temps
        self.assertIn("mul r0, r0, r1", code)
        self.assertIn("add r0, r0, r1", code)
        self.assertEqual(offset, 8)  # Two temp slots used


class TestEvaluateExpressionUnop(unittest.TestCase):
    """Test UNOP expression type."""
    
    def test_unop_neg_literal(self):
        """Test negation of a literal."""
        expr = {
            "type": "UNOP",
            "op": "neg",
            "operand": {"type": "LITERAL", "value": 5}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #5",
            "neg r0, r0"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 0)
    
    def test_unop_not_literal(self):
        """Test logical NOT of a literal."""
        expr = {
            "type": "UNOP",
            "op": "not",
            "operand": {"type": "LITERAL", "value": 0}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #0",
            "mvn r0, r0"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 0)
    
    def test_unop_neg_var(self):
        """Test negation of a variable."""
        expr = {
            "type": "UNOP",
            "op": "neg",
            "operand": {"type": "VAR", "name": "x"}
        }
        var_offsets = {"x": 8}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        expected_lines = [
            "ldr r0, [sp, #8]",
            "neg r0, r0"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 0)
    
    def test_unop_not_var(self):
        """Test logical NOT of a variable."""
        expr = {
            "type": "UNOP",
            "op": "not",
            "operand": {"type": "VAR", "name": "flag"}
        }
        var_offsets = {"flag": 12}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        expected_lines = [
            "ldr r0, [sp, #12]",
            "mvn r0, r0"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 0)
    
    def test_unop_unknown_op_valueerror(self):
        """Test that unknown unary operator raises ValueError."""
        expr = {
            "type": "UNOP",
            "op": "unknown_unop",
            "operand": {"type": "LITERAL", "value": 5}
        }
        with self.assertRaises(ValueError):
            evaluate_expression(expr, "test_func", {}, 0)
    
    def test_unop_nested(self):
        """Test nested unary operations."""
        expr = {
            "type": "UNOP",
            "op": "neg",
            "operand": {
                "type": "UNOP",
                "op": "not",
                "operand": {"type": "LITERAL", "value": 0}
            }
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        expected_lines = [
            "mov r0, #0",
            "mvn r0, r0",
            "neg r0, r0"
        ]
        self.assertEqual(code, "\n".join(expected_lines))
        self.assertEqual(offset, 0)


class TestEvaluateExpressionUnknownType(unittest.TestCase):
    """Test unknown expression types."""
    
    def test_unknown_type_valueerror(self):
        """Test that unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN_TYPE"}
        with self.assertRaises(ValueError) as context:
            evaluate_expression(expr, "test_func", {}, 0)
        self.assertIn("Unknown expression type", str(context.exception))
    
    def test_call_type_valueerror(self):
        """Test that CALL type raises ValueError."""
        expr = {"type": "CALL"}
        with self.assertRaises(ValueError):
            evaluate_expression(expr, "test_func", {}, 0)
    
    def test_member_type_valueerror(self):
        """Test that MEMBER type raises ValueError."""
        expr = {"type": "MEMBER"}
        with self.assertRaises(ValueError):
            evaluate_expression(expr, "test_func", {}, 0)


class TestEvaluateExpressionOffsetPropagation(unittest.TestCase):
    """Test offset propagation through nested expressions."""
    
    def test_offset_with_nonzero_start(self):
        """Test evaluation with non-zero starting offset."""
        expr = {"type": "LITERAL", "value": 42}
        code, offset = evaluate_expression(expr, "test_func", {}, 100)
        self.assertEqual(code, "mov r0, #42")
        self.assertEqual(offset, 100)  # Offset unchanged for literal
    
    def test_offset_binop_accumulation(self):
        """Test offset accumulation through binary operations."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        self.assertEqual(offset, 4)  # One temp slot allocated
    
    def test_offset_deeply_nested(self):
        """Test offset with deeply nested expressions."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {
                "type": "BINOP",
                "op": "add",
                "left": {
                    "type": "BINOP",
                    "op": "add",
                    "left": {"type": "LITERAL", "value": 1},
                    "right": {"type": "LITERAL", "value": 2}
                },
                "right": {"type": "LITERAL", "value": 3}
            },
            "right": {"type": "LITERAL", "value": 4}
        }
        code, offset = evaluate_expression(expr, "test_func", {}, 0)
        # Each BINOP allocates a temp slot
        self.assertEqual(offset, 12)  # Three temp slots (4 bytes each)


class TestEvaluateExpressionComplexExpressions(unittest.TestCase):
    """Test complex real-world expression patterns."""
    
    def test_arithmetic_expression(self):
        """Test (a + b) * (c - d)."""
        expr = {
            "type": "BINOP",
            "op": "mul",
            "left": {
                "type": "BINOP",
                "op": "add",
                "left": {"type": "VAR", "name": "a"},
                "right": {"type": "VAR", "name": "b"}
            },
            "right": {
                "type": "BINOP",
                "op": "sub",
                "left": {"type": "VAR", "name": "c"},
                "right": {"type": "VAR", "name": "d"}
            }
        }
        var_offsets = {"a": 0, "b": 4, "c": 8, "d": 12}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        
        # Verify key operations are present
        self.assertIn("add r0, r0, r1", code)
        self.assertIn("sub r0, r0, r1", code)
        self.assertIn("mul r0, r0, r1", code)
        self.assertEqual(offset, 8)  # Two temp slots for the two sub-expressions
    
    def test_comparison_with_logical(self):
        """Test (x > 0) and (y < 10)."""
        expr = {
            "type": "BINOP",
            "op": "and",
            "left": {
                "type": "BINOP",
                "op": "gt",
                "left": {"type": "VAR", "name": "x"},
                "right": {"type": "LITERAL", "value": 0}
            },
            "right": {
                "type": "BINOP",
                "op": "lt",
                "left": {"type": "VAR", "name": "y"},
                "right": {"type": "LITERAL", "value": 10}
            }
        }
        var_offsets = {"x": 0, "y": 4}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        
        # Verify comparison and logical operations
        self.assertIn("cmp r0, r1", code)
        self.assertIn("cset r0, gt", code)
        self.assertIn("cset r0, lt", code)
        self.assertIn("and r0, r0, r1", code)
    
    def test_unary_in_binary(self):
        """Test (-a) + b."""
        expr = {
            "type": "BINOP",
            "op": "add",
            "left": {
                "type": "UNOP",
                "op": "neg",
                "operand": {"type": "VAR", "name": "a"}
            },
            "right": {"type": "VAR", "name": "b"}
        }
        var_offsets = {"a": 0, "b": 4}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        
        self.assertIn("neg r0, r0", code)
        self.assertIn("add r0, r0, r1", code)
        self.assertEqual(offset, 4)
    
    def test_not_condition(self):
        """Test not (x == 0)."""
        expr = {
            "type": "UNOP",
            "op": "not",
            "operand": {
                "type": "BINOP",
                "op": "eq",
                "left": {"type": "VAR", "name": "x"},
                "right": {"type": "LITERAL", "value": 0}
            }
        }
        var_offsets = {"x": 0}
        code, offset = evaluate_expression(expr, "test_func", var_offsets, 0)
        
        self.assertIn("cmp r0, r1", code)
        self.assertIn("cset r0, eq", code)
        self.assertIn("mvn r0, r0", code)


if __name__ == "__main__":
    unittest.main()
