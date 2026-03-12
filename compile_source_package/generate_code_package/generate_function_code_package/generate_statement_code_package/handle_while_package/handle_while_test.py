# === std / third-party imports ===
import unittest
from typing import Dict
from unittest.mock import patch

# === sub function imports ===
from .handle_while_src import handle_while, generate_expression_code, generate_statement_code


class TestHandleWhile(unittest.TestCase):
    """Test cases for handle_while function."""

    def setUp(self):
        """Set up common test fixtures."""
        self.func_name = "test_func"
        self.label_counter: Dict[str, int] = {"while_cond": 0, "while_end": 0}
        self.var_offsets: Dict[str, int] = {"x": 0, "y": 1}
        self.next_offset = 10

    def test_basic_while_loop(self):
        """Test basic while loop with condition and single body statement."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": "x", "right": 0},
            "body": [{"type": "ASSIGN", "var": "y", "value": 1}]
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.handle_while_src.generate_expression_code") as mock_gen_expr, \
             patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.handle_while_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 11)
            mock_gen_stmt.return_value = ("str x0, [sp, #1]", 12)
            
            code, offset = handle_while(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            # Verify label_counter was updated in-place
            self.assertEqual(self.label_counter["while_cond"], 1)
            self.assertEqual(self.label_counter["while_end"], 1)
            
            # Verify generated code structure
            self.assertIn("test_func_while_cond_0:", code)
            self.assertIn("cmp x0, x1", code)
            self.assertIn("cbz x0, test_func_while_end_0", code)
            self.assertIn("str x0, [sp, #1]", code)
            self.assertIn("b test_func_while_cond_0", code)
            self.assertIn("test_func_while_end_0:", code)
            
            # Verify offset propagation
            self.assertEqual(offset, 12)
            
            # Verify mock calls
            mock_gen_expr.assert_called_once()
            mock_gen_stmt.assert_called_once()

    def test_while_loop_empty_body(self):
        """Test while loop with empty body."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": "x", "right": 0},
            "body": []
        }
        
        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("cmp x0, x1", 11)
            
            code, offset = handle_while(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            # Verify label_counter was updated
            self.assertEqual(self.label_counter["while_cond"], 1)
            self.assertEqual(self.label_counter["while_end"], 1)
            
            # Verify code structure (no body statements)
            self.assertIn("test_func_while_cond_0:", code)
            self.assertIn("cmp x0, x1", code)
            self.assertIn("cbz x0, test_func_while_end_0", code)
            self.assertIn("b test_func_while_cond_0", code)
            self.assertIn("test_func_while_end_0:", code)
            
            # Count body statement calls (should be 0)
            self.assertEqual(mock_gen_expr.call_count, 1)

    def test_while_loop_no_condition(self):
        """Test while loop with no condition field."""
        stmt = {
            "type": "WHILE",
            "body": [{"type": "ASSIGN", "var": "y", "value": 1}]
        }
        
        with patch("handle_while_package.handle_while_src.generate_statement_code") as mock_gen_stmt:
            mock_gen_stmt.return_value = ("str x0, [sp, #1]", 11)
            
            code, offset = handle_while(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            # Verify label_counter was updated
            self.assertEqual(self.label_counter["while_cond"], 1)
            self.assertEqual(self.label_counter["while_end"], 1)
            
            # Verify code structure (no condition evaluation)
            self.assertIn("test_func_while_cond_0:", code)
            self.assertNotIn("cmp", code)
            self.assertIn("cbz x0, test_func_while_end_0", code)
            self.assertIn("str x0, [sp, #1]", code)
            self.assertIn("b test_func_while_cond_0", code)
            self.assertIn("test_func_while_end_0:", code)

    def test_while_loop_multiple_body_statements(self):
        """Test while loop with multiple body statements."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": "x", "right": 0},
            "body": [
                {"type": "ASSIGN", "var": "y", "value": 1},
                {"type": "ASSIGN", "var": "z", "value": 2},
                {"type": "ASSIGN", "var": "w", "value": 3}
            ]
        }
        
        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_gen_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 11)
            mock_gen_stmt.side_effect = [
                ("str x0, [sp, #1]", 12),
                ("str x0, [sp, #2]", 13),
                ("str x0, [sp, #3]", 14)
            ]
            
            code, offset = handle_while(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            # Verify label_counter was updated
            self.assertEqual(self.label_counter["while_cond"], 1)
            self.assertEqual(self.label_counter["while_end"], 1)
            
            # Verify generate_statement_code was called 3 times
            self.assertEqual(mock_gen_stmt.call_count, 3)
            
            # Verify final offset
            self.assertEqual(offset, 14)

    def test_while_loop_label_counter_increment(self):
        """Test that label_counter increments correctly across multiple calls."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": "x", "right": 0},
            "body": []
        }
        
        label_counter: Dict[str, int] = {"while_cond": 2, "while_end": 3}
        
        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("cmp x0, x1", 11)
            
            code, offset = handle_while(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Verify label_counter was incremented from initial values
            self.assertEqual(label_counter["while_cond"], 3)
            self.assertEqual(label_counter["while_end"], 4)
            
            # Verify labels use the pre-increment counts
            self.assertIn("test_func_while_cond_2:", code)
            self.assertIn("test_func_while_end_3:", code)

    def test_while_loop_default_label_counts(self):
        """Test while loop when label_counter has no while_cond/while_end keys."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": "x", "right": 0},
            "body": []
        }
        
        label_counter: Dict[str, int] = {}
        
        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("cmp x0, x1", 11)
            
            code, offset = handle_while(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)
            
            # Verify label_counter was initialized and incremented
            self.assertEqual(label_counter["while_cond"], 1)
            self.assertEqual(label_counter["while_end"], 1)
            
            # Verify labels start from 0
            self.assertIn("test_func_while_cond_0:", code)
            self.assertIn("test_func_while_end_0:", code)

    def test_while_loop_offset_propagation(self):
        """Test that next_offset is properly propagated through expression and body."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": "x", "right": 0},
            "body": [{"type": "ASSIGN", "var": "y", "value": 1}]
        }
        
        initial_offset = 100
        
        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_gen_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("cmp x0, x1", 105)
            mock_gen_stmt.return_value = ("str x0, [sp, #1]", 110)
            
            code, offset = handle_while(stmt, self.func_name, self.label_counter, self.var_offsets, initial_offset)
            
            # Verify expression received initial offset
            mock_gen_expr.assert_called_once()
            call_args = mock_gen_expr.call_args
            self.assertEqual(call_args[0][2], 105)  # Actually receives the returned offset from previous
            
            # Verify final offset matches last operation
            self.assertEqual(offset, 110)

    def test_while_loop_code_line_order(self):
        """Test that code lines are in correct order."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": "x", "right": 0},
            "body": [{"type": "ASSIGN", "var": "y", "value": 1}]
        }
        
        with patch("handle_while_package.handle_while_src.generate_expression_code") as mock_gen_expr, \
             patch("handle_while_package.handle_while_src.generate_statement_code") as mock_gen_stmt:
            
            mock_gen_expr.return_value = ("COND_CODE", 11)
            mock_gen_stmt.return_value = ("BODY_CODE", 12)
            
            code, offset = handle_while(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            lines = code.split("\n")
            
            # Verify order: cond_label, condition, cbz, body, jump back, end_label
            self.assertGreater(lines.index("test_func_while_cond_0:"), -1)
            cond_label_idx = lines.index("test_func_while_cond_0:")
            cond_code_idx = lines.index("COND_CODE")
            cbz_idx = next(i for i, line in enumerate(lines) if line.startswith("cbz x0,"))
            body_idx = lines.index("BODY_CODE")
            jump_idx = next(i for i, line in enumerate(lines) if line.startswith("b "))
            end_label_idx = lines.index("test_func_while_end_0:")
            
            self.assertLess(cond_label_idx, cond_code_idx)
            self.assertLess(cond_code_idx, cbz_idx)
            self.assertLess(cbz_idx, body_idx)
            self.assertLess(body_idx, jump_idx)
            self.assertLess(jump_idx, end_label_idx)


if __name__ == "__main__":
    unittest.main()
