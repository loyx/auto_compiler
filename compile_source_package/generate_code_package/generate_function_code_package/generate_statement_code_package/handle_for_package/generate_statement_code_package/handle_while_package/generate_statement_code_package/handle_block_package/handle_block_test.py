import unittest
from unittest.mock import patch
from typing import Dict

from .handle_block_src import handle_block


class TestHandleBlock(unittest.TestCase):
    """Test cases for handle_block function."""
    
    def test_empty_block(self):
        """Test handling of a block with no statements."""
        stmt = {"type": "BLOCK", "statements": []}
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, offset = handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "")
        self.assertEqual(offset, 0)
    
    def test_single_statement(self):
        """Test handling of a block with a single statement."""
        stmt = {
            "type": "BLOCK",
            "statements": [{"type": "VAR_DECL", "var_name": "x"}]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {"while_cond": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 4
        
        with patch(
            "handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("mov r0, #0", 8)
            
            code, offset = handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(code, "mov r0, #0")
            self.assertEqual(offset, 8)
            mock_gen.assert_called_once_with(
                stmt={"type": "VAR_DECL", "var_name": "x"},
                func_name="test_func",
                label_counter=label_counter,
                var_offsets=var_offsets,
                current_offset=4
            )
    
    def test_multiple_statements(self):
        """Test handling of a block with multiple statements."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "VAR_DECL", "var_name": "x"},
                {"type": "ASSIGN", "var_name": "x", "value": 5},
            ]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {"while_cond": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 4
        
        with patch(
            "handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.side_effect = [
                ("mov r0, #0", 8),
                ("mov r1, #5", 12),
            ]
            
            code, offset = handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
            
            expected_code = "mov r0, #0\nmov r1, #5"
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, 12)
            self.assertEqual(mock_gen.call_count, 2)
    
    def test_offset_accumulation(self):
        """Test that offsets accumulate correctly across statements."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "VAR_DECL", "var_name": "a"},
                {"type": "VAR_DECL", "var_name": "b"},
                {"type": "VAR_DECL", "var_name": "c"},
            ]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with patch(
            "handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.side_effect = [
                ("code_a", 4),
                ("code_b", 8),
                ("code_c", 12),
            ]
            
            code, offset = handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(offset, 12)
            calls = mock_gen.call_args_list
            self.assertEqual(calls[0][1]["current_offset"], 0)
            self.assertEqual(calls[1][1]["current_offset"], 4)
            self.assertEqual(calls[2][1]["current_offset"], 8)
    
    def test_code_joining_with_newlines(self):
        """Test that code from multiple statements is joined with newlines."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "ASSIGN", "var_name": "x", "value": 1},
                {"type": "ASSIGN", "var_name": "y", "value": 2},
            ]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with patch(
            "handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.side_effect = [
                ("line1", 4),
                ("line2", 8),
            ]
            
            code, offset = handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
            
            self.assertEqual(code, "line1\nline2")
    
    def test_no_statements_key(self):
        """Test handling when 'statements' key is missing from stmt."""
        stmt = {"type": "BLOCK"}
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 5
        
        code, offset = handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, "")
        self.assertEqual(offset, 5)
    
    def test_mutable_label_counter_passed_through(self):
        """Test that label_counter is passed to statement handlers (may be modified)."""
        stmt = {
            "type": "BLOCK",
            "statements": [{"type": "WHILE", "condition": "x > 0"}]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {"while_cond": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with patch(
            "handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("while_code", 4)
            
            handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
            
            mock_gen.assert_called_once()
            call_kwargs = mock_gen.call_args[1]
            self.assertIs(call_kwargs["label_counter"], label_counter)
    
    def test_mutable_var_offsets_passed_through(self):
        """Test that var_offsets is passed to statement handlers (may be modified)."""
        stmt = {
            "type": "BLOCK",
            "statements": [{"type": "VAR_DECL", "var_name": "x"}]
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {"existing_var": 0}
        next_offset = 4
        
        with patch(
            "handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("decl_code", 8)
            
            handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
            
            call_kwargs = mock_gen.call_args[1]
            self.assertIs(call_kwargs["var_offsets"], var_offsets)
    
    def test_func_name_passed_through(self):
        """Test that func_name is passed correctly to statement handlers."""
        stmt = {
            "type": "BLOCK",
            "statements": [{"type": "ASSIGN", "var_name": "x", "value": 1}]
        }
        func_name = "my_function"
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with patch(
            "handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("assign_code", 4)
            
            handle_block(stmt, func_name, label_counter, var_offsets, next_offset)
            
            call_kwargs = mock_gen.call_args[1]
            self.assertEqual(call_kwargs["func_name"], "my_function")


if __name__ == "__main__":
    unittest.main()
