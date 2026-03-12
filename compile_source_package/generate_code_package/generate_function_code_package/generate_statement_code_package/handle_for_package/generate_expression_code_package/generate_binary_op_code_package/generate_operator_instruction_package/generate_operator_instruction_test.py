# === std / third-party imports ===
import unittest
from typing import Dict

# === sub function imports ===
from .generate_operator_instruction_src import generate_operator_instruction


class TestGenerateOperatorInstruction(unittest.TestCase):
    """Test cases for generate_operator_instruction function."""

    def test_arithmetic_add(self):
        """Test addition operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("+", "test_func", label_counter, 10)
        self.assertEqual(instruction, "add x0, x1, x0")
        self.assertEqual(offset, 10)
        self.assertEqual(label_counter, {})

    def test_arithmetic_sub(self):
        """Test subtraction operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("-", "test_func", label_counter, 10)
        self.assertEqual(instruction, "sub x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_arithmetic_mul(self):
        """Test multiplication operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("*", "test_func", label_counter, 10)
        self.assertEqual(instruction, "mul x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_arithmetic_div(self):
        """Test division operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("/", "test_func", label_counter, 10)
        self.assertEqual(instruction, "sdiv x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_arithmetic_mod(self):
        """Test modulo operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("%", "test_func", label_counter, 10)
        expected_code = "sdiv x2, x1, x0\n    msub x0, x2, x0, x1"
        self.assertEqual(instruction, expected_code)
        self.assertEqual(offset, 10)

    def test_comparison_eq(self):
        """Test equality operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("==", "test_func", label_counter, 10)
        self.assertEqual(instruction, "cmp x1, x0\n    cset x0, eq")
        self.assertEqual(offset, 10)

    def test_comparison_ne(self):
        """Test not equal operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("!=", "test_func", label_counter, 10)
        self.assertEqual(instruction, "cmp x1, x0\n    cset x0, ne")
        self.assertEqual(offset, 10)

    def test_comparison_lt(self):
        """Test less than operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("<", "test_func", label_counter, 10)
        self.assertEqual(instruction, "cmp x1, x0\n    cset x0, lt")
        self.assertEqual(offset, 10)

    def test_comparison_gt(self):
        """Test greater than operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction(">", "test_func", label_counter, 10)
        self.assertEqual(instruction, "cmp x1, x0\n    cset x0, gt")
        self.assertEqual(offset, 10)

    def test_comparison_le(self):
        """Test less than or equal operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("<=", "test_func", label_counter, 10)
        self.assertEqual(instruction, "cmp x1, x0\n    cset x0, le")
        self.assertEqual(offset, 10)

    def test_comparison_ge(self):
        """Test greater than or equal operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction(">=", "test_func", label_counter, 10)
        self.assertEqual(instruction, "cmp x1, x0\n    cset x0, ge")
        self.assertEqual(offset, 10)

    def test_logical_and_modifies_label_counter(self):
        """Test logical AND operator modifies label_counter in-place."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("&&", "test_func", label_counter, 10)
        self.assertIn("cbz x0,", instruction)
        self.assertIn("test_func_skip_0", instruction)
        self.assertIn("mov x0, x1", instruction)
        self.assertEqual(offset, 10)
        self.assertEqual(label_counter, {"skip": 1})

    def test_logical_and_incremental_labels(self):
        """Test logical AND generates incremental labels."""
        label_counter: Dict[str, int] = {"skip": 5}
        instruction, offset = generate_operator_instruction("&&", "my_func", label_counter, 20)
        self.assertIn("my_func_skip_5", instruction)
        self.assertEqual(label_counter, {"skip": 6})

    def test_logical_or_modifies_label_counter(self):
        """Test logical OR operator modifies label_counter in-place."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("||", "test_func", label_counter, 10)
        self.assertIn("cbnz x0,", instruction)
        self.assertIn("test_func_skip_0", instruction)
        self.assertIn("mov x0, x1", instruction)
        self.assertEqual(offset, 10)
        self.assertEqual(label_counter, {"skip": 1})

    def test_logical_or_incremental_labels(self):
        """Test logical OR generates incremental labels."""
        label_counter: Dict[str, int] = {"skip": 3}
        instruction, offset = generate_operator_instruction("||", "another_func", label_counter, 15)
        self.assertIn("another_func_skip_3", instruction)
        self.assertEqual(label_counter, {"skip": 4})

    def test_bitwise_and(self):
        """Test bitwise AND operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("&", "test_func", label_counter, 10)
        self.assertEqual(instruction, "and x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_bitwise_or(self):
        """Test bitwise OR operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("|", "test_func", label_counter, 10)
        self.assertEqual(instruction, "orr x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_bitwise_xor(self):
        """Test bitwise XOR operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("^", "test_func", label_counter, 10)
        self.assertEqual(instruction, "eor x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_bitwise_left_shift(self):
        """Test left shift operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("<<", "test_func", label_counter, 10)
        self.assertEqual(instruction, "lsl x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_bitwise_right_shift(self):
        """Test arithmetic right shift operator."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction(">>", "test_func", label_counter, 10)
        self.assertEqual(instruction, "asr x0, x1, x0")
        self.assertEqual(offset, 10)

    def test_unknown_operator_raises_value_error(self):
        """Test unknown operator raises ValueError."""
        label_counter: Dict[str, int] = {}
        with self.assertRaises(ValueError) as context:
            generate_operator_instruction("???", "test_func", label_counter, 10)
        self.assertIn("Unknown binary operator: ???", str(context.exception))

    def test_unknown_operator_does_not_modify_label_counter(self):
        """Test unknown operator does not modify label_counter before raising."""
        label_counter: Dict[str, int] = {"skip": 5}
        original_counter = label_counter.copy()
        with self.assertRaises(ValueError):
            generate_operator_instruction("@", "test_func", label_counter, 10)
        self.assertEqual(label_counter, original_counter)

    def test_zero_offset(self):
        """Test with zero offset."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("+", "test_func", label_counter, 0)
        self.assertEqual(offset, 0)

    def test_large_offset(self):
        """Test with large offset value."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("+", "test_func", label_counter, 999999)
        self.assertEqual(offset, 999999)

    def test_empty_func_name(self):
        """Test with empty function name for short-circuit operators."""
        label_counter: Dict[str, int] = {}
        instruction, offset = generate_operator_instruction("&&", "", label_counter, 10)
        self.assertIn("_skip_0", instruction)
        self.assertEqual(label_counter, {"skip": 1})

    def test_mixed_and_or_operations(self):
        """Test mixed && and || operations share skip counter."""
        label_counter: Dict[str, int] = {}
        instruction1, _ = generate_operator_instruction("&&", "func", label_counter, 10)
        instruction2, _ = generate_operator_instruction("||", "func", label_counter, 10)
        instruction3, _ = generate_operator_instruction("&&", "func", label_counter, 10)
        
        self.assertIn("func_skip_0", instruction1)
        self.assertIn("func_skip_1", instruction2)
        self.assertIn("func_skip_2", instruction3)
        self.assertEqual(label_counter, {"skip": 3})


if __name__ == "__main__":
    unittest.main()
