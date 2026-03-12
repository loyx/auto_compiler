# === std / third-party imports ===
import unittest

# === relative imports ===
from ._handle_literal_src import _handle_literal


class TestHandleLiteral(unittest.TestCase):
    """Test cases for _handle_literal function."""

    def test_positive_literal(self):
        """Test with positive integer literal."""
        expr = {"type": "LITERAL", "value": 42}
        next_offset = 10
        assembly_code, returned_offset = _handle_literal(expr, next_offset)
        
        self.assertEqual(assembly_code, "MOV R0, #42")
        self.assertEqual(returned_offset, next_offset)

    def test_negative_literal(self):
        """Test with negative integer literal."""
        expr = {"type": "LITERAL", "value": -100}
        next_offset = 20
        assembly_code, returned_offset = _handle_literal(expr, next_offset)
        
        self.assertEqual(assembly_code, "MOV R0, #-100")
        self.assertEqual(returned_offset, next_offset)

    def test_zero_literal(self):
        """Test with zero literal."""
        expr = {"type": "LITERAL", "value": 0}
        next_offset = 0
        assembly_code, returned_offset = _handle_literal(expr, next_offset)
        
        self.assertEqual(assembly_code, "MOV R0, #0")
        self.assertEqual(returned_offset, 0)

    def test_large_positive_literal(self):
        """Test with large positive integer literal."""
        expr = {"type": "LITERAL", "value": 2147483647}
        next_offset = 100
        assembly_code, returned_offset = _handle_literal(expr, next_offset)
        
        self.assertEqual(assembly_code, "MOV R0, #2147483647")
        self.assertEqual(returned_offset, next_offset)

    def test_large_negative_literal(self):
        """Test with large negative integer literal."""
        expr = {"type": "LITERAL", "value": -2147483648}
        next_offset = 50
        assembly_code, returned_offset = _handle_literal(expr, next_offset)
        
        self.assertEqual(assembly_code, "MOV R0, #-2147483648")
        self.assertEqual(returned_offset, next_offset)

    def test_next_offset_unchanged(self):
        """Test that next_offset is not modified regardless of value."""
        expr = {"type": "LITERAL", "value": 999}
        next_offset = 12345
        _, returned_offset = _handle_literal(expr, next_offset)
        
        self.assertEqual(returned_offset, next_offset)

    def test_returns_tuple(self):
        """Test that function returns a tuple of correct types."""
        expr = {"type": "LITERAL", "value": 1}
        next_offset = 5
        result = _handle_literal(expr, next_offset)
        
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], int)

    def test_one_literal(self):
        """Test with value of 1."""
        expr = {"type": "LITERAL", "value": 1}
        next_offset = 8
        assembly_code, returned_offset = _handle_literal(expr, next_offset)
        
        self.assertEqual(assembly_code, "MOV R0, #1")
        self.assertEqual(returned_offset, 8)


if __name__ == "__main__":
    unittest.main()
