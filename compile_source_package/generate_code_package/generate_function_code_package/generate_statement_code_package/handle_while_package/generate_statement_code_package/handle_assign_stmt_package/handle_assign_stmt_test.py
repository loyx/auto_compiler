import unittest
from unittest.mock import patch
from typing import Dict

# Relative import from the same package
from .handle_assign_stmt_src import handle_assign_stmt


class TestHandleAssignStmt(unittest.TestCase):
    """Test cases for handle_assign_stmt function."""

    def test_new_variable_assignment(self):
        """Test assigning a value to a new variable."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "CONST", "value": 42}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LOAD_CONST 42\n", 0)

            code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(var_offsets, {"x": 0})
            self.assertEqual(new_offset, 8)
            self.assertEqual(code, "LOAD_CONST 42\nSTORE_OFFSET 0\n")
            mock_gen_expr.assert_called_once_with({"type": "CONST", "value": 42}, var_offsets, 0)

    def test_existing_variable_reassignment(self):
        """Test reassigning a value to an existing variable."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "CONST", "value": 100}
        }
        var_offsets: Dict[str, int] = {"x": 16}
        next_offset = 24

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LOAD_CONST 100\n", 24)

            code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(var_offsets, {"x": 16})
            self.assertEqual(new_offset, 24)
            self.assertEqual(code, "LOAD_CONST 100\nSTORE_OFFSET 16\n")

    def test_multiple_variables_assignment(self):
        """Test assigning to multiple variables sequentially."""
        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 8

        stmt_y = {
            "type": "ASSIGN",
            "target": "y",
            "value": {"type": "CONST", "value": 20}
        }

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LOAD_CONST 20\n", 8)

            code, new_offset = handle_assign_stmt(stmt_y, var_offsets, next_offset)

            self.assertEqual(var_offsets, {"x": 0, "y": 8})
            self.assertEqual(new_offset, 16)
            self.assertEqual(code, "LOAD_CONST 20\nSTORE_OFFSET 8\n")

    def test_zero_offset_initial(self):
        """Test variable assignment starting from offset 0."""
        stmt = {
            "type": "ASSIGN",
            "target": "a",
            "value": {"type": "CONST", "value": 0}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LOAD_CONST 0\n", 0)

            code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(var_offsets, {"a": 0})
            self.assertEqual(new_offset, 8)
            self.assertEqual(code, "LOAD_CONST 0\nSTORE_OFFSET 0\n")

    def test_generate_expression_code_exception_propagation(self):
        """Test that exceptions from generate_expression_code are propagated."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "INVALID"}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.side_effect = ValueError("Invalid expression type")

            with self.assertRaises(ValueError) as context:
                handle_assign_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(str(context.exception), "Invalid expression type")
            self.assertEqual(var_offsets, {})

    def test_complex_expression_code(self):
        """Test assignment with complex expression generating multiple instructions."""
        stmt = {
            "type": "ASSIGN",
            "target": "result",
            "value": {"type": "BINOP", "op": "ADD", "left": {"type": "VAR", "name": "a"}, "right": {"type": "VAR", "name": "b"}}
        }
        var_offsets: Dict[str, int] = {"a": 0, "b": 8}
        next_offset = 16

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LOAD_VAR 0\nLOAD_VAR 8\nADD\n", 16)

            code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(var_offsets, {"a": 0, "b": 8, "result": 16})
            self.assertEqual(new_offset, 24)
            self.assertEqual(code, "LOAD_VAR 0\nLOAD_VAR 8\nADD\nSTORE_OFFSET 16\n")

    def test_var_offsets_modified_in_place(self):
        """Test that var_offsets is modified in-place, not replaced."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "CONST", "value": 1}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        original_id = id(var_offsets)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LOAD_CONST 1\n", 0)

            handle_assign_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(id(var_offsets), original_id)
            self.assertEqual(var_offsets, {"x": 0})

    def test_non_zero_starting_offset(self):
        """Test variable assignment with non-zero starting offset."""
        stmt = {
            "type": "ASSIGN",
            "target": "z",
            "value": {"type": "CONST", "value": 99}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 64

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LOAD_CONST 99\n", 64)

            code, new_offset = handle_assign_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(var_offsets, {"z": 64})
            self.assertEqual(new_offset, 72)
            self.assertEqual(code, "LOAD_CONST 99\nSTORE_OFFSET 64\n")


if __name__ == "__main__":
    unittest.main()
