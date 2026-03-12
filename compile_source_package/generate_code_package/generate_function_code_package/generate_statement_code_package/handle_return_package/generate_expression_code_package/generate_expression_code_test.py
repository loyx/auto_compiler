import unittest

# Relative import from the same package
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""
    
    def test_const_int(self):
        """Test CONST operation with integer value."""
        expr = {"op": "CONST", "value": 42}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "    li x0, 42\n")
    
    def test_const_float(self):
        """Test CONST operation with float value."""
        expr = {"op": "CONST", "value": 3.14}
        result = generate_expression_code(expr, "test_func", {})
        self.assertIn("load float constant 3.14", result)
    
    def test_var_existing(self):
        """Test VAR operation with existing variable."""
        expr = {"op": "VAR", "var_name": "x"}
        var_offsets = {"x": 16}
        result = generate_expression_code(expr, "test_func", var_offsets)
        self.assertEqual(result, "    lw x0, 16(sp)\n")
    
    def test_var_not_found(self):
        """Test VAR operation with non-existent variable raises ValueError."""
        expr = {"op": "VAR", "var_name": "y"}
        var_offsets = {"x": 16}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", var_offsets)
        self.assertIn("y", str(context.exception))
    
    def test_binop_add(self):
        """Test BINOP operation with addition."""
        expr = {
            "op": "BINOP",
            "left": {"op": "CONST", "value": 5},
            "right": {"op": "CONST", "value": 3},
            "operator": "+"
        }
        result = generate_expression_code(expr, "test_func", {})
        self.assertIn("add x0, x1, x0", result)
        self.assertIn("li x0, 5", result)
        self.assertIn("li x0, 3", result)
    
    def test_binop_all_operators(self):
        """Test BINOP with all supported operators."""
        operators = ["+", "-", "*", "/", "%", "&", "|", "^"]
        expected_instructions = {
            "+": "add", "-": "sub", "*": "mul", "/": "div",
            "%": "rem", "&": "and", "|": "or", "^": "xor"
        }
        for op in operators:
            expr = {
                "op": "BINOP",
                "left": {"op": "CONST", "value": 10},
                "right": {"op": "CONST", "value": 2},
                "operator": op
            }
            result = generate_expression_code(expr, "test_func", {})
            self.assertIn(f"{expected_instructions[op]} x0, x1, x0", result)
    
    def test_binop_missing_left(self):
        """Test BINOP operation with missing left operand."""
        expr = {
            "op": "BINOP",
            "right": {"op": "CONST", "value": 3},
            "operator": "+"
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("left", str(context.exception))
    
    def test_binop_missing_right(self):
        """Test BINOP operation with missing right operand."""
        expr = {
            "op": "BINOP",
            "left": {"op": "CONST", "value": 5},
            "operator": "+"
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("right", str(context.exception))
    
    def test_binop_missing_operator(self):
        """Test BINOP operation with missing operator."""
        expr = {
            "op": "BINOP",
            "left": {"op": "CONST", "value": 5},
            "right": {"op": "CONST", "value": 3}
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("operator", str(context.exception))
    
    def test_unknown_op_type(self):
        """Test unknown operation type raises ValueError."""
        expr = {"op": "UNKNOWN", "value": 42}
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("UNKNOWN", str(context.exception))
    
    def test_unsupported_operator(self):
        """Test unsupported binary operator raises ValueError."""
        expr = {
            "op": "BINOP",
            "left": {"op": "CONST", "value": 5},
            "right": {"op": "CONST", "value": 3},
            "operator": "**"
        }
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        self.assertIn("**", str(context.exception))
    
    def test_nested_binop(self):
        """Test nested binary operations."""
        expr = {
            "op": "BINOP",
            "left": {
                "op": "BINOP",
                "left": {"op": "CONST", "value": 1},
                "right": {"op": "CONST", "value": 2},
                "operator": "+"
            },
            "right": {"op": "CONST", "value": 3},
            "operator": "*"
        }
        result = generate_expression_code(expr, "test_func", {})
        self.assertIn("add x0, x1, x0", result)
        self.assertIn("mul x0, x1, x0", result)
    
    def test_var_in_binop(self):
        """Test BINOP with variable operands."""
        expr = {
            "op": "BINOP",
            "left": {"op": "VAR", "var_name": "a"},
            "right": {"op": "VAR", "var_name": "b"},
            "operator": "+"
        }
        var_offsets = {"a": 8, "b": 16}
        result = generate_expression_code(expr, "test_func", var_offsets)
        self.assertIn("lw x0, 8(sp)", result)
        self.assertIn("lw x0, 16(sp)", result)
        self.assertIn("add x0, x1, x0", result)
    
    def test_mixed_const_var_binop(self):
        """Test BINOP with mixed constant and variable operands."""
        expr = {
            "op": "BINOP",
            "left": {"op": "CONST", "value": 10},
            "right": {"op": "VAR", "var_name": "x"},
            "operator": "-"
        }
        var_offsets = {"x": 24}
        result = generate_expression_code(expr, "test_func", var_offsets)
        self.assertIn("li x0, 10", result)
        self.assertIn("lw x0, 24(sp)", result)
        self.assertIn("sub x0, x1, x0", result)


if __name__ == "__main__":
    unittest.main()
