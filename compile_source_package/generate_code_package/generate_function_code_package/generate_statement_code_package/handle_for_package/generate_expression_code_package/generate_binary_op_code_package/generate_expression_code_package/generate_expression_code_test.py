import unittest
from unittest.mock import patch

from .generate_expression_code_src import generate_expression_code, _generate_literal_code, _generate_variable_code


class TestGenerateLiteralCode(unittest.TestCase):
    """Test cases for _generate_literal_code helper function."""

    def test_bool_true_literal(self):
        """Test generating code for boolean True literal."""
        expr = {"type": "LITERAL", "value": True}
        code, next_offset = _generate_literal_code(expr, 10)
        
        self.assertEqual(code, "MOV x0, #1")
        self.assertEqual(next_offset, 10)

    def test_bool_false_literal(self):
        """Test generating code for boolean False literal."""
        expr = {"type": "LITERAL", "value": False}
        code, next_offset = _generate_literal_code(expr, 10)
        
        self.assertEqual(code, "MOV x0, #0")
        self.assertEqual(next_offset, 10)

    def test_int_literal_zero(self):
        """Test generating code for integer 0 literal."""
        expr = {"type": "LITERAL", "value": 0}
        code, next_offset = _generate_literal_code(expr, 5)
        
        self.assertEqual(code, "MOV x0, #0")
        self.assertEqual(next_offset, 5)

    def test_int_literal_positive(self):
        """Test generating code for positive integer literal."""
        expr = {"type": "LITERAL", "value": 42}
        code, next_offset = _generate_literal_code(expr, 10)
        
        self.assertEqual(code, "MOV x0, #42")
        self.assertEqual(next_offset, 10)

    def test_int_literal_negative(self):
        """Test generating code for negative integer literal."""
        expr = {"type": "LITERAL", "value": -10}
        code, next_offset = _generate_literal_code(expr, 10)
        
        self.assertEqual(code, "MOV x0, #-10")
        self.assertEqual(next_offset, 10)

    def test_float_literal_raises(self):
        """Test that float literals raise ValueError."""
        expr = {"type": "LITERAL", "value": 3.14}
        
        with self.assertRaises(ValueError) as context:
            _generate_literal_code(expr, 10)
        
        self.assertIn("Float literals not supported", str(context.exception))

    def test_string_literal_raises(self):
        """Test that string literals raise ValueError."""
        expr = {"type": "LITERAL", "value": "hello"}
        
        with self.assertRaises(ValueError) as context:
            _generate_literal_code(expr, 10)
        
        self.assertIn("String literals not supported", str(context.exception))

    def test_none_literal_raises(self):
        """Test that None literal raises ValueError."""
        expr = {"type": "LITERAL", "value": None}
        
        with self.assertRaises(ValueError) as context:
            _generate_literal_code(expr, 10)
        
        self.assertIn("Unsupported literal value type", str(context.exception))

    def test_list_literal_raises(self):
        """Test that list literal raises ValueError."""
        expr = {"type": "LITERAL", "value": [1, 2, 3]}
        
        with self.assertRaises(ValueError) as context:
            _generate_literal_code(expr, 10)
        
        self.assertIn("Unsupported literal value type", str(context.exception))


