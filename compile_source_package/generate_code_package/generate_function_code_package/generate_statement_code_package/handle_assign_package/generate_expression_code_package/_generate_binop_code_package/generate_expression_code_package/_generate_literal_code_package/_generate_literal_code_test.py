import unittest

# Relative import from the same package
from ._generate_literal_code_src import _generate_literal_code


class TestGenerateLiteralCode(unittest.TestCase):
    """Test cases for _generate_literal_code function."""

    def test_int_literal_positive(self):
        """Test generating code for positive integer literal."""
        expr = {
            "type": "LITERAL",
            "value": 42,
            "literal_type": "int"
        }
        result = _generate_literal_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #42")

    def test_int_literal_negative(self):
        """Test generating code for negative integer literal."""
        expr = {
            "type": "LITERAL",
            "value": -10,
            "literal_type": "int"
        }
        result = _generate_literal_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #-10")

    def test_int_literal_zero(self):
        """Test generating code for zero integer literal."""
        expr = {
            "type": "LITERAL",
            "value": 0,
            "literal_type": "int"
        }
        result = _generate_literal_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #0")

    def test_bool_literal_true(self):
        """Test generating code for boolean True literal."""
        expr = {
            "type": "LITERAL",
            "value": True,
            "literal_type": "bool"
        }
        result = _generate_literal_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #1")

    def test_bool_literal_false(self):
        """Test generating code for boolean False literal."""
        expr = {
            "type": "LITERAL",
            "value": False,
            "literal_type": "bool"
        }
        result = _generate_literal_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #0")

    def test_invalid_literal_type(self):
        """Test that ValueError is raised for invalid literal_type."""
        expr = {
            "type": "LITERAL",
            "value": 42,
            "literal_type": "float"
        }
        with self.assertRaises(ValueError) as context:
            _generate_literal_code(expr, "test_func", {})
        self.assertIn("Invalid literal_type: float", str(context.exception))

    def test_invalid_literal_type_none(self):
        """Test that ValueError is raised when literal_type is None."""
        expr = {
            "type": "LITERAL",
            "value": 42,
            "literal_type": None
        }
        with self.assertRaises(ValueError) as context:
            _generate_literal_code(expr, "test_func", {})
        self.assertIn("Invalid literal_type: None", str(context.exception))

    def test_func_name_not_used(self):
        """Test that func_name parameter doesn't affect output."""
        expr = {
            "type": "LITERAL",
            "value": 42,
            "literal_type": "int"
        }
        result1 = _generate_literal_code(expr, "func1", {})
        result2 = _generate_literal_code(expr, "func2", {})
        self.assertEqual(result1, result2)

    def test_var_offsets_not_used(self):
        """Test that var_offsets parameter doesn't affect output."""
        expr = {
            "type": "LITERAL",
            "value": 42,
            "literal_type": "int"
        }
        result1 = _generate_literal_code(expr, "test_func", {})
        result2 = _generate_literal_code(expr, "test_func", {"var": 0})
        self.assertEqual(result1, result2)

    def test_int_literal_large_value(self):
        """Test generating code for large integer literal."""
        expr = {
            "type": "LITERAL",
            "value": 999999,
            "literal_type": "int"
        }
        result = _generate_literal_code(expr, "test_func", {})
        self.assertEqual(result, "mov x0, #999999")


if __name__ == "__main__":
    unittest.main()
