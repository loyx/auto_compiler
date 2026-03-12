import unittest
from unittest.mock import patch

from .handle_if_src import handle_if


# Helper to patch with absolute module paths
def patch_generate_expression_code():
    return patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')


def patch_generate_statement_code():
    return patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')


class TestHandleIf(unittest.TestCase):
    """Test cases for handle_if function."""

    def test_if_without_else(self):
        """Test IF statement without else branch."""
        stmt = {
            "type": "IF",
            "condition": {"type": "binary", "op": ">", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "then_body": [
                {"type": "ASSIGN", "target": "y", "value": {"type": "literal", "value": 1}}
            ],
            "else_body": []
        }

        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0, "y": 4}
        next_offset = 8

        with patch_generate_expression_code() as mock_expr, \
             patch_generate_statement_code() as mock_stmt:

            mock_expr.return_value = ("MOV R0, #1", 8)
            mock_stmt.return_value = ("STR R1, [R13, #4]", 12)

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("MOV R0, #1", code)
            self.assertIn("CMP R0, #0", code)
            self.assertIn("B.EQ test_func_if_0_end", code)
            self.assertIn("STR R1, [R13, #4]", code)
            self.assertIn("test_func_if_0_end:", code)
            self.assertNotIn("test_func_if_0_else:", code)
            self.assertEqual(label_counter["if_else"], 0)
            self.assertEqual(label_counter["if_end"], 1)
            self.assertEqual(final_offset, 12)

    def test_if_with_else(self):
        """Test IF statement with else branch."""
        stmt = {
            "type": "IF",
            "condition": {"type": "binary", "op": "==", "left": {"type": "var", "name": "a"}, "right": {"type": "literal", "value": 5}},
            "then_body": [
                {"type": "ASSIGN", "target": "b", "value": {"type": "literal", "value": 10}}
            ],
            "else_body": [
                {"type": "ASSIGN", "target": "b", "value": {"type": "literal", "value": 20}}
            ]
        }

        func_name = "my_func"
        label_counter = {"if_else": 2, "if_end": 3}
        var_offsets = {"a": 0, "b": 4}
        next_offset = 8

        with patch_generate_expression_code() as mock_expr, \
             patch_generate_statement_code() as mock_stmt:

            mock_expr.return_value = ("LDR R0, [R13, #0]", 8)
            mock_stmt.side_effect = [
                ("MOV R1, #10", 12),
                ("MOV R1, #20", 16)
            ]

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("LDR R0, [R13, #0]", code)
            self.assertIn("CMP R0, #0", code)
            self.assertIn("B.EQ my_func_if_2_else", code)
            self.assertIn("my_func_if_2_else:", code)
            self.assertIn("B my_func_if_3_end", code)
            self.assertIn("MOV R1, #10", code)
            self.assertIn("MOV R1, #20", code)
            self.assertIn("my_func_if_3_end:", code)
            self.assertEqual(label_counter["if_else"], 3)
            self.assertEqual(label_counter["if_end"], 4)
            self.assertEqual(final_offset, 16)

    def test_empty_bodies(self):
        """Test IF statement with empty then and else bodies."""
        stmt = {
            "type": "IF",
            "condition": {"type": "binary", "op": ">", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 0}},
            "then_body": [],
            "else_body": []
        }

        func_name = "empty_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0}
        next_offset = 12

        with patch_generate_expression_code() as mock_expr:
            mock_expr.return_value = ("CMP R0, #0", 12)

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("CMP R0, #0", code)
            self.assertIn("B.EQ empty_func_if_0_end", code)
            self.assertIn("empty_func_if_0_end:", code)
            self.assertEqual(label_counter["if_end"], 1)
            self.assertEqual(final_offset, 12)

    def test_multiple_then_statements(self):
        """Test IF statement with multiple statements in then body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "literal", "value": True},
            "then_body": [
                {"type": "ASSIGN", "target": "a", "value": {"type": "literal", "value": 1}},
                {"type": "ASSIGN", "target": "b", "value": {"type": "literal", "value": 2}},
                {"type": "ASSIGN", "target": "c", "value": {"type": "literal", "value": 3}}
            ],
            "else_body": []
        }

        func_name = "multi_func"
        label_counter = {"if_end": 5}
        var_offsets = {"a": 0, "b": 4, "c": 8}
        next_offset = 100

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:

            mock_expr.return_value = ("MOV R0, #1", 100)
            mock_stmt.side_effect = [
                ("MOV R1, #1", 110),
                ("MOV R2, #2", 120),
                ("MOV R3, #3", 130)
            ]

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(mock_stmt.call_count, 3)
            self.assertEqual(label_counter["if_end"], 6)
            self.assertEqual(final_offset, 130)

    def test_offset_propagation(self):
        """Test that offset is properly propagated through statement generation."""
        stmt = {
            "type": "IF",
            "condition": {"type": "literal", "value": True},
            "then_body": [
                {"type": "ASSIGN", "target": "x", "value": {"type": "literal", "value": 1}},
                {"type": "ASSIGN", "target": "y", "value": {"type": "literal", "value": 2}}
            ],
            "else_body": [
                {"type": "ASSIGN", "target": "z", "value": {"type": "literal", "value": 3}}
            ]
        }

        func_name = "offset_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0, "y": 4, "z": 8}
        next_offset = 100

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:

            mock_expr.return_value = ("MOV R0, #1", 100)
            mock_stmt.side_effect = [
                ("STR R1, [R13, #0]", 110),
                ("STR R2, [R13, #4]", 120),
                ("STR R3, [R13, #8]", 130)
            ]

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            calls = mock_stmt.call_args_list
            self.assertEqual(len(calls), 3)
            self.assertEqual(calls[0][0][4], 100)
            self.assertEqual(calls[1][0][4], 110)
            self.assertEqual(calls[2][0][4], 120)
            self.assertEqual(final_offset, 130)

    def test_label_counter_increment_order(self):
        """Test that label counter increments in correct order (else before end)."""
        stmt = {
            "type": "IF",
            "condition": {"type": "literal", "value": False},
            "then_body": [],
            "else_body": [{"type": "NOP"}]
        }

        func_name = "order_func"
        label_counter = {"if_else": 10, "if_end": 20}
        var_offsets = {}
        next_offset = 0

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:

            mock_expr.return_value = ("MOV R0, #0", 0)
            mock_stmt.return_value = ("NOP", 4)

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("order_func_if_10_else:", code)
            self.assertIn("order_func_if_20_end:", code)
            self.assertEqual(label_counter["if_else"], 11)
            self.assertEqual(label_counter["if_end"], 21)
            else_pos = code.find("order_func_if_10_else:")
            end_pos = code.find("order_func_if_20_end:")
            self.assertLess(else_pos, end_pos)

    def test_default_label_counter_values(self):
        """Test handle_if with missing label counter keys."""
        stmt = {
            "type": "IF",
            "condition": {"type": "literal", "value": True},
            "then_body": [],
            "else_body": []
        }

        func_name = "default_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr:
            mock_expr.return_value = ("MOV R0, #1", 0)

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("default_func_if_0_end:", code)
            self.assertEqual(label_counter["if_end"], 1)

    def test_default_label_counter_with_else(self):
        """Test handle_if with else and missing label counter keys."""
        stmt = {
            "type": "IF",
            "condition": {"type": "literal", "value": True},
            "then_body": [],
            "else_body": [{"type": "NOP"}]
        }

        func_name = "default_else_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_expr, \
             patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code') as mock_stmt:

            mock_expr.return_value = ("MOV R0, #1", 0)
            mock_stmt.return_value = ("NOP", 4)

            code, final_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("default_else_func_if_0_else:", code)
            self.assertIn("default_else_func_if_1_end:", code)
            self.assertEqual(label_counter["if_else"], 1)
            self.assertEqual(label_counter["if_end"], 2)


if __name__ == '__main__':
    unittest.main()