class TestGenerateVariableCode(unittest.TestCase):
    """Test cases for _generate_variable_code helper function."""

    def test_existing_variable(self):
        """Test generating code for existing variable."""
        expr = {"type": "VARIABLE", "name": "x"}
        var_offsets = {"x": 16, "y": 24}
        
        code, next_offset = _generate_variable_code(expr, var_offsets, 10)
        
        self.assertEqual(code, "LDR x0, [sp, #16]")
        self.assertEqual(next_offset, 10)

    def test_variable_at_offset_zero(self):
        """Test generating code for variable at offset 0."""
        expr = {"type": "VARIABLE", "name": "param"}
        var_offsets = {"param": 0}
        
        code, next_offset = _generate_variable_code(expr, var_offsets, 5)
        
        self.assertEqual(code, "LDR x0, [sp, #0]")
        self.assertEqual(next_offset, 5)

    def test_unknown_variable_raises(self):
        """Test that unknown variable raises ValueError."""
        expr = {"type": "VARIABLE", "name": "unknown_var"}
        var_offsets = {"x": 16, "y": 24}
        
        with self.assertRaises(ValueError) as context:
            _generate_variable_code(expr, var_offsets, 10)
        
        self.assertIn("Unknown variable: unknown_var", str(context.exception))

    def test_empty_var_offsets_raises(self):
        """Test that empty var_offsets raises ValueError for any variable."""
        expr = {"type": "VARIABLE", "name": "any_var"}
        var_offsets = {}
        
        with self.assertRaises(ValueError) as context:
            _generate_variable_code(expr, var_offsets, 10)
        
        self.assertIn("Unknown variable: any_var", str(context.exception))


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code main function."""

    def test_literal_expression_dispatch(self):
        """Test that LITERAL type dispatches to literal handler."""
        expr = {"type": "LITERAL", "value": 42}
        label_counter = {}
        var_offsets = {}
        
        code, next_offset = generate_expression_code(
            expr, "test_func", label_counter, var_offsets, 10
        )
        
        self.assertEqual(code, "MOV x0, #42")
        self.assertEqual(next_offset, 10)

    def test_bool_literal_expression(self):
        """Test boolean literal expression."""
        expr = {"type": "LITERAL", "value": True}
        
        code, next_offset = generate_expression_code(
            expr, "test_func", {}, {}, 5
        )
        
        self.assertEqual(code, "MOV x0, #1")
        self.assertEqual(next_offset, 5)

    def test_variable_expression_dispatch(self):
        """Test that VARIABLE type dispatches to variable handler."""
        expr = {"type": "VARIABLE", "name": "counter"}
        var_offsets = {"counter": 32}
        
        code, next_offset = generate_expression_code(
            expr, "test_func", {}, var_offsets, 10
        )
        
        self.assertEqual(code, "LDR x0, [sp, #32]")
        self.assertEqual(next_offset, 10)

    @patch('generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code')
    def test_binary_op_expression_dispatch(self, mock_binary_op):
        """Test that BINARY_OP type dispatches to binary op handler."""
        expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        label_counter = {"for_cond": 0}
        var_offsets = {}
        
        mock_binary_op.return_value = ("ADD x0, x1, x2", 15)
        
        code, next_offset = generate_expression_code(
            expr, "test_func", label_counter, var_offsets, 10
        )
        
        mock_binary_op.assert_called_once_with(
            expr, "test_func", label_counter, var_offsets, 10
        )
        self.assertEqual(code, "ADD x0, x1, x2")
        self.assertEqual(next_offset, 15)

    @patch('generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code')
    def test_binary_op_with_nested_expressions(self, mock_binary_op):
        """Test BINARY_OP with nested left and right expressions."""
        expr = {
            "type": "BINARY_OP",
            "operator": "*",
            "left": {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            },
            "right": {"type": "VARIABLE", "name": "x"}
        }
        label_counter = {}
        var_offsets = {"x": 16}
        
        mock_binary_op.return_value = ("MUL x0, x1, x2", 20)
        
        code, next_offset = generate_expression_code(
            expr, "multiply_func", label_counter, var_offsets, 5
        )
        
        mock_binary_op.assert_called_once()
        self.assertEqual(next_offset, 20)

    def test_unsupported_expression_type_raises(self):
        """Test that unsupported expression type raises ValueError."""
        expr = {"type": "UNARY_OP", "operator": "-", "operand": {"type": "LITERAL", "value": 5}}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {}, {}, 10)
        
        self.assertIn("Unsupported expression type: UNARY_OP", str(context.exception))

    def test_empty_expr_type_raises(self):
        """Test that empty expr dict raises ValueError."""
        expr = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {}, {}, 10)
        
        self.assertIn("Unsupported expression type: None", str(context.exception))

    def test_label_counter_not_modified_for_literal(self):
        """Test that label_counter is not modified for LITERAL expressions."""
        expr = {"type": "LITERAL", "value": 100}
        label_counter = {"for_cond": 5, "true": 3}
        original_counter = label_counter.copy()
        
        generate_expression_code(expr, "test_func", label_counter, {}, 10)
        
        self.assertEqual(label_counter, original_counter)

    def test_label_counter_not_modified_for_variable(self):
        """Test that label_counter is not modified for VARIABLE expressions."""
        expr = {"type": "VARIABLE", "name": "x"}
        var_offsets = {"x": 16}
        label_counter = {"for_end": 2}
        original_counter = label_counter.copy()
        
        generate_expression_code(expr, "test_func", label_counter, var_offsets, 10)
        
        self.assertEqual(label_counter, original_counter)

    @patch('generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code')
    def test_label_counter_may_be_modified_for_binary_op(self, mock_binary_op):
        """Test that label_counter may be modified for BINARY_OP expressions."""
        expr = {
            "type": "BINARY_OP",
            "operator": "&&",
            "left": {"type": "LITERAL", "value": True},
            "right": {"type": "LITERAL", "value": True}
        }
        label_counter = {"false": 0}
        var_offsets = {}
        
        def side_effect(e, fn, lc, vo, no):
            lc["false"] = 1
            return ("CMP x0, #0", no)
        
        mock_binary_op.side_effect = side_effect
        
        generate_expression_code(expr, "test_func", label_counter, var_offsets, 10)
        
        self.assertEqual(label_counter["false"], 1)

    def test_var_offsets_not_modified(self):
        """Test that var_offsets is not modified by generate_expression_code."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets = {"x": 16, "y": 24}
        original_offsets = var_offsets.copy()
        
        generate_expression_code(expr, "test_func", {}, var_offsets, 10)
        
        self.assertEqual(var_offsets, original_offsets)

    def test_next_offset_zero_for_literal(self):
        """Test with next_offset starting at 0 for literal."""
        expr = {"type": "LITERAL", "value": 0}
        
        code, next_offset = generate_expression_code(
            expr, "test_func", {}, {}, 0
        )
        
        self.assertEqual(code, "MOV x0, #0")
        self.assertEqual(next_offset, 0)

    def test_large_int_literal(self):
        """Test with large integer literal."""
        expr = {"type": "LITERAL", "value": 999999}
        
        code, next_offset = generate_expression_code(
            expr, "test_func", {}, {}, 10
        )
        
        self.assertEqual(code, "MOV x0, #999999")
        self.assertEqual(next_offset, 10)


