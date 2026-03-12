import unittest
from unittest.mock import patch, call

from .handle_while_src import handle_while


class TestHandleWhile(unittest.TestCase):
    """Test cases for handle_while function."""

    def test_basic_while_loop(self):
        """Test basic while loop with condition and single body statement."""
        stmt = {
            "type": "WHILE",
            "condition": {
                "type": "binary",
                "op": "<",
                "left": {"type": "identifier", "name": "i"},
                "right": {"type": "literal", "value": 10}
            },
            "body": [
                {
                    "type": "ASSIGN",
                    "target": "i",
                    "value": {
                        "type": "binary",
                        "op": "+",
                        "left": {"type": "identifier", "name": "i"},
                        "right": {"type": "literal", "value": 1}
                    }
                }
            ]
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 4

        with patch('handle_while_src.evaluate_expression') as mock_eval, \
             patch('handle_while_src.generate_statement_code') as mock_gen:
            mock_eval.return_value = "    cmp r0, #10\n"
            mock_gen.return_value = ("    add r0, r0, #1\n", 8)

            code, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify label counter was incremented
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_end"], 1)

            # Verify labels are in the code
            self.assertIn("test_func_while_cond_0", code)
            self.assertIn("test_func_while_end_0", code)

            # Verify structure
            self.assertIn("b test_func_while_cond_0", code)
            self.assertIn("cmp r0, #0", code)
            self.assertIn("beq test_func_while_end_0", code)
            self.assertIn("b test_func_while_cond_0", code)

            # Verify offset updated
            self.assertEqual(offset, 8)

            # Verify delegates were called correctly
            mock_eval.assert_called_once_with(
                stmt["condition"], var_offsets, "r0"
            )
            mock_gen.assert_called_once_with(
                stmt["body"][0], func_name, label_counter, var_offsets, next_offset
            )

    def test_empty_body_while_loop(self):
        """Test while loop with empty body."""
        stmt = {
            "type": "WHILE",
            "condition": {
                "type": "binary",
                "op": "<",
                "left": {"type": "identifier", "name": "i"},
                "right": {"type": "literal", "value": 10}
            },
            "body": []
        }
        func_name = "main"
        label_counter = {"while_cond": 5, "while_end": 5}
        var_offsets = {"i": 0}
        next_offset = 16

        with patch('handle_while_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = "    ldr r0, [sp, #0]\n"

            code, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify label counter was incremented
            self.assertEqual(label_counter["while_cond"], 6)
            self.assertEqual(label_counter["while_end"], 6)

            # Verify labels use correct counter values
            self.assertIn("main_while_cond_5", code)
            self.assertIn("main_while_end_5", code)

            # Verify offset unchanged (no body statements)
            self.assertEqual(offset, next_offset)

    def test_multiple_body_statements(self):
        """Test while loop with multiple body statements."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "literal", "value": 1},
            "body": [
                {"type": "ASSIGN", "target": "i", "value": {"type": "literal", "value": 1}},
                {"type": "ASSIGN", "target": "sum", "value": {"type": "literal", "value": 2}}
            ]
        }
        func_name = "loop_func"
        label_counter = {"while_cond": 2, "while_end": 2}
        var_offsets = {"i": 0, "sum": 4}
        next_offset = 8

        with patch('handle_while_src.evaluate_expression') as mock_eval, \
             patch('handle_while_src.generate_statement_code') as mock_gen:
            mock_eval.return_value = "    mov r0, #1\n"
            mock_gen.side_effect = [
                ("    str r0, [sp, #0]\n", 12),
                ("    str r0, [sp, #4]\n", 16)
            ]

            code, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify label counter incremented
            self.assertEqual(label_counter["while_cond"], 3)
            self.assertEqual(label_counter["while_end"], 3)

            # Verify offset is from last statement
            self.assertEqual(offset, 16)

            # Verify generate_statement_code called for each body statement
            self.assertEqual(mock_gen.call_count, 2)
            mock_gen.assert_has_calls([
                call(stmt["body"][0], func_name, label_counter, var_offsets, next_offset),
                call(stmt["body"][1], func_name, label_counter, var_offsets, 12)
            ])

    def test_fresh_label_counters(self):
        """Test while loop with fresh (empty) label counters."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "literal", "value": 1},
            "body": [{"type": "NOP"}]
        }
        func_name = "fresh_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with patch('handle_while_src.evaluate_expression') as mock_eval, \
             patch('handle_while_src.generate_statement_code') as mock_gen:
            mock_eval.return_value = "    mov r0, #1\n"
            mock_gen.return_value = ("    nop\n", 4)

            code, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify labels start from 0
            self.assertIn("fresh_func_while_cond_0", code)
            self.assertIn("fresh_func_while_end_0", code)

            # Verify counter initialized and incremented
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_end"], 1)

    def test_missing_condition(self):
        """Test while loop with missing condition field."""
        stmt = {
            "type": "WHILE",
            "body": [{"type": "NOP"}]
        }
        func_name = "func_missing"
        label_counter = {"while_cond": 10, "while_end": 10}
        var_offsets = {}
        next_offset = 16

        with patch('handle_while_src.evaluate_expression') as mock_eval, \
             patch('handle_while_src.generate_statement_code') as mock_gen:
            mock_eval.return_value = ""
            mock_gen.return_value = ("    nop\n", 20)

            code, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify labels generated
            self.assertIn("func_missing_while_cond_10", code)
            self.assertIn("func_missing_while_end_10", code)

            # Verify counter incremented
            self.assertEqual(label_counter["while_cond"], 11)
            self.assertEqual(label_counter["while_end"], 11)

            # Verify evaluate_expression called with empty dict
            mock_eval.assert_called_once_with({}, var_offsets, "r0")

    def test_missing_body(self):
        """Test while loop with missing body field."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "literal", "value": 1}
        }
        func_name = "test_func"
        label_counter = {"while_cond": 5, "while_end": 5}
        var_offsets = {}
        next_offset = 16

        with patch('handle_while_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = "    mov r0, #1\n"

            code, offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

            # Verify labels generated
            self.assertIn("test_func_while_cond_5", code)
            self.assertIn("test_func_while_end_5", code)

            # Verify counter incremented
            self.assertEqual(label_counter["while_cond"], 6)
            self.assertEqual(label_counter["while_end"], 6)

            # Verify offset unchanged
            self.assertEqual(offset, next_offset)

    def test_label_counter_state_across_multiple_loops(self):
        """Test that label counter state is maintained across multiple while loops."""
        stmt1 = {
            "type": "WHILE",
            "condition": {"type": "literal", "value": 1},
            "body": []
        }
        stmt2 = {
            "type": "WHILE",
            "condition": {"type": "literal", "value": 1},
            "body": []
        }
        func_name = "multi_loop"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with patch('handle_while_src.evaluate_expression') as mock_eval:
            mock_eval.return_value = "    mov r0, #1\n"

            # First loop
            code1, offset1 = handle_while(stmt1, func_name, label_counter, var_offsets, next_offset)
            self.assertIn("multi_loop_while_cond_0", code1)
            self.assertIn("multi_loop_while_end_0", code1)

            # Second loop should use incremented counters
            code2, offset2 = handle_while(stmt2, func_name, label_counter, var_offsets, offset1)
            self.assertIn("multi_loop_while_cond_1", code2)
            self.assertIn("multi_loop_while_end_1", code2)

            # Verify final counter state
            self.assertEqual(label_counter["while_cond"], 2)
            self.assertEqual(label_counter["while_end"], 2)


if __name__ == "__main__":
    unittest.main()
