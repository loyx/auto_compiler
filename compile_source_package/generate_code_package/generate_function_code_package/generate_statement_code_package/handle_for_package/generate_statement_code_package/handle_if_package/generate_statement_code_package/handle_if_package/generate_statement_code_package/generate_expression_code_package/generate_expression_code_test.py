import unittest
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    
    def test_literal_positive(self):
        """Test literal expression with positive value"""
        expr = {"type": "literal", "value": 42}
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    MOV R0, #42")
    
    def test_literal_zero(self):
        """Test literal expression with zero value"""
        expr = {"type": "literal", "value": 0}
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    MOV R0, #0")
    
    def test_literal_negative(self):
        """Test literal expression with negative value"""
        expr = {"type": "literal", "value": -10}
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    MOV R0, #-10")
    
    def test_variable_exists(self):
        """Test variable expression with existing variable"""
        expr = {"type": "variable", "var_name": "x"}
        var_offsets = {"x": 8}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    LDR R0, [SP, #8]")
    
    def test_variable_missing(self):
        """Test variable expression with missing variable (defaults to offset 0)"""
        expr = {"type": "variable", "var_name": "y"}
        var_offsets = {"x": 8}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    LDR R0, [SP, #0]")
    
    def test_binop_add(self):
        """Test binary operation: addition"""
        expr = {
            "type": "binop",
            "op": "add",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #5",
            "    PUSH {R0}",
            "    MOV R0, #3",
            "    POP {R1}",
            "    ADD R0, R1, R0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_sub(self):
        """Test binary operation: subtraction"""
        expr = {
            "type": "binop",
            "op": "sub",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 4}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #10",
            "    PUSH {R0}",
            "    MOV R0, #4",
            "    POP {R1}",
            "    SUB R0, R1, R0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_mul(self):
        """Test binary operation: multiplication"""
        expr = {
            "type": "binop",
            "op": "mul",
            "left": {"type": "literal", "value": 6},
            "right": {"type": "literal", "value": 7}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #6",
            "    PUSH {R0}",
            "    MOV R0, #7",
            "    POP {R1}",
            "    MUL R0, R1, R0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_div(self):
        """Test binary operation: division"""
        expr = {
            "type": "binop",
            "op": "div",
            "left": {"type": "literal", "value": 20},
            "right": {"type": "literal", "value": 4}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #20",
            "    PUSH {R0}",
            "    MOV R0, #4",
            "    POP {R1}",
            "    SDIV R0, R1, R0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_lt(self):
        """Test binary operation: less than"""
        expr = {
            "type": "binop",
            "op": "lt",
            "left": {"type": "literal", "value": 3},
            "right": {"type": "literal", "value": 5}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #3",
            "    PUSH {R0}",
            "    MOV R0, #5",
            "    POP {R1}",
            "    CMP R1, R0",
            "    MOVLT R0, #1",
            "    MOVGE R0, #0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_gt(self):
        """Test binary operation: greater than"""
        expr = {
            "type": "binop",
            "op": "gt",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 5}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #10",
            "    PUSH {R0}",
            "    MOV R0, #5",
            "    POP {R1}",
            "    CMP R1, R0",
            "    MOVGT R0, #1",
            "    MOVLE R0, #0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_eq(self):
        """Test binary operation: equal"""
        expr = {
            "type": "binop",
            "op": "eq",
            "left": {"type": "literal", "value": 7},
            "right": {"type": "literal", "value": 7}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #7",
            "    PUSH {R0}",
            "    MOV R0, #7",
            "    POP {R1}",
            "    CMP R1, R0",
            "    MOVEQ R0, #1",
            "    MOVNE R0, #0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_and(self):
        """Test binary operation: logical and"""
        expr = {
            "type": "binop",
            "op": "and",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 1}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #1",
            "    PUSH {R0}",
            "    MOV R0, #1",
            "    POP {R1}",
            "    AND R0, R1, R0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_or(self):
        """Test binary operation: logical or"""
        expr = {
            "type": "binop",
            "op": "or",
            "left": {"type": "literal", "value": 0},
            "right": {"type": "literal", "value": 1}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    MOV R0, #0",
            "    PUSH {R0}",
            "    MOV R0, #1",
            "    POP {R1}",
            "    ORR R0, R1, R0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_binop_with_variables(self):
        """Test binary operation with variables"""
        expr = {
            "type": "binop",
            "op": "add",
            "left": {"type": "variable", "var_name": "x"},
            "right": {"type": "variable", "var_name": "y"}
        }
        var_offsets = {"x": 8, "y": 12}
        result = generate_expression_code(expr, var_offsets)
        expected_lines = [
            "    LDR R0, [SP, #8]",
            "    PUSH {R0}",
            "    LDR R0, [SP, #12]",
            "    POP {R1}",
            "    ADD R0, R1, R0"
        ]
        self.assertEqual(result, "\n".join(expected_lines))
    
    def test_nested_expression(self):
        """Test nested binary operations"""
        expr = {
            "type": "binop",
            "op": "add",
            "left": {
                "type": "binop",
                "op": "mul",
                "left": {"type": "literal", "value": 2},
                "right": {"type": "literal", "value": 3}
            },
            "right": {"type": "literal", "value": 4}
        }
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        # Should generate code for (2 * 3) + 4
        self.assertIn("MUL R0, R1, R0", result)
        self.assertIn("ADD R0, R1, R0", result)
        self.assertIn("PUSH {R0}", result)
        self.assertIn("POP {R1}", result)
    
    def test_unknown_expression_type(self):
        """Test error handling for unknown expression type"""
        expr = {"type": "unknown"}
        var_offsets = {}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets)
        self.assertIn("Unknown expression type", str(context.exception))
    
    def test_unknown_operator(self):
        """Test error handling for unknown operator"""
        expr = {
            "type": "binop",
            "op": "unknown_op",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        var_offsets = {}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets)
        self.assertIn("Unknown operator", str(context.exception))
    
    def test_default_literal_value(self):
        """Test literal with missing value defaults to 0"""
        expr = {"type": "literal"}
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    MOV R0, #0")
    
    def test_default_variable_name(self):
        """Test variable with missing var_name defaults to empty string"""
        expr = {"type": "variable"}
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    LDR R0, [SP, #0]")
    
    def test_default_var_offset(self):
        """Test variable lookup with missing offset defaults to 0"""
        expr = {"type": "variable", "var_name": "missing"}
        var_offsets = {}
        result = generate_expression_code(expr, var_offsets)
        self.assertEqual(result, "    LDR R0, [SP, #0]")


if __name__ == "__main__":
    unittest.main()
