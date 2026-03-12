# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === relative imports ===
from .handle_for_src import handle_for


class TestHandleFor(unittest.TestCase):
    """Test cases for handle_for function."""

    def test_complete_for_loop(self):
        """Test FOR loop with all sections: init, condition, update, and body."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "target": "i", "value": 0},
            "condition": {"type": "BINOP", "op": "<", "left": {"type": "IDENT", "name": "i"}, "right": {"type": "LITERAL", "value": 10}},
            "update": {"type": "ASSIGN", "target": "i", "value": {"type": "BINOP", "op": "+", "left": {"type": "IDENT", "name": "i"}, "right": {"type": "LITERAL", "value": 1}}},
            "body": [{"type": "EXPR", "expr": {"type": "IDENT", "name": "i"}}]
        }
        func_name = "test_func"
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        var_offsets = {"i": 0}
        next_offset = 10

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code") as mock_gen_stmt:
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.evaluate_expression") as mock_eval_expr:
                mock_gen_stmt.side_effect = [
                    ("    mov r0, #0\n", 10),  # init
                    ("    ldr r0, [sp, #0]\n", 10),  # body
                    ("    ldr r0, [sp, #0]\n    add r0, r0, #1\n", 10)  # update
                ]
                mock_eval_expr.return_value = "    ldr r0, [sp, #0]\n    cmp r0, #10\n"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify label counter was incremented
                self.assertEqual(label_counter["for_cond"], 1)
                self.assertEqual(label_counter["for_end"], 1)
                self.assertEqual(label_counter["for_update"], 1)

                # Verify labels are in code
                self.assertIn(".L_for_cond_0:", code)
                self.assertIn(".L_for_end_0:", code)
                self.assertIn(".L_for_update_0:", code)

                # Verify structure
                self.assertIn("cmp r0, #0", code)
                self.assertIn("beq .L_for_end_0", code)
                self.assertIn("b .L_for_cond_0", code)

                # Verify offset propagation
                self.assertEqual(updated_offset, 10)

    def test_for_loop_without_init(self):
        """Test FOR loop without init section."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": {"type": "LITERAL", "value": 1},
            "update": None,
            "body": []
        }
        func_name = "test_func"
        label_counter = {"for_cond": 5, "for_end": 3, "for_update": 2}
        var_offsets = {}
        next_offset = 5

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code") as mock_gen_stmt:
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.evaluate_expression") as mock_eval_expr:
                mock_eval_expr.return_value = "    mov r0, #1\n"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify no init code was generated (generate_statement_code not called for init)
                init_calls = [call for call in mock_gen_stmt.call_args_list if call[0][0] is stmt.get("init")]
                self.assertEqual(len(init_calls), 0)

                # Verify labels use correct indices
                self.assertIn(".L_for_cond_5:", code)
                self.assertIn(".L_for_end_3:", code)
                self.assertIn(".L_for_update_2:", code)

    def test_for_loop_without_update(self):
        """Test FOR loop without update section."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": {"type": "LITERAL", "value": 1},
            "update": None,
            "body": []
        }
        func_name = "test_func"
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        var_offsets = {}
        next_offset = 5

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code") as mock_gen_stmt:
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.evaluate_expression") as mock_eval_expr:
                mock_eval_expr.return_value = "    mov r0, #1\n"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify update label exists but no update code
                self.assertIn(".L_for_update_0:", code)
                # Verify generate_statement_code not called for update
                update_calls = [call for call in mock_gen_stmt.call_args_list if call[0][0] is stmt.get("update")]
                self.assertEqual(len(update_calls), 0)

    def test_for_loop_with_multiple_body_statements(self):
        """Test FOR loop with multiple body statements."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": {"type": "LITERAL", "value": 1},
            "update": None,
            "body": [
                {"type": "EXPR", "expr": {"type": "LITERAL", "value": 1}},
                {"type": "EXPR", "expr": {"type": "LITERAL", "value": 2}},
                {"type": "EXPR", "expr": {"type": "LITERAL", "value": 3}}
            ]
        }
        func_name = "test_func"
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        var_offsets = {}
        next_offset = 5

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code") as mock_gen_stmt:
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.evaluate_expression") as mock_eval_expr:
                mock_gen_stmt.side_effect = [
                    ("    mov r0, #1\n", 5),
                    ("    mov r0, #2\n", 5),
                    ("    mov r0, #3\n", 5)
                ]
                mock_eval_expr.return_value = "    mov r0, #1\n"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify generate_statement_code called 3 times for body
                body_calls = [call for call in mock_gen_stmt.call_args_list if call[0][0] in stmt["body"]]
                self.assertEqual(len(body_calls), 3)

    def test_for_loop_empty_body(self):
        """Test FOR loop with empty body."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": {"type": "LITERAL", "value": 1},
            "update": None,
            "body": []
        }
        func_name = "test_func"
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        var_offsets = {}
        next_offset = 5

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code") as mock_gen_stmt:
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.evaluate_expression") as mock_eval_expr:
                mock_eval_expr.return_value = "    mov r0, #1\n"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify no body statements processed
                self.assertEqual(mock_gen_stmt.call_count, 0)

    def test_for_loop_without_condition(self):
        """Test FOR loop without condition (infinite loop pattern)."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": None,
            "update": None,
            "body": []
        }
        func_name = "test_func"
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        var_offsets = {}
        next_offset = 5

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code") as mock_gen_stmt:
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.evaluate_expression") as mock_eval_expr:
                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify no condition evaluation code
                self.assertNotIn("cmp r0, #0", code)
                self.assertNotIn("beq .L_for_end_0", code)

                # Verify evaluate_expression not called
                mock_eval_expr.assert_not_called()

    def test_label_counter_increment(self):
        """Test that label_counter is incremented in-place for each label type."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": {"type": "LITERAL", "value": 1},
            "update": None,
            "body": []
        }
        func_name = "test_func"
        label_counter = {"for_cond": 10, "for_end": 20, "for_update": 30}
        var_offsets = {}
        next_offset = 5

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code"):
            with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.evaluate_expression") as mock_eval_expr:
                mock_eval_expr.return_value = "    mov r0, #1\n"

                handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify each counter incremented by 1
                self.assertEqual(label_counter["for_cond"], 11)
                self.assertEqual(label_counter["for_end"], 21)
                self.assertEqual(label_counter["for_update"], 31)

    def test_label_counter_missing_keys(self):
        """Test handle_for when label_counter is missing some keys."""
        stmt = {
            "type": "FOR",
            "init": None,
            "condition": {"type": "LITERAL", "value": 1},
            "update": None,
            "body": []
        }
        func_name = "test_func"
        label_counter = {}  # Empty label_counter
        var_offsets = {}
        next_offset = 5

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_for_package.handle_for_src.generate_statement_code"):
            with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval_expr:
                mock_eval_expr.return_value = "    mov r0, #1\n"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify labels use 0 as default
                self.assertIn(".L_for_cond_0:", code)
                self.assertIn(".L_for_end_0:", code)
                self.assertIn(".L_for_update_0:", code)

                # Verify counters were added
                self.assertEqual(label_counter["for_cond"], 1)
                self.assertEqual(label_counter["for_end"], 1)
                self.assertEqual(label_counter["for_update"], 1)

    def test_next_offset_propagation(self):
        """Test that next_offset is properly propagated through nested calls."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "target": "i", "value": 0},
            "condition": {"type": "LITERAL", "value": 1},
            "update": {"type": "ASSIGN", "target": "i", "value": 0},
            "body": [{"type": "ASSIGN", "target": "j", "value": 0}]
        }
        func_name = "test_func"
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        var_offsets = {"i": 0, "j": 1}
        next_offset = 10

        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval_expr:
                # Simulate offset changes through nested calls
                mock_gen_stmt.side_effect = [
                    ("    mov r0, #0\n", 11),  # init: offset increases
                    ("    mov r0, #0\n", 12),  # body: offset increases
                    ("    mov r0, #0\n", 13)  # update: offset increases
                ]
                mock_eval_expr.return_value = "    mov r0, #1\n"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify final offset is from last nested call
                self.assertEqual(updated_offset, 13)

    def test_code_order_structure(self):
        """Test that code sections appear in correct order: init, cond_label, condition, body, update_label, update, branch, end_label."""
        stmt = {
            "type": "FOR",
            "init": {"type": "ASSIGN", "target": "i", "value": 0},
            "condition": {"type": "LITERAL", "value": 1},
            "update": {"type": "ASSIGN", "target": "i", "value": 0},
            "body": [{"type": "EXPR", "expr": {"type": "LITERAL", "value": 1}}]
        }
        func_name = "test_func"
        label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        var_offsets = {"i": 0}
        next_offset = 5

        with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen_stmt:
            with patch("autoapp_workspace.workspace.projects.cc.files.main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval_expr:
                mock_gen_stmt.side_effect = [
                    ("INIT_CODE", 5),
                    ("BODY_CODE", 5),
                    ("UPDATE_CODE", 5)
                ]
                mock_eval_expr.return_value = "COND_CODE"

                code, updated_offset = handle_for(stmt, func_name, label_counter, var_offsets, next_offset)

                # Verify order by finding indices
                init_idx = code.find("INIT_CODE")
                cond_label_idx = code.find(".L_for_cond_0:")
                cond_code_idx = code.find("COND_CODE")
                body_idx = code.find("BODY_CODE")
                update_label_idx = code.find(".L_for_update_0:")
                update_idx = code.find("UPDATE_CODE")
                branch_idx = code.find("b .L_for_cond_0")
                end_label_idx = code.find(".L_for_end_0:")

                # Verify order
                self.assertLess(init_idx, cond_label_idx)
                self.assertLess(cond_label_idx, cond_code_idx)
                self.assertLess(cond_code_idx, body_idx)
                self.assertLess(body_idx, update_label_idx)
                self.assertLess(update_label_idx, update_idx)
                self.assertLess(update_idx, branch_idx)
                self.assertLess(branch_idx, end_label_idx)


if __name__ == "__main__":
    unittest.main()
