import unittest
from unittest.mock import patch

from .handle_if_src import handle_if


class TestHandleIf(unittest.TestCase):
    """Test cases for handle_if function."""

    def test_if_with_else_branch(self):
        """Test IF statement with both then and else branches."""
        stmt = {
            "type": "IF",
            "condition": {"type": "BINARY", "op": "==", "left": 1, "right": 2},
            "then_body": [{"type": "EXPR", "expr": {"type": "LITERAL", "value": 1}}],
            "else_body": [{"type": "EXPR", "expr": {"type": "LITERAL", "value": 2}}]
        }
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0}
        next_offset = 10

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.handle_if_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:

            mock_gen_expr.return_value = ("    mov x0, #1\n", 11, "x0")
            mock_gen_stmt.side_effect = [
                ("    // then statement\n", 11),
                ("    // else statement\n", 12)
            ]

            result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("cbz x0, test_func_else_0", result_code)
            self.assertIn("b test_func_end_0", result_code)
            self.assertIn("test_func_else_0:\n", result_code)
            self.assertIn("test_func_end_0:\n", result_code)
            self.assertEqual(label_counter["if_else"], 1)
            self.assertEqual(label_counter["if_end"], 1)
            self.assertEqual(result_offset, 12)

    def test_if_without_else_branch(self):
        """Test IF statement with only then branch (no else)."""
        stmt = {
            "type": "IF",
            "condition": {"type": "BINARY", "op": ">", "left": 5, "right": 3},
            "then_body": [{"type": "EXPR", "expr": {"type": "LITERAL", "value": 10}}],
        }
        func_name = "test_func"
        label_counter = {"if_else": 2, "if_end": 3}
        var_offsets = {"y": 1}
        next_offset = 20

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.handle_if_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:

            mock_gen_expr.return_value = ("    mov x1, #5\n", 21, "x1")
            mock_gen_stmt.return_value = ("    // then\n", 21)

            result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("cbz x1, test_func_else_2", result_code)
            self.assertIn("test_func_end_3:\n", result_code)
            self.assertNotIn("b test_func_end", result_code)
            self.assertEqual(label_counter["if_else"], 3)
            self.assertEqual(label_counter["if_end"], 4)

    def test_if_missing_condition(self):
        """Test IF statement with missing condition (error case)."""
        stmt = {
            "type": "IF",
            "then_body": [],
            "else_body": []
        }
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 5

        result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("ERROR: IF missing condition", result_code)
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertEqual(result_offset, 5)

    def test_if_empty_then_body(self):
        """Test IF statement with empty then_body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": True},
            "then_body": [],
            "else_body": [{"type": "EXPR", "expr": {"type": "LITERAL", "value": 1}}]
        }
        func_name = "my_func"
        label_counter = {"if_else": 1, "if_end": 1}
        var_offsets = {"z": 2}
        next_offset = 15

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.handle_if_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:

            mock_gen_expr.return_value = ("    mov x2, #1\n", 16, "x2")
            mock_gen_stmt.return_value = ("    // else stmt\n", 16)

            result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("cbz x2, my_func_else_1", result_code)
            self.assertIn("my_func_end_1:\n", result_code)
            self.assertEqual(label_counter["if_else"], 2)
            self.assertEqual(label_counter["if_end"], 2)

    def test_if_multiple_then_statements(self):
        """Test IF with multiple statements in then_body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "IDENT", "name": "flag"},
            "then_body": [
                {"type": "EXPR", "expr": {"type": "LITERAL", "value": 1}},
                {"type": "EXPR", "expr": {"type": "LITERAL", "value": 2}},
                {"type": "EXPR", "expr": {"type": "LITERAL", "value": 3}}
            ],
            "else_body": []
        }
        func_name = "func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"flag": 0}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.handle_if_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:

            mock_gen_expr.return_value = ("    ldr x0, [sp, #0]\n", 1, "x0")
            mock_gen_stmt.side_effect = [
                ("    // stmt1\n", 1),
                ("    // stmt2\n", 2),
                ("    // stmt3\n", 3)
            ]

            result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(mock_gen_stmt.call_count, 3)
            self.assertEqual(result_offset, 3)
            self.assertIn("func_end_0:\n", result_code)

    def test_if_empty_else_body_treated_as_has_else(self):
        """Test IF with empty else_body list - treated as having else branch."""
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [{"type": "EXPR", "expr": {"type": "LITERAL", "value": 1}}],
            "else_body": []
        }
        func_name = "test"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.handle_if_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:

            mock_gen_expr.return_value = ("    mov x0, #1\n", 1, "x0")
            mock_gen_stmt.return_value = ("    // then\n", 1)

            result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("test_else_0:\n", result_code)
            self.assertIn("test_end_0:\n", result_code)
            self.assertIn("b test_end_0", result_code)
            self.assertEqual(label_counter["if_else"], 1)
            self.assertEqual(label_counter["if_end"], 1)

    def test_label_counter_initialization(self):
        """Test when label_counter doesn't have if_else or if_end keys."""
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [],
            "else_body": []
        }
        func_name = "func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #1\n", 1, "x0")

            result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertIn("func_else_0:", result_code)
            self.assertIn("func_end_0:", result_code)
            self.assertEqual(label_counter["if_else"], 1)
            self.assertEqual(label_counter["if_end"], 1)

    def test_if_no_else_body_key(self):
        """Test IF when else_body key is not present (None)."""
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [{"type": "EXPR", "expr": {"type": "LITERAL", "value": 1}}]
        }
        func_name = "test"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.handle_if_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:

            mock_gen_expr.return_value = ("    mov x0, #1\n", 1, "x0")
            mock_gen_stmt.return_value = ("    // then\n", 1)

            result_code, result_offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertNotIn("test_else_0:", result_code)
            self.assertIn("test_end_0:\n", result_code)
            self.assertNotIn("b test_end_0", result_code)
            self.assertEqual(label_counter["if_else"], 1)
            self.assertEqual(label_counter["if_end"], 1)


if __name__ == "__main__":
    unittest.main()
