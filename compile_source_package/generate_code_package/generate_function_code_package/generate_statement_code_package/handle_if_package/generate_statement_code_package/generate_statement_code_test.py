import unittest
from unittest.mock import patch

from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code function."""

    def test_if_statement_delegates_to_handle_if(self):
        """Test IF statement type is delegated to handle_if handler."""
        stmt = {"type": "IF", "condition": {}, "then_body": [], "else_body": []}
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 0

        expected_code = "    ; if code"
        expected_offset = 5

        with patch("handle_if_package.generate_statement_code_package.handle_if_package.handle_if_src.handle_if") as mock_handle_if:
            mock_handle_if.return_value = (expected_code, expected_offset)

            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handle_if.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, expected_offset)

    def test_assign_statement_delegates_to_handle_assign(self):
        """Test ASSIGN statement type is delegated to handle_assign handler."""
        stmt = {"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 42}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"x": 0}
        next_offset = 1

        expected_code = "    ; assign code"
        expected_offset = 3

        with patch("handle_if_package.generate_statement_code_package.handle_assign_package.handle_assign_src.handle_assign") as mock_handle_assign:
            mock_handle_assign.return_value = (expected_code, expected_offset)

            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handle_assign.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, expected_offset)

    def test_return_statement_delegates_to_handle_return(self):
        """Test RETURN statement type is delegated to handle_return handler."""
        stmt = {"type": "RETURN", "expression": {"type": "LITERAL", "value": 0}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        expected_code = "    ; return code"
        expected_offset = 2

        with patch("handle_if_package.generate_statement_code_package.handle_return_package.handle_return_src.handle_return") as mock_handle_return:
            mock_handle_return.return_value = (expected_code, expected_offset)

            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handle_return.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, expected_offset)

    def test_while_statement_delegates_to_handle_while(self):
        """Test WHILE statement type is delegated to handle_while handler."""
        stmt = {"type": "WHILE", "condition": {}, "body": []}
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {}
        next_offset = 0

        expected_code = "    ; while code"
        expected_offset = 10

        with patch("handle_if_package.generate_statement_code_package.handle_while_package.handle_while_src.handle_while") as mock_handle_while:
            mock_handle_while.return_value = (expected_code, expected_offset)

            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handle_while.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, expected_offset)

    def test_break_statement_emits_branch_instruction(self):
        """Test BREAK statement emits branch to break label."""
        stmt = {"type": "BREAK"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    b test_func_break_label")
        self.assertEqual(offset, 0)

    def test_continue_statement_emits_branch_instruction(self):
        """Test CONTINUE statement emits branch to continue label."""
        stmt = {"type": "CONTINUE"}
        func_name = "my_function"
        label_counter = {}
        var_offsets = {}
        next_offset = 5

        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(code, "    b my_function_continue_label")
        self.assertEqual(offset, 5)

    def test_decl_statement_allocates_new_offset(self):
        """Test DECL statement allocates stack slot for new variable."""
        stmt = {"type": "DECL", "name": "new_var"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 3

        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("new_var", var_offsets)
        self.assertEqual(var_offsets["new_var"], 3)
        self.assertEqual(offset, 4)
        self.assertIn("decl new_var at offset 3", code)

    def test_decl_statement_reuses_existing_offset(self):
        """Test DECL statement does not allocate new offset for existing variable."""
        stmt = {"type": "DECL", "name": "existing_var"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"existing_var": 2}
        next_offset = 5

        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(var_offsets["existing_var"], 2)
        self.assertEqual(offset, 5)
        self.assertIn("decl existing_var at offset 2", code)

    def test_expr_statement_delegates_to_generate_expression_code(self):
        """Test EXPR statement delegates to generate_expression_code."""
        stmt = {"type": "EXPR", "expression": {"type": "LITERAL", "value": 42}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        expected_code = "    ; expr code"
        expected_offset = 2

        with patch("handle_if_package.generate_statement_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = (expected_code, expected_offset, "r0")

            code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with({"type": "LITERAL", "value": 42}, var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, expected_offset)

    def test_block_statement_processes_all_statements(self):
        """Test BLOCK statement processes all nested statements sequentially."""
        stmt1 = {"type": "BREAK"}
        stmt2 = {"type": "CONTINUE"}
        stmt = {"type": "BLOCK", "statements": [stmt1, stmt2]}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("b test_func_break_label", code)
        self.assertIn("b test_func_continue_label", code)
        self.assertEqual(offset, 0)

    def test_block_statement_propagates_offset_changes(self):
        """Test BLOCK statement propagates offset changes through nested statements."""
        stmt1 = {"type": "DECL", "name": "var1"}
        stmt2 = {"type": "DECL", "name": "var2"}
        stmt = {"type": "BLOCK", "statements": [stmt1, stmt2]}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(var_offsets["var1"], 0)
        self.assertEqual(var_offsets["var2"], 1)
        self.assertEqual(offset, 2)

    def test_unknown_statement_type_raises_value_error(self):
        """Test unknown statement type raises ValueError."""
        stmt = {"type": "UNKNOWN_TYPE"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("Unsupported statement type: UNKNOWN_TYPE", str(context.exception))

    def test_missing_type_field_raises_value_error(self):
        """Test missing type field raises ValueError."""
        stmt = {"condition": {}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("Unsupported statement type: None", str(context.exception))

    def test_label_counter_passed_by_reference(self):
        """Test label_counter is passed by reference to handlers."""
        stmt = {"type": "IF", "condition": {}, "then_body": [], "else_body": []}
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 0

        with patch("handle_if_package.generate_statement_code_package.handle_if_package.handle_if_src.handle_if") as mock_handle_if:
            def side_effect(s, f, lc, vo, no):
                lc["if_else"] = 5
                lc["if_end"] = 10
                return ("code", 5)

            mock_handle_if.side_effect = side_effect

            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(label_counter["if_else"], 5)
            self.assertEqual(label_counter["if_end"], 10)

    def test_var_offsets_passed_by_reference(self):
        """Test var_offsets is passed by reference to handlers."""
        stmt = {"type": "ASSIGN", "target": "x", "value": {}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"x": 0}
        next_offset = 1

        with patch("handle_if_package.generate_statement_code_package.handle_assign_package.handle_assign_src.handle_assign") as mock_handle_assign:
            def side_effect(s, f, lc, vo, no):
                vo["y"] = 5
                return ("code", 2)

            mock_handle_assign.side_effect = side_effect

            generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            self.assertEqual(var_offsets["y"], 5)


if __name__ == "__main__":
    unittest.main()
