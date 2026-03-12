import unittest
from unittest.mock import patch, call

# Relative import for the function under test
from .handle_while_src import handle_while


class TestHandleWhile(unittest.TestCase):
    """Test cases for handle_while function"""

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_simple_loop(self, mock_gen_expr, mock_gen_stmt):
        """Test basic while loop with one body statement"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": [{"type": "ASSIGN", "var": "i", "expr": {"type": "BINOP", "op": "-", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 1}}}]
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 5

        mock_gen_expr.return_value = ("PUSH 0\nCMP >", 6)
        mock_gen_stmt.return_value = ("ASSIGN i", 7)

        result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("test_func_while_start_0:", result_code)
        self.assertIn("PUSH 0\nCMP >", result_code)
        self.assertIn("JZ test_func_while_end_0", result_code)
        self.assertIn("ASSIGN i", result_code)
        self.assertIn("B test_func_while_start_0", result_code)
        self.assertIn("test_func_while_end_0:", result_code)
        self.assertEqual(result_offset, 7)
        self.assertEqual(label_counter["while_start"], 1)
        self.assertEqual(label_counter["while_end"], 1)

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_empty_body(self, mock_gen_expr, mock_gen_stmt):
        """Test while loop with empty body"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": []
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 5

        mock_gen_expr.return_value = ("PUSH 0\nCMP >", 6)
        mock_gen_stmt.return_value = ("", 6)

        result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("test_func_while_start_0:", result_code)
        self.assertIn("PUSH 0\nCMP >", result_code)
        self.assertIn("JZ test_func_while_end_0", result_code)
        self.assertIn("B test_func_while_start_0", result_code)
        self.assertIn("test_func_while_end_0:", result_code)
        self.assertEqual(result_offset, 6)
        self.assertEqual(label_counter["while_start"], 1)
        self.assertEqual(label_counter["while_end"], 1)

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_multiple_body_statements(self, mock_gen_expr, mock_gen_stmt):
        """Test while loop with multiple body statements"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": [
                {"type": "ASSIGN", "var": "i", "expr": {"type": "BINOP", "op": "-", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 1}}},
                {"type": "ASSIGN", "var": "sum", "expr": {"type": "BINOP", "op": "+", "left": {"type": "VAR", "name": "sum"}, "right": {"type": "VAR", "name": "i"}}}
            ]
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0, "sum": 1}
        next_offset = 5

        mock_gen_expr.return_value = ("PUSH 0\nCMP >", 6)
        mock_gen_stmt.side_effect = [("ASSIGN i", 7), ("ASSIGN sum", 8)]

        result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("test_func_while_start_0:", result_code)
        self.assertIn("PUSH 0\nCMP >", result_code)
        self.assertIn("JZ test_func_while_end_0", result_code)
        self.assertIn("ASSIGN i", result_code)
        self.assertIn("ASSIGN sum", result_code)
        self.assertIn("B test_func_while_start_0", result_code)
        self.assertIn("test_func_while_end_0:", result_code)
        self.assertEqual(result_offset, 8)
        self.assertEqual(mock_gen_stmt.call_count, 2)

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_non_zero_label_counter(self, mock_gen_expr, mock_gen_stmt):
        """Test while loop with non-zero initial label counter"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "x"}, "right": {"type": "CONST", "value": 0}},
            "body": [{"type": "ASSIGN", "var": "x", "expr": {"type": "CONST", "value": 1}}]
        }
        func_name = "my_func"
        label_counter = {"while_start": 3, "while_end": 5}
        var_offsets = {"x": 0}
        next_offset = 10

        mock_gen_expr.return_value = ("PUSH 1", 11)
        mock_gen_stmt.return_value = ("ASSIGN x", 11)

        result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("my_func_while_start_3:", result_code)
        self.assertIn("JZ my_func_while_end_5", result_code)
        self.assertEqual(label_counter["while_start"], 4)
        self.assertEqual(label_counter["while_end"], 6)

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_offset_propagation(self, mock_gen_expr, mock_gen_stmt):
        """Test that next_offset is properly propagated through expression and statement generation"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": [{"type": "ASSIGN", "var": "i", "expr": {"type": "BINOP", "op": "-", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 1}}}]
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 5

        mock_gen_expr.return_value = ("PUSH 0\nCMP >", 10)
        mock_gen_stmt.return_value = ("ASSIGN i", 15)

        result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(result_offset, 15)

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_expression_code_empty(self, mock_gen_expr, mock_gen_stmt):
        """Test while loop when expression code is empty"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CONST", "value": 1},
            "body": [{"type": "ASSIGN", "var": "x", "expr": {"type": "CONST", "value": 0}}]
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        mock_gen_expr.return_value = ("", 5)
        mock_gen_stmt.return_value = ("ASSIGN x", 6)

        result_code, result_offset = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertIn("test_func_while_start_0:", result_code)
        self.assertIn("JZ test_func_while_end_0", result_code)
        self.assertIn("ASSIGN x", result_code)
        self.assertIn("B test_func_while_start_0", result_code)
        self.assertIn("test_func_while_end_0:", result_code)
        self.assertEqual(result_offset, 6)

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_calls_generate_expression_code(self, mock_gen_expr, mock_gen_stmt):
        """Test that generate_expression_code is called with correct parameters"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": []
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 5

        mock_gen_expr.return_value = ("", 6)
        mock_gen_stmt.return_value = ("", 6)

        handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        mock_gen_expr.assert_called_once_with(
            {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            var_offsets,
            5
        )

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_calls_generate_statement_code(self, mock_gen_expr, mock_gen_stmt):
        """Test that generate_statement_code is called with correct parameters for each body statement"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": [
                {"type": "ASSIGN", "var": "i", "expr": {"type": "CONST", "value": 1}},
                {"type": "ASSIGN", "var": "j", "expr": {"type": "CONST", "value": 2}}
            ]
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0, "j": 1}
        next_offset = 5

        mock_gen_expr.return_value = ("", 6)
        mock_gen_stmt.side_effect = [("ASSIGN i", 7), ("ASSIGN j", 8)]

        handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(mock_gen_stmt.call_count, 2)
        mock_gen_stmt.assert_has_calls([
            call({"type": "ASSIGN", "var": "i", "expr": {"type": "CONST", "value": 1}}, "test_func", label_counter, var_offsets, 6),
            call({"type": "ASSIGN", "var": "j", "expr": {"type": "CONST", "value": 2}}, "test_func", label_counter, var_offsets, 7)
        ])

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_label_counter_mutation(self, mock_gen_expr, mock_gen_stmt):
        """Test that label_counter is mutated in-place"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": []
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 5

        mock_gen_expr.return_value = ("", 6)
        mock_gen_stmt.return_value = ("", 6)

        original_id = id(label_counter)
        handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        self.assertEqual(id(label_counter), original_id)
        self.assertEqual(label_counter["while_start"], 1)
        self.assertEqual(label_counter["while_end"], 1)

    @patch('generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_while_code_structure_order(self, mock_gen_expr, mock_gen_stmt):
        """Test that assembly code has correct structure and order"""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "op": ">", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 0}},
            "body": [{"type": "ASSIGN", "var": "i", "expr": {"type": "CONST", "value": 1}}]
        }
        func_name = "test_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 5

        mock_gen_expr.return_value = ("COND_CODE", 6)
        mock_gen_stmt.return_value = ("BODY_CODE", 7)

        result_code, _ = handle_while(stmt, func_name, label_counter, var_offsets, next_offset)

        lines = result_code.split('\n')
        self.assertGreater(len(lines), 0)
        self.assertTrue(lines[0].startswith("test_func_while_start_0:"))
        self.assertEqual(lines[1], "COND_CODE")
        self.assertEqual(lines[2].strip(), "JZ test_func_while_end_0")
        self.assertEqual(lines[3], "BODY_CODE")
        self.assertEqual(lines[4].strip(), "B test_func_while_start_0")
        self.assertTrue(lines[5].startswith("test_func_while_end_0:"))


if __name__ == '__main__':
    unittest.main()
