import unittest

from .generate_expression_code_src import (
    generate_expression_code,
    _generate_literal_code,
    _generate_ident_code,
    _generate_binary_op_code,
)


class TestGenerateLiteralCode(unittest.TestCase):
    """Tests for _generate_literal_code helper function."""

    def test_literal_zero(self):
        """Test loading literal value 0."""
        expr = {"type": "LITERAL", "value": 0}
        code, offset = _generate_literal_code(expr)
        self.assertEqual(code, "    MOV R0, #0\n")
        self.assertEqual(offset, 0)

    def test_literal_positive(self):
        """Test loading positive literal value."""
        expr = {"type": "LITERAL", "value": 42}
        code, offset = _generate_literal_code(expr)
        self.assertEqual(code, "    MOV R0, #42\n")
        self.assertEqual(offset, 0)

    def test_literal_negative(self):
        """Test loading negative literal value."""
        expr = {"type": "LITERAL", "value": -10}
        code, offset = _generate_literal_code(expr)
        self.assertEqual(code, "    MOV R0, #-10\n")
        self.assertEqual(offset, 0)


class TestGenerateIdentCode(unittest.TestCase):
    """Tests for _generate_ident_code helper function."""

    def test_ident_existing_variable(self):
        """Test loading existing variable from stack."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 8}
        code, offset = _generate_ident_code(expr, var_offsets)
        self.assertEqual(code, "    LDR R0, [SP, #8]\n")
        self.assertEqual(offset, 0)

    def test_ident_variable_at_offset_zero(self):
        """Test loading variable at offset 0."""
        expr = {"type": "IDENT", "name": "y"}
        var_offsets = {"y": 0}
        code, offset = _generate_ident_code(expr, var_offsets)
        self.assertEqual(code, "    LDR R0, [SP, #0]\n")
        self.assertEqual(offset, 0)

    def test_ident_missing_variable(self):
        """Test error when variable not in var_offsets."""
        expr = {"type": "IDENT", "name": "missing"}
        var_offsets = {"x": 8}
        with self.assertRaises(ValueError) as context:
            _generate_ident_code(expr, var_offsets)
        self.assertIn("missing", str(context.exception))
        self.assertIn("not found", str(context.exception))


class TestGenerateBinaryOpCode(unittest.TestCase):
    """Tests for _generate_binary_op_code helper function."""

    def test_binary_add(self):
        """Test addition operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #5\n"
            "    PUSH {R0}\n"
            "    MOV R0, #3\n"
            "    POP {R1}\n"
            "    ADD R0, R1, R0\n"
        )
        self.assertEqual(code, expected)
        self.assertEqual(offset, 0)

    def test_binary_sub(self):
        """Test subtraction operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #10\n"
            "    PUSH {R0}\n"
            "    MOV R0, #4\n"
            "    POP {R1}\n"
            "    SUB R0, R1, R0\n"
        )
        self.assertEqual(code, expected)

    def test_binary_mul(self):
        """Test multiplication operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "*",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #6\n"
            "    PUSH {R0}\n"
            "    MOV R0, #7\n"
            "    POP {R1}\n"
            "    MUL R0, R1, R0\n"
        )
        self.assertEqual(code, expected)

    def test_binary_div(self):
        """Test division operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #20\n"
            "    PUSH {R0}\n"
            "    MOV R0, #4\n"
            "    POP {R1}\n"
            "    SDIV R0, R1, R0\n"
        )
        self.assertEqual(code, expected)

    def test_cmp_equal(self):
        """Test equality comparison (==)."""
        expr = {
            "type": "CMP",
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #5\n"
            "    PUSH {R0}\n"
            "    MOV R0, #5\n"
            "    POP {R1}\n"
            "    CMP R1, R0\n"
            "    MOVEQ R0, #1\n"
            "    MOVNE R0, #0\n"
        )
        self.assertEqual(code, expected)

    def test_cmp_not_equal(self):
        """Test inequality comparison (!=)."""
        expr = {
            "type": "CMP",
            "op": "!=",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #3\n"
            "    PUSH {R0}\n"
            "    MOV R0, #5\n"
            "    POP {R1}\n"
            "    CMP R1, R0\n"
            "    MOVNE R0, #1\n"
            "    MOVEQ R0, #0\n"
        )
        self.assertEqual(code, expected)

    def test_cmp_less_than(self):
        """Test less than comparison (<)."""
        expr = {
            "type": "CMP",
            "op": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #3\n"
            "    PUSH {R0}\n"
            "    MOV R0, #5\n"
            "    POP {R1}\n"
            "    CMP R1, R0\n"
            "    MOVLT R0, #1\n"
            "    MOVGE R0, #0\n"
        )
        self.assertEqual(code, expected)

    def test_cmp_greater_than(self):
        """Test greater than comparison (>)."""
        expr = {
            "type": "CMP",
            "op": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #10\n"
            "    PUSH {R0}\n"
            "    MOV R0, #5\n"
            "    POP {R1}\n"
            "    CMP R1, R0\n"
            "    MOVGT R0, #1\n"
            "    MOVLE R0, #0\n"
        )
        self.assertEqual(code, expected)

    def test_cmp_less_equal(self):
        """Test less than or equal comparison (<=)."""
        expr = {
            "type": "CMP",
            "op": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #5\n"
            "    PUSH {R0}\n"
            "    MOV R0, #5\n"
            "    POP {R1}\n"
            "    CMP R1, R0\n"
            "    MOVLE R0, #1\n"
            "    MOVGT R0, #0\n"
        )
        self.assertEqual(code, expected)

    def test_cmp_greater_equal(self):
        """Test greater than or equal comparison (>=)."""
        expr = {
            "type": "CMP",
            "op": ">=",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    MOV R0, #10\n"
            "    PUSH {R0}\n"
            "    MOV R0, #5\n"
            "    POP {R1}\n"
            "    CMP R1, R0\n"
            "    MOVGE R0, #1\n"
            "    MOVLT R0, #0\n"
        )
        self.assertEqual(code, expected)

    def test_binary_unknown_operator(self):
        """Test error when operator is unknown."""
        expr = {
            "type": "BINARY_OP",
            "op": "%",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 3},
        }
        label_counter = {}
        var_offsets = {}
        with self.assertRaises(ValueError) as context:
            _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        self.assertIn("%", str(context.exception))

    def test_binary_with_ident_operands(self):
        """Test binary operation with variable operands."""
        expr = {
            "type": "BINARY_OP",
            "op": "+",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "IDENT", "name": "y"},
        }
        label_counter = {}
        var_offsets = {"x": 8, "y": 12}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        expected = (
            "    LDR R0, [SP, #8]\n"
            "    PUSH {R0}\n"
            "    LDR R0, [SP, #12]\n"
            "    POP {R1}\n"
            "    ADD R0, R1, R0\n"
        )
        self.assertEqual(code, expected)

    def test_binary_nested_expression(self):
        """Test binary operation with nested binary expression."""
        expr = {
            "type": "BINARY_OP",
            "op": "+",
            "left": {
                "type": "BINARY_OP",
                "op": "*",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3},
            },
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = _generate_binary_op_code(expr, label_counter, var_offsets, 0)
        self.assertIn("MUL R0, R1, R0", code)
        self.assertIn("ADD R0, R1, R0", code)


class TestGenerateExpressionCode(unittest.TestCase):
    """Tests for main generate_expression_code function."""

    def test_expression_literal(self):
        """Test main function with LITERAL expression."""
        expr = {"type": "LITERAL", "value": 100}
        label_counter = {}
        var_offsets = {}
        code, offset = generate_expression_code(expr, "main", label_counter, var_offsets, 0)
        self.assertEqual(code, "    MOV R0, #100\n")
        self.assertEqual(offset, 0)

    def test_expression_ident(self):
        """Test main function with IDENT expression."""
        expr = {"type": "IDENT", "name": "var1"}
        label_counter = {}
        var_offsets = {"var1": 16}
        code, offset = generate_expression_code(expr, "main", label_counter, var_offsets, 0)
        self.assertEqual(code, "    LDR R0, [SP, #16]\n")
        self.assertEqual(offset, 0)

    def test_expression_binary_op(self):
        """Test main function with BINARY_OP expression."""
        expr = {
            "type": "BINARY_OP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = generate_expression_code(expr, "main", label_counter, var_offsets, 0)
        self.assertIn("ADD R0, R1, R0", code)

    def test_expression_cmp(self):
        """Test main function with CMP expression."""
        expr = {
            "type": "CMP",
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5},
        }
        label_counter = {}
        var_offsets = {}
        code, offset = generate_expression_code(expr, "main", label_counter, var_offsets, 0)
        self.assertIn("CMP R1, R0", code)
        self.assertIn("MOVEQ R0, #1", code)

    def test_expression_unknown_type(self):
        """Test error when expression type is unknown."""
        expr = {"type": "UNKNOWN_TYPE"}
        label_counter = {}
        var_offsets = {}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "main", label_counter, var_offsets, 0)
        self.assertIn("UNKNOWN_TYPE", str(context.exception))

    def test_expression_complex_nested(self):
        """Test complex nested expression with mixed types."""
        expr = {
            "type": "CMP",
            "op": ">",
            "left": {
                "type": "BINARY_OP",
                "op": "+",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "LITERAL", "value": 10},
            },
            "right": {
                "type": "BINARY_OP",
                "op": "*",
                "left": {"type": "IDENT", "name": "b"},
                "right": {"type": "LITERAL", "value": 2},
            },
        }
        label_counter = {}
        var_offsets = {"a": 8, "b": 12}
        code, offset = generate_expression_code(expr, "main", label_counter, var_offsets, 0)
        self.assertIn("LDR R0, [SP, #8]", code)
        self.assertIn("LDR R0, [SP, #12]", code)
        self.assertIn("ADD R0, R1, R0", code)
        self.assertIn("MUL R0, R1, R0", code)
        self.assertIn("MOVGT R0, #1", code)

    def test_func_name_not_used(self):
        """Test that func_name parameter doesn't affect output (not used in current impl)."""
        expr = {"type": "LITERAL", "value": 42}
        label_counter = {}
        var_offsets = {}
        code1, _ = generate_expression_code(expr, "func1", label_counter, var_offsets, 0)
        code2, _ = generate_expression_code(expr, "func2", label_counter, var_offsets, 0)
        self.assertEqual(code1, code2)

    def test_next_offset_returned_unchanged(self):
        """Test that next_offset is returned unchanged."""
        expr = {"type": "LITERAL", "value": 1}
        label_counter = {}
        var_offsets = {}
        _, offset = generate_expression_code(expr, "main", label_counter, var_offsets, 99)
        self.assertEqual(offset, 99)


if __name__ == "__main__":
    unittest.main()
