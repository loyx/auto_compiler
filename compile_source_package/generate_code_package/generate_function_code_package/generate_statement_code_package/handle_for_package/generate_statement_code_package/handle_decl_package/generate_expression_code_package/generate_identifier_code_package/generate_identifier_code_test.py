import unittest

# Relative import from the same package
from .generate_identifier_code_src import generate_identifier_code


class TestGenerateIdentifierCode(unittest.TestCase):
    """Test cases for generate_identifier_code function."""
    
    def test_int_type(self):
        """Test with int var_type - should use LDR instruction."""
        expr = {"type": "IDENTIFIER", "name": "x", "var_type": "int"}
        var_offsets = {"x": 4}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #4]")
        self.assertEqual(reg, 0)
    
    def test_char_type(self):
        """Test with char var_type - should use LDRB instruction."""
        expr = {"type": "IDENTIFIER", "name": "c", "var_type": "char"}
        var_offsets = {"c": 8}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDRB R0, [SP, #8]")
        self.assertEqual(reg, 0)
    
    def test_short_type(self):
        """Test with short var_type - should use LDRH instruction."""
        expr = {"type": "IDENTIFIER", "name": "s", "var_type": "short"}
        var_offsets = {"s": 12}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDRH R0, [SP, #12]")
        self.assertEqual(reg, 0)
    
    def test_float_type(self):
        """Test with float var_type - should use LDR instruction."""
        expr = {"type": "IDENTIFIER", "name": "f", "var_type": "float"}
        var_offsets = {"f": 16}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #16]")
        self.assertEqual(reg, 0)
    
    def test_long_type(self):
        """Test with long var_type - should use LDR instruction."""
        expr = {"type": "IDENTIFIER", "name": "l", "var_type": "long"}
        var_offsets = {"l": 20}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #20]")
        self.assertEqual(reg, 0)
    
    def test_pointer_type(self):
        """Test with pointer var_type - should use LDR instruction."""
        expr = {"type": "IDENTIFIER", "name": "ptr", "var_type": "pointer"}
        var_offsets = {"ptr": 24}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #24]")
        self.assertEqual(reg, 0)
    
    def test_double_type(self):
        """Test with double var_type - should use LDR instruction."""
        expr = {"type": "IDENTIFIER", "name": "d", "var_type": "double"}
        var_offsets = {"d": 28}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #28]")
        self.assertEqual(reg, 0)
    
    def test_default_var_type(self):
        """Test without var_type field - should default to int (LDR)."""
        expr = {"type": "IDENTIFIER", "name": "x"}
        var_offsets = {"x": 0}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #0]")
        self.assertEqual(reg, 0)
    
    def test_zero_offset(self):
        """Test with zero offset."""
        expr = {"type": "IDENTIFIER", "name": "x", "var_type": "int"}
        var_offsets = {"x": 0}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #0]")
        self.assertEqual(reg, 0)
    
    def test_large_offset(self):
        """Test with large offset value."""
        expr = {"type": "IDENTIFIER", "name": "x", "var_type": "int"}
        var_offsets = {"x": 1024}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #1024]")
        self.assertEqual(reg, 0)
    
    def test_negative_offset(self):
        """Test with negative offset value."""
        expr = {"type": "IDENTIFIER", "name": "x", "var_type": "int"}
        var_offsets = {"x": -8}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDR R0, [SP, #-8]")
        self.assertEqual(reg, 0)
    
    def test_missing_name_field(self):
        """Test that missing name field raises KeyError."""
        expr = {"type": "IDENTIFIER", "var_type": "int"}
        var_offsets = {"x": 4}
        with self.assertRaises(KeyError) as context:
            generate_identifier_code(expr, var_offsets)
        self.assertEqual(str(context.exception), "Missing field: name")
    
    def test_variable_not_in_var_offsets(self):
        """Test that variable not in var_offsets raises KeyError."""
        expr = {"type": "IDENTIFIER", "name": "y", "var_type": "int"}
        var_offsets = {"x": 4}
        with self.assertRaises(KeyError) as context:
            generate_identifier_code(expr, var_offsets)
        self.assertEqual(str(context.exception), "Variable 'y' not found in var_offsets")
    
    def test_empty_var_offsets(self):
        """Test with empty var_offsets dict."""
        expr = {"type": "IDENTIFIER", "name": "x", "var_type": "int"}
        var_offsets = {}
        with self.assertRaises(KeyError) as context:
            generate_identifier_code(expr, var_offsets)
        self.assertEqual(str(context.exception), "Variable 'x' not found in var_offsets")
    
    def test_multiple_variables_in_offsets(self):
        """Test selecting correct variable from multiple in var_offsets."""
        expr = {"type": "IDENTIFIER", "name": "b", "var_type": "char"}
        var_offsets = {"a": 4, "b": 8, "c": 12}
        code, reg = generate_identifier_code(expr, var_offsets)
        self.assertEqual(code, "LDRB R0, [SP, #8]")
        self.assertEqual(reg, 0)
    
    def test_return_register_always_zero(self):
        """Test that result_register is always 0."""
        test_cases = [
            ({"type": "IDENTIFIER", "name": "x", "var_type": "int"}, {"x": 0}),
            ({"type": "IDENTIFIER", "name": "c", "var_type": "char"}, {"c": 4}),
            ({"type": "IDENTIFIER", "name": "s", "var_type": "short"}, {"s": 8}),
        ]
        for expr, var_offsets in test_cases:
            _, reg = generate_identifier_code(expr, var_offsets)
            self.assertEqual(reg, 0)


if __name__ == "__main__":
    unittest.main()
