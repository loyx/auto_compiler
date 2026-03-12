# === imports ===
import unittest
from unittest.mock import patch

# === relative import of UUT ===
from ._generate_call_code_src import _generate_call_code


class TestGenerateCallCode(unittest.TestCase):
    """Unit tests for _generate_call_code function."""

    def test_no_arguments(self):
        """Test function call with no arguments."""
        expr = {
            "type": "CALL",
            "function": "my_func",
            "arguments": []
        }
        result = _generate_call_code(expr, "current_func", {})
        self.assertEqual(result, "    bl my_func")

    def test_single_argument(self):
        """Test function call with one argument (stays in x0)."""
        expr = {
            "type": "CALL",
            "function": "my_func",
            "arguments": [{"type": "CONST", "value": 42}]
        }
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.return_value = "    mov x0, #42"
            result = _generate_call_code(expr, "current_func", {})
            mock_gen.assert_called_once_with({"type": "CONST", "value": 42}, "current_func", {})
            self.assertEqual(result, "    mov x0, #42\n    bl my_func")

    def test_two_arguments(self):
        """Test function call with two arguments (x0 and x1)."""
        expr = {
            "type": "CALL",
            "function": "add_func",
            "arguments": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2}
            ]
        }
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                "    mov x0, #1",
                "    mov x0, #2"
            ]
            result = _generate_call_code(expr, "current_func", {})
            self.assertEqual(mock_gen.call_count, 2)
            expected = "    mov x0, #1\n    mov x0, #2\n    mov x1, x0\n    bl add_func"
            self.assertEqual(result, expected)

    def test_eight_arguments_max(self):
        """Test function call with exactly 8 arguments (maximum supported)."""
        expr = {
            "type": "CALL",
            "function": "multi_arg_func",
            "arguments": [{"type": "CONST", "value": i} for i in range(8)]
        }
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [f"    mov x0, #{i}" for i in range(8)]
            result = _generate_call_code(expr, "current_func", {})
            self.assertEqual(mock_gen.call_count, 8)
            # First arg stays in x0, args 1-7 are moved to x1-x7
            lines = result.split("\n")
            self.assertEqual(len(lines), 8 + 7)  # 8 arg codes + 7 mov instructions + 1 bl
            self.assertIn("    bl multi_arg_func", lines)

    def test_nine_arguments_raises_error(self):
        """Test that more than 8 arguments raises ValueError."""
        expr = {
            "type": "CALL",
            "function": "too_many_args",
            "arguments": [{"type": "CONST", "value": i} for i in range(9)]
        }
        with self.assertRaises(ValueError) as context:
            _generate_call_code(expr, "current_func", {})
        self.assertIn("Too many arguments", str(context.exception))
        self.assertIn("9", str(context.exception))

    def test_missing_function_field(self):
        """Test that missing 'function' field raises KeyError."""
        expr = {
            "type": "CALL",
            "arguments": []
        }
        with self.assertRaises(KeyError) as context:
            _generate_call_code(expr, "current_func", {})
        self.assertIn("function", str(context.exception))

    def test_missing_arguments_field(self):
        """Test that missing 'arguments' field raises KeyError."""
        expr = {
            "type": "CALL",
            "function": "my_func"
        }
        with self.assertRaises(KeyError) as context:
            _generate_call_code(expr, "current_func", {})
        self.assertIn("arguments", str(context.exception))

    def test_nested_call_expression(self):
        """Test function call with nested CALL expression as argument."""
        expr = {
            "type": "CALL",
            "function": "outer_func",
            "arguments": [
                {
                    "type": "CALL",
                    "function": "inner_func",
                    "arguments": []
                }
            ]
        }
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.return_value = "    bl inner_func"
            result = _generate_call_code(expr, "current_func", {})
            mock_gen.assert_called_once_with(
                {"type": "CALL", "function": "inner_func", "arguments": []},
                "current_func",
                {}
            )
            self.assertEqual(result, "    bl inner_func\n    bl outer_func")

    def test_var_offsets_passed_to_recursive_calls(self):
        """Test that var_offsets are passed correctly to generate_expression_code."""
        expr = {
            "type": "CALL",
            "function": "my_func",
            "arguments": [{"type": "VAR", "name": "x"}]
        }
        var_offsets = {"x": 0, "y": 8}
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.return_value = "    ldr x0, [sp, #0]"
            _generate_call_code(expr, "current_func", var_offsets)
            mock_gen.assert_called_once_with(
                {"type": "VAR", "name": "x"},
                "current_func",
                var_offsets
            )

    def test_func_name_passed_to_recursive_calls(self):
        """Test that func_name is passed correctly to generate_expression_code."""
        expr = {
            "type": "CALL",
            "function": "my_func",
            "arguments": [{"type": "CONST", "value": 10}]
        }
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.return_value = "    mov x0, #10"
            _generate_call_code(expr, "caller_func", {})
            mock_gen.assert_called_once_with(
                {"type": "CONST", "value": 10},
                "caller_func",
                {}
            )

    def test_return_value_in_x0(self):
        """Test that the result structure implies return value in x0."""
        expr = {
            "type": "CALL",
            "function": "compute",
            "arguments": []
        }
        result = _generate_call_code(expr, "current_func", {})
        # After bl instruction, return value is in x0 per ARM64 convention
        self.assertEqual(result, "    bl compute")
        # The test verifies the structure - no explicit mov needed after bl

    def test_argument_register_mapping(self):
        """Test that arguments 1-7 are mapped to x1-x7 correctly."""
        expr = {
            "type": "CALL",
            "function": "test_func",
            "arguments": [{"type": "CONST", "value": i} for i in range(5)]
        }
        with patch("._generate_call_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [f"    mov x0, #{i}" for i in range(5)]
            result = _generate_call_code(expr, "current_func", {})
            lines = result.split("\n")
            # Verify mov instructions for args 1-4 (to x1-x4)
            self.assertIn("    mov x1, x0", lines)
            self.assertIn("    mov x2, x0", lines)
            self.assertIn("    mov x3, x0", lines)
            self.assertIn("    mov x4, x0", lines)


if __name__ == "__main__":
    unittest.main()
