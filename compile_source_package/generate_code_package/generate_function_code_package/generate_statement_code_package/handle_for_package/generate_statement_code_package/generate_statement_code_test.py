import unittest
from unittest.mock import patch

from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code dispatch function."""

    def setUp(self):
        """Set up common test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"for_cond": 0, "if_else": 0}
        self.var_offsets = {"x": 0, "y": 4}
        self.next_offset = 8

    def test_dispatch_for_statement(self):
        """Test dispatch to handle_for for FOR statement type."""
        stmt = {"type": "FOR", "init": {}, "condition": {}, "update": {}, "body": {}}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_for") as mock_handler:
            mock_handler.return_value = ("FOR_CODE", 16)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once_with(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            self.assertEqual(code, "FOR_CODE")
            self.assertEqual(offset, 16)

    def test_dispatch_if_statement(self):
        """Test dispatch to handle_if for IF statement type."""
        stmt = {"type": "IF", "condition": {}, "then_body": {}, "else_body": {}}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_if") as mock_handler:
            mock_handler.return_value = ("IF_CODE", 20)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "IF_CODE")
            self.assertEqual(offset, 20)

    def test_dispatch_while_statement(self):
        """Test dispatch to handle_while for WHILE statement type."""
        stmt = {"type": "WHILE", "condition": {}, "body": {}}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_while") as mock_handler:
            mock_handler.return_value = ("WHILE_CODE", 24)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "WHILE_CODE")
            self.assertEqual(offset, 24)

    def test_dispatch_return_statement(self):
        """Test dispatch to handle_return for RETURN statement type."""
        stmt = {"type": "RETURN", "value": {}}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_return") as mock_handler:
            mock_handler.return_value = ("RETURN_CODE", 8)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "RETURN_CODE")
            self.assertEqual(offset, 8)

    def test_dispatch_assign_statement(self):
        """Test dispatch to handle_assign for ASSIGN statement type."""
        stmt = {"type": "ASSIGN", "target": "x", "value": {}}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_assign") as mock_handler:
            mock_handler.return_value = ("ASSIGN_CODE", 12)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "ASSIGN_CODE")
            self.assertEqual(offset, 12)

    def test_dispatch_block_statement(self):
        """Test dispatch to handle_block for BLOCK statement type."""
        stmt = {"type": "BLOCK", "statements": []}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_block") as mock_handler:
            mock_handler.return_value = ("BLOCK_CODE", 32)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "BLOCK_CODE")
            self.assertEqual(offset, 32)

    def test_dispatch_decl_statement(self):
        """Test dispatch to handle_decl for DECL statement type."""
        stmt = {"type": "DECL", "var_name": "z", "var_type": "int", "init_value": None}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_decl") as mock_handler:
            mock_handler.return_value = ("DECL_CODE", 12)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "DECL_CODE")
            self.assertEqual(offset, 12)

    def test_dispatch_call_statement(self):
        """Test dispatch to handle_call for CALL statement type."""
        stmt = {"type": "CALL", "func_name": "printf", "arguments": []}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_call") as mock_handler:
            mock_handler.return_value = ("CALL_CODE", 8)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "CALL_CODE")
            self.assertEqual(offset, 8)

    def test_dispatch_break_statement(self):
        """Test dispatch to handle_break for BREAK statement type."""
        stmt = {"type": "BREAK"}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_break") as mock_handler:
            mock_handler.return_value = ("BREAK_CODE", 8)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "BREAK_CODE")
            self.assertEqual(offset, 8)

    def test_dispatch_continue_statement(self):
        """Test dispatch to handle_continue for CONTINUE statement type."""
        stmt = {"type": "CONTINUE"}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_continue") as mock_handler:
            mock_handler.return_value = ("CONTINUE_CODE", 8)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handler.assert_called_once()
            self.assertEqual(code, "CONTINUE_CODE")
            self.assertEqual(offset, 8)

    def test_unsupported_statement_type_raises_valueerror(self):
        """Test that unsupported statement type raises ValueError."""
        stmt = {"type": "UNKNOWN_TYPE"}
        
        with self.assertRaises(ValueError) as context:
            generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
        
        self.assertIn("Unsupported statement type: UNKNOWN_TYPE", str(context.exception))

    def test_missing_type_field_treated_as_unknown(self):
        """Test that missing type field defaults to UNKNOWN and raises ValueError."""
        stmt = {}
        
        with self.assertRaises(ValueError) as context:
            generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
        
        self.assertIn("Unsupported statement type: UNKNOWN", str(context.exception))

    def test_handler_receives_all_parameters_unchanged(self):
        """Test that all parameters are passed correctly to handler."""
        stmt = {"type": "RETURN", "value": {}}
        original_label_counter = {"for_cond": 5}
        original_var_offsets = {"x": 0}
        original_offset = 100
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_return") as mock_handler:
            mock_handler.return_value = ("CODE", 100)
            
            generate_statement_code(
                stmt, self.func_name, original_label_counter, original_var_offsets, original_offset
            )
            
            call_args = mock_handler.call_args
            self.assertIs(call_args[0][0], stmt)
            self.assertEqual(call_args[0][1], self.func_name)
            self.assertIs(call_args[0][2], original_label_counter)
            self.assertIs(call_args[0][3], original_var_offsets)
            self.assertEqual(call_args[0][4], original_offset)

    def test_handler_return_value_propagated_correctly(self):
        """Test that handler's return value is propagated correctly."""
        stmt = {"type": "IF", "condition": {}, "then_body": {}}
        
        with patch("generate_statement_code_package.generate_statement_code_src.handle_if") as mock_handler:
            mock_handler.return_value = ("COMPLEX_CODE_WITH_LABELS", 999)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertEqual(code, "COMPLEX_CODE_WITH_LABELS")
            self.assertEqual(offset, 999)

    def test_label_counter_may_be_modified_by_handler(self):
        """Test that label_counter can be modified in-place by handler."""
        stmt = {"type": "FOR", "init": {}, "condition": {}, "update": {}, "body": {}}
        
        with patch("generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.generate_statement_code_src.handle_for") as mock_handler:
            def side_effect(s, fn, lc, vo, no):
                lc["for_cond"] = 10
                lc["for_end"] = 11
                return ("CODE", 16)
            
            mock_handler.side_effect = side_effect
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertEqual(self.label_counter["for_cond"], 10)
            self.assertEqual(self.label_counter["for_end"], 11)


if __name__ == "__main__":
    unittest.main()
