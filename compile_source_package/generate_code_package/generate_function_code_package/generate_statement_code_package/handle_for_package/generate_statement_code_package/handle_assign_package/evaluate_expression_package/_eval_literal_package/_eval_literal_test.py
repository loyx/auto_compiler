# === std / third-party imports ===
import unittest

# === relative import of UUT ===
from ._eval_literal_src import _eval_literal


class TestEvalLiteral(unittest.TestCase):
    """Test cases for _eval_literal function."""

    def test_literal_bool_true(self):
        """Test LITERAL expression with boolean True value."""
        expr = {"type": "LITERAL", "value": True}
        code, offset_delta, register = _eval_literal(expr)
        
        self.assertEqual(code, "    MOV R0, #1")
        self.assertEqual(offset_delta, 0)
        self.assertEqual(register, "R0")

    def test_literal_bool_false(self):
        """Test LITERAL expression with boolean False value."""
        expr = {"type": "LITERAL", "value": False}
        code, offset_delta, register = _eval_literal(expr)
        
        self.assertEqual(code, "    MOV R0, #0")
        self.assertEqual(offset_delta, 0)
        self.assertEqual(register, "R0")

    def test_literal_positive_int(self):
        """Test LITERAL expression with positive integer value."""
        expr = {"type": "LITERAL", "value": 42}
        code, offset_delta, register = _eval_literal(expr)
        
        self.assertEqual(code, "    MOV R0, #42")
        self.assertEqual(offset_delta, 0)
        self.assertEqual(register, "R0")

    def test_literal_negative_int(self):
        """Test LITERAL expression with negative integer value."""
        expr = {"type": "LITERAL", "value": -10}
        code, offset_delta, register = _eval_literal(expr)
        
        self.assertEqual(code, "    MOV R0, #-10")
        self.assertEqual(offset_delta, 0)
        self.assertEqual(register, "R0")

    def test_literal_zero(self):
        """Test LITERAL expression with zero value."""
        expr = {"type": "LITERAL", "value": 0}
        code, offset_delta, register = _eval_literal(expr)
        
        self.assertEqual(code, "    MOV R0, #0")
        self.assertEqual(offset_delta, 0)
        self.assertEqual(register, "R0")

    def test_literal_missing_value_field(self):
        """Test LITERAL expression raises ValueError when 'value' field is missing."""
        expr = {"type": "LITERAL"}
        
        with self.assertRaises(ValueError) as context:
            _eval_literal(expr)
        
        self.assertIn("Missing required field 'value'", str(context.exception))

    def test_literal_none_value(self):
        """Test LITERAL expression raises ValueError when 'value' is None."""
        expr = {"type": "LITERAL", "value": None}
        
        with self.assertRaises(ValueError) as context:
            _eval_literal(expr)
        
        self.assertIn("Missing required field 'value'", str(context.exception))

    def test_literal_unsupported_type_string(self):
        """Test LITERAL expression raises ValueError for string type."""
        expr = {"type": "LITERAL", "value": "hello"}
        
        with self.assertRaises(ValueError) as context:
            _eval_literal(expr)
        
        self.assertIn("Unsupported literal type: str", str(context.exception))

    def test_literal_unsupported_type_float(self):
        """Test LITERAL expression raises ValueError for float type."""
        expr = {"type": "LITERAL", "value": 3.14}
        
        with self.assertRaises(ValueError) as context:
            _eval_literal(expr)
        
        self.assertIn("Unsupported literal type: float", str(context.exception))

    def test_literal_unsupported_type_list(self):
        """Test LITERAL expression raises ValueError for list type."""
        expr = {"type": "LITERAL", "value": [1, 2, 3]}
        
        with self.assertRaises(ValueError) as context:
            _eval_literal(expr)
        
        self.assertIn("Unsupported literal type: list", str(context.exception))

    def test_literal_unsupported_type_dict(self):
        """Test LITERAL expression raises ValueError for dict type."""
        expr = {"type": "LITERAL", "value": {"key": "value"}}
        
        with self.assertRaises(ValueError) as context:
            _eval_literal(expr)
        
        self.assertIn("Unsupported literal type: dict", str(context.exception))

    def test_literal_empty_dict(self):
        """Test LITERAL expression raises ValueError for empty dict."""
        expr = {}
        
        with self.assertRaises(ValueError) as context:
            _eval_literal(expr)
        
        self.assertIn("Missing required field 'value'", str(context.exception))


if __name__ == "__main__":
    unittest.main()
