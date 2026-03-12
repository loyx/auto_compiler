import unittest
from .generate_epilogue_src import generate_epilogue


class TestGenerateEpilogue(unittest.TestCase):
    """Test cases for generate_epilogue function."""

    def test_generate_epilogue_basic(self):
        """Test basic epilogue generation with stack_size=0."""
        result = generate_epilogue(0)
        expected = "    mov sp, fp\n    ldp fp, lr, [sp], #16\n    ret"
        self.assertEqual(result, expected)

    def test_generate_epilogue_with_different_stack_sizes(self):
        """Test that stack_size doesn't affect output (as per spec)."""
        for stack_size in [0, 16, 32, 64, 128, 256, 1024]:
            with self.subTest(stack_size=stack_size):
                result = generate_epilogue(stack_size)
                expected = "    mov sp, fp\n    ldp fp, lr, [sp], #16\n    ret"
                self.assertEqual(result, expected)

    def test_generate_epilogue_format(self):
        """Test output format: 4 spaces prefix, newline separated, 3 lines."""
        result = generate_epilogue(16)
        lines = result.split("\n")

        # Should have exactly 3 lines
        self.assertEqual(len(lines), 3)

        # Each line should start with 4 spaces
        for line in lines:
            self.assertTrue(
                line.startswith("    "),
                f"Line '{line}' doesn't start with 4 spaces"
            )

        # Verify exact instruction content
        self.assertEqual(lines[0], "    mov sp, fp")
        self.assertEqual(lines[1], "    ldp fp, lr, [sp], #16")
        self.assertEqual(lines[2], "    ret")

    def test_generate_epilogue_no_trailing_newline(self):
        """Test that result doesn't have trailing newline."""
        result = generate_epilogue(16)
        self.assertFalse(result.endswith("\n"))

    def test_generate_epilogue_negative_stack_size(self):
        """Test behavior with negative stack_size (edge case)."""
        result = generate_epilogue(-16)
        expected = "    mov sp, fp\n    ldp fp, lr, [sp], #16\n    ret"
        self.assertEqual(result, expected)

    def test_generate_epilogue_return_type(self):
        """Test that return type is string."""
        result = generate_epilogue(16)
        self.assertIsInstance(result, str)


if __name__ == "__main__":
    unittest.main()
