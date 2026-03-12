import unittest
from unittest.mock import patch

# Relative import from the same package
from .handle_if_src import handle_if


class TestHandleIf(unittest.TestCase):
    """Test cases for handle_if function."""

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_then_and_else(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with both then_body and else_body."""
        mock_gen_expr.return_value = ("    LOAD R0, 1", 11, "R0")
        mock_gen_stmt.side_effect = [
            ("    STORE R0, x", 12),
            ("    STORE R1, y", 13),
        ]
        
        stmt = {
            "type": "IF",
            "condition": {"type": "BINARY", "op": ">", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 0}},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 1}}],
            "else_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "LITERAL", "value": 0}}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0, "y": 1}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertEqual(final_offset, 13)
        
        lines = code.split("\n")
        self.assertIn("    LOAD R0, 1", lines)
        self.assertIn("    JZ test_func_if_else_0", lines)
        self.assertIn("    STORE R0, x", lines)
        self.assertIn("    B test_func_if_end_0", lines)
        self.assertIn("test_func_if_else_0:", lines)
        self.assertIn("    STORE R1, y", lines)
        self.assertIn("test_func_if_end_0:", lines)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_without_else_body(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with only then_body (no else_body)."""
        mock_gen_expr.return_value = ("    CMP R0, 0", 11, "R0")
        mock_gen_stmt.return_value = ("    ADD R0, 1", 12)
        
        stmt = {
            "type": "IF",
            "condition": {"type": "IDENT", "name": "flag"},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 1}}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertEqual(final_offset, 12)
        
        lines = code.split("\n")
        self.assertIn("    CMP R0, 0", lines)
        self.assertIn("    JZ test_func_if_else_0", lines)
        self.assertIn("    ADD R0, 1", lines)
        self.assertIn("    B test_func_if_end_0", lines)
        self.assertIn("test_func_if_else_0:", lines)
        self.assertIn("test_func_if_end_0:", lines)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_empty_then_body(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with empty then_body."""
        mock_gen_expr.return_value = ("    TEST R0", 11, "R0")
        
        stmt = {
            "type": "IF",
            "condition": {"type": "UNARY", "op": "NOT", "operand": {"type": "IDENT", "name": "flag"}},
            "then_body": [],
            "else_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "LITERAL", "value": 0}}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"y": 0}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        
        lines = code.split("\n")
        self.assertIn("    TEST R0", lines)
        self.assertIn("    JZ test_func_if_else_0", lines)
        self.assertIn("    B test_func_if_end_0", lines)
        self.assertIn("test_func_if_else_0:", lines)
        self.assertIn("test_func_if_end_0:", lines)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_empty_else_body(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with empty else_body list."""
        mock_gen_expr.return_value = ("    LOAD R0, 1", 11, "R0")
        mock_gen_stmt.return_value = ("    STORE R0, x", 12)
        
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 1}}],
            "else_body": [],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        
        lines = code.split("\n")
        self.assertIn("    LOAD R0, 1", lines)
        self.assertIn("    JZ test_func_if_else_0", lines)
        self.assertIn("    STORE R0, x", lines)
        self.assertIn("    B test_func_if_end_0", lines)
        self.assertIn("test_func_if_else_0:", lines)
        self.assertIn("test_func_if_end_0:", lines)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_multiple_then_statements(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with multiple statements in then_body."""
        mock_gen_expr.return_value = ("    CMP R0, 10", 11, "R0")
        mock_gen_stmt.side_effect = [
            ("    STORE R0, a", 12),
            ("    STORE R1, b", 13),
            ("    STORE R2, c", 14),
        ]
        
        stmt = {
            "type": "IF",
            "condition": {"type": "BINARY", "op": "<", "left": {"type": "IDENT", "name": "x"}, "right": {"type": "LITERAL", "value": 10}},
            "then_body": [
                {"type": "ASSIGN", "target": "a", "value": {"type": "IDENT", "name": "x"}},
                {"type": "ASSIGN", "target": "b", "value": {"type": "IDENT", "name": "y"}},
                {"type": "ASSIGN", "target": "c", "value": {"type": "IDENT", "name": "z"}},
            ],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"a": 0, "b": 1, "c": 2}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertEqual(final_offset, 14)
        
        lines = code.split("\n")
        self.assertIn("    CMP R0, 10", lines)
        self.assertIn("    JZ test_func_if_else_0", lines)
        self.assertIn("    STORE R0, a", lines)
        self.assertIn("    STORE R1, b", lines)
        self.assertIn("    STORE R2, c", lines)
        self.assertIn("    B test_func_if_end_0", lines)
        self.assertIn("test_func_if_else_0:", lines)
        self.assertIn("test_func_if_end_0:", lines)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_non_zero_label_counter(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with non-zero initial label counter."""
        mock_gen_expr.return_value = ("    LOAD R0, 1", 101, "R0")
        mock_gen_stmt.return_value = ("    STORE R0, x", 102)
        
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 1}}],
        }
        label_counter = {"if_else": 5, "if_end": 3}
        var_offsets = {"x": 0}
        next_offset = 100
        
        code, final_offset = handle_if(stmt, "my_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 6)
        self.assertEqual(label_counter["if_end"], 4)
        self.assertIn("my_func_if_else_5", code)
        self.assertIn("my_func_if_end_3", code)
        self.assertIn("    JZ my_func_if_else_5", code)
        self.assertIn("    B my_func_if_end_3", code)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_missing_condition(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with missing condition key."""
        mock_gen_expr.return_value = ("", 10, "R0")
        mock_gen_stmt.return_value = ("    NOP", 11)
        
        stmt = {
            "type": "IF",
            "then_body": [{"type": "NOP"}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertIn("    JZ test_func_if_else_0", code)
        self.assertIn("    B test_func_if_end_0", code)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_missing_then_body(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with missing then_body key."""
        mock_gen_expr.return_value = ("    LOAD R0, 1", 11, "R0")
        
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertIn("    LOAD R0, 1", code)
        self.assertIn("    JZ test_func_if_else_0", code)
        self.assertIn("    B test_func_if_end_0", code)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_with_missing_else_body(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement with missing else_body key."""
        mock_gen_expr.return_value = ("    LOAD R0, 1", 11, "R0")
        mock_gen_stmt.return_value = ("    STORE R0, x", 12)
        
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 1}}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(label_counter["if_else"], 1)
        self.assertEqual(label_counter["if_end"], 1)
        self.assertIn("test_func_if_else_0:", code)
        self.assertIn("test_func_if_end_0:", code)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_var_offsets_modified_in_place(self, mock_gen_expr, mock_gen_stmt):
        """Test that var_offsets is modified in-place by child functions."""
        mock_gen_expr.return_value = ("    LOAD R0, 1", 11, "R0")
        mock_gen_stmt.side_effect = [
            ("    STORE R0, x", 12),
            ("    STORE R1, y", 13),
        ]
        
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 1}}],
            "else_body": [{"type": "ASSIGN", "target": "y", "value": {"type": "LITERAL", "value": 0}}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0}
        next_offset = 10
        
        handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(mock_gen_stmt.call_count, 2)
        first_call_var_offsets = mock_gen_stmt.call_args_list[0][0][3]
        second_call_var_offsets = mock_gen_stmt.call_args_list[1][0][3]
        self.assertIs(first_call_var_offsets, var_offsets)
        self.assertIs(second_call_var_offsets, var_offsets)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_empty_condition_code(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement when generate_expression_code returns empty code."""
        mock_gen_expr.return_value = ("", 10, "R0")
        mock_gen_stmt.return_value = ("    STORE R0, x", 11)
        
        stmt = {
            "type": "IF",
            "condition": {"type": "IDENT", "name": "flag"},
            "then_body": [{"type": "ASSIGN", "target": "x", "value": {"type": "LITERAL", "value": 1}}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        lines = code.split("\n")
        self.assertNotIn("", lines)
        self.assertIn("    JZ test_func_if_else_0", lines)
        self.assertIn("    STORE R0, x", lines)

    @patch('handle_if_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code')
    @patch('handle_if_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_handle_if_empty_statement_code(self, mock_gen_expr, mock_gen_stmt):
        """Test IF statement when generate_statement_code returns empty code."""
        mock_gen_expr.return_value = ("    LOAD R0, 1", 11, "R0")
        mock_gen_stmt.return_value = ("", 12)
        
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [{"type": "NOP"}],
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 10
        
        code, final_offset = handle_if(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        lines = code.split("\n")
        self.assertNotIn("", lines)
        self.assertIn("    LOAD R0, 1", lines)
        self.assertIn("    JZ test_func_if_else_0", lines)
        self.assertIn("    B test_func_if_end_0", lines)


if __name__ == "__main__":
    unittest.main()
