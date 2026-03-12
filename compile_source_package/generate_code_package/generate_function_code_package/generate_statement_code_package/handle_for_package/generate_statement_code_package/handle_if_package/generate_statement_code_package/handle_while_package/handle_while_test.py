# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict

# === relative imports ===
from .handle_while_src import handle_while


class TestHandleWhile(unittest.TestCase):
    """Test cases for handle_while function."""

    def test_simple_while_loop(self):
        """Test basic WHILE loop with single condition and empty body."""
        stmt = {
            "type": "while",
            "condition": {"type": "binary", "operator": "<", "left": {"type": "var", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": []
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {"while_start": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {"i": 0}
        next_offset = 1

        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_stmt:
            mock_expr.return_value = ("CMP R1, #10", 1)
            mock_stmt.return_value = ("", 1)

            asm_code, updated_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify label counter was mutated
            self.assertEqual(label_counter["while_start"], 1)
            self.assertEqual(label_counter["while_end"], 1)

            # Verify expression code was called with correct parameters
            mock_expr.assert_called_once()
            call_args = mock_expr.call_args
            self.assertEqual(call_args[0][0], stmt["condition"])
            self.assertEqual(call_args[0][1], func_name)

            # Verify assembly structure
            self.assertIn("test_func_while_0_start:", asm_code)
            self.assertIn("CMP R0, #0", asm_code)
            self.assertIn("B.EQ test_func_while_0_end", asm_code)
            self.assertIn("B test_func_while_0_start", asm_code)
            self.assertIn("test_func_while_0_end:", asm_code)

            # Verify offset propagation
            self.assertEqual(updated_offset, 1)

    def test_while_loop_with_body_statements(self):
        """Test WHILE loop with multiple body statements."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": 1},
            "body": [
                {"type": "assign", "var": "i", "value": {"type": "literal", "value": 1}},
                {"type": "assign", "var": "j", "value": {"type": "literal", "value": 2}}
            ]
        }
        func_name = "main"
        label_counter: Dict[str, int] = {"while_start": 2, "while_end": 3}
        var_offsets: Dict[str, int] = {"i": 0, "j": 1}
        next_offset = 2

        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_stmt:
            mock_expr.return_value = ("MOV R0, #1", 2)
            mock_stmt.side_effect = [
                ("STR R0, [SP, #0]", 3),
                ("STR R0, [SP, #4]", 4)
            ]

            asm_code, updated_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify label counter was incremented
            self.assertEqual(label_counter["while_start"], 3)
            self.assertEqual(label_counter["while_end"], 4)

            # Verify generate_statement_code was called twice for body
            self.assertEqual(mock_stmt.call_count, 2)

            # Verify final offset
            self.assertEqual(updated_offset, 4)

            # Verify body code is included in assembly
            self.assertIn("STR R0, [SP, #0]", asm_code)
            self.assertIn("STR R0, [SP, #4]", asm_code)

    def test_while_loop_empty_body(self):
        """Test WHILE loop with no body statements."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": 0},
            "body": []
        }
        func_name = "empty_loop"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_stmt:
            mock_expr.return_value = ("MOV R0, #0", 0)
            mock_stmt.return_value = ("", 0)

            asm_code, updated_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify default label counter values work
            self.assertEqual(label_counter["while_start"], 1)
            self.assertEqual(label_counter["while_end"], 1)

            # Verify generate_statement_code was not called for empty body
            mock_stmt.assert_not_called()

            # Verify offset remains unchanged
            self.assertEqual(updated_offset, 0)

    def test_label_uniqueness_across_multiple_calls(self):
        """Test that multiple handle_while calls generate unique labels."""
        stmt = {"type": "while", "condition": {"type": "literal", "value": 1}, "body": []}
        func_name = "multi"
        label_counter: Dict[str, int] = {"while_start": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_stmt:
            mock_expr.return_value = ("NOP", 0)
            mock_stmt.return_value = ("", 0)

            # First call
            asm1, _ = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)
            # Second call
            asm2, _ = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify labels are unique
            self.assertIn("multi_while_0_start", asm1)
            self.assertIn("multi_while_1_start", asm2)
            self.assertIn("multi_while_0_end", asm1)
            self.assertIn("multi_while_1_end", asm2)

            # Verify label counter was incremented twice
            self.assertEqual(label_counter["while_start"], 2)
            self.assertEqual(label_counter["while_end"], 2)

    def test_offset_propagation_through_body(self):
        """Test that offset is correctly propagated through body statement processing."""
        stmt = {
            "type": "while",
            "condition": {"type": "literal", "value": 1},
            "body": [
                {"type": "assign", "var": "a", "value": {"type": "literal", "value": 1}},
                {"type": "assign", "var": "b", "value": {"type": "literal", "value": 2}},
                {"type": "assign", "var": "c", "value": {"type": "literal", "value": 3}}
            ]
        }
        func_name = "offset_test"
        label_counter: Dict[str, int] = {"while_start": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 5

        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_stmt:
            # Expression returns offset 5
            mock_expr.return_value = ("MOV R0, #1", 5)
            # Each statement increments offset
            mock_stmt.side_effect = [
                ("NOP", 6),
                ("NOP", 7),
                ("NOP", 8)
            ]

            asm_code, updated_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify final offset is from last statement
            self.assertEqual(updated_offset, 8)

            # Verify generate_statement_code was called with correct offsets
            calls = mock_stmt.call_args_list
            self.assertEqual(len(calls), 3)
            # First call should use cond_offset (5)
            # Subsequent calls should use previous statement's offset

    def test_condition_evaluation_integration(self):
        """Test that condition evaluation code is properly integrated into loop."""
        stmt = {
            "type": "while",
            "condition": {"type": "binary", "operator": "==", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "body": []
        }
        func_name = "cond_test"
        label_counter: Dict[str, int] = {"while_start": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 1

        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_stmt:
            mock_expr.return_value = ("LDR R0, [SP, #0]\nCMP R0, #0", 1)
            mock_stmt.return_value = ("", 1)

            asm_code, _ = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify condition code appears after loop_start_label
            lines = asm_code.split("\n")
            self.assertEqual(lines[0], "cond_test_while_0_start:")
            self.assertIn("LDR R0, [SP, #0]", lines[1])
            # Verify CMP R0, #0 (loop termination check) is present
            self.assertIn("CMP R0, #0", asm_code)

    def test_return_type_structure(self):
        """Test that return value is correct Tuple[str, int] structure."""
        stmt = {"type": "while", "condition": {"type": "literal", "value": 1}, "body": []}
        func_name = "return_test"
        label_counter: Dict[str, int] = {"while_start": 0, "while_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_stmt:
            mock_expr.return_value = ("NOP", 42)
            mock_stmt.return_value = ("", 42)

            result = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify return type
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], int)
            self.assertEqual(result[1], 42)


if __name__ == "__main__":
    unittest.main()