class TestGenerateExpressionCodeIntegration(unittest.TestCase):
    """Integration tests for generate_expression_code with realistic scenarios."""

    @patch('generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code')
    def test_arithmetic_expression(self, mock_binary_op):
        """Test arithmetic expression: 5 + 3."""
        expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        mock_binary_op.return_value = ("MOV x1, #5\nMOV x2, #3\nADD x0, x1, x2", 12)
        
        code, next_offset = generate_expression_code(
            expr, "add_func", {}, {}, 10
        )
        
        self.assertIn("ADD x0, x1, x2", code)

    @patch('generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code')
    def test_comparison_expression(self, mock_binary_op):
        """Test comparison expression: x > 10."""
        expr = {
            "type": "BINARY_OP",
            "operator": ">",
            "left": {"type": "VARIABLE", "name": "x"},
            "right": {"type": "LITERAL", "value": 10}
        }
        var_offsets = {"x": 16}
        mock_binary_op.return_value = ("LDR x1, [sp, #16]\nMOV x2, #10\nCMP x1, x2", 12)
        
        code, next_offset = generate_expression_code(
            expr, "compare_func", {}, var_offsets, 10
        )
        
        self.assertIn("CMP", code)

    @patch('generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code')
    def test_complex_nested_expression(self, mock_binary_op):
        """Test complex nested expression: (a + b) * (c - d)."""
        expr = {
            "type": "BINARY_OP",
            "operator": "*",
            "left": {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "VARIABLE", "name": "a"},
                "right": {"type": "VARIABLE", "name": "b"}
            },
            "right": {
                "type": "BINARY_OP",
                "operator": "-",
                "left": {"type": "VARIABLE", "name": "c"},
                "right": {"type": "VARIABLE", "name": "d"}
            }
        }
        var_offsets = {"a": 16, "b": 24, "c": 32, "d": 40}
        mock_binary_op.return_value = ("MUL x0, x1, x2", 20)
        
        code, next_offset = generate_expression_code(
            expr, "complex_func", {}, var_offsets, 5
        )
        
        mock_binary_op.assert_called_once()
        self.assertEqual(next_offset, 20)


if __name__ == "__main__":
    unittest.main()
