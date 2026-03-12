"""Unit tests for handle_block function."""

from typing import Dict
from unittest.mock import patch

# Relative import from the same package
from .handle_block_src import handle_block


class TestHandleBlock:
    """Test cases for handle_block function."""

    def test_empty_block_returns_empty_string(self):
        """Test that a block with no statements returns empty string and unchanged offset."""
        stmt = {"type": "BLOCK", "statements": []}
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        
        code, offset = handle_block(stmt, "test_func", label_counter, var_offsets, 100)
        
        assert code == ""
        assert offset == 100

    def test_single_statement_block(self):
        """Test block with a single statement delegates correctly."""
        stmt = {"type": "BLOCK", "statements": [{"type": "EXPR", "value": "test"}]}
        label_counter: Dict[str, int] = {"for_cond": 0}
        var_offsets: Dict[str, int] = {"x": 10}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("mov x0, #1", 104)
            
            code, offset = handle_block(stmt, "test_func", label_counter, var_offsets, 100)
            
            assert code == "mov x0, #1"
            assert offset == 104
            mock_gen.assert_called_once_with(
                {"type": "EXPR", "value": "test"},
                "test_func",
                label_counter,
                var_offsets,
                100
            )

    def test_multiple_statements_concatenated_with_newlines(self):
        """Test that multiple statements are concatenated with newline separators."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "EXPR", "value": "first"},
                {"type": "EXPR", "value": "second"},
                {"type": "EXPR", "value": "third"}
            ]
        }
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.side_effect = [
                ("code1", 104),
                ("code2", 108),
                ("code3", 112)
            ]
            
            code, offset = handle_block(stmt, "my_func", label_counter, var_offsets, 100)
            
            assert code == "code1\ncode2\ncode3"
            assert offset == 112
            assert mock_gen.call_count == 3

    def test_offset_accumulates_across_statements(self):
        """Test that offset is properly accumulated and passed to each subsequent statement."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "STMT1"},
                {"type": "STMT2"},
                {"type": "STMT3"}
            ]
        }
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.side_effect = [
                ("asm1", 108),   # starts at 100, ends at 108
                ("asm2", 112),   # starts at 108, ends at 112
                ("asm3", 120)    # starts at 112, ends at 120
            ]
            
            code, offset = handle_block(stmt, "func", label_counter, var_offsets, 100)
            
            # Verify each call received the correct offset from previous statement
            calls = mock_gen.call_args_list
            assert calls[0][0][4] == 100   # first call offset
            assert calls[1][0][4] == 108   # second call offset
            assert calls[2][0][4] == 112   # third call offset
            
            assert offset == 120

    def test_label_counter_passed_to_children(self):
        """Test that label_counter is passed through to child statement handlers."""
        stmt = {"type": "BLOCK", "statements": [{"type": "FOR"}]}
        label_counter: Dict[str, int] = {"for_cond": 5, "for_end": 10}
        var_offsets: Dict[str, int] = {}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("loop_code", 104)
            
            handle_block(stmt, "test", label_counter, var_offsets, 100)
            
            # Verify label_counter was passed (same object reference)
            call_args = mock_gen.call_args
            assert call_args[0][2] is label_counter

    def test_var_offsets_passed_to_children(self):
        """Test that var_offsets is passed through to child statement handlers."""
        stmt = {"type": "BLOCK", "statements": [{"type": "ASSIGN"}]}
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {"x": 100, "y": 104}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("assign_code", 108)
            
            handle_block(stmt, "test", label_counter, var_offsets, 100)
            
            # Verify var_offsets was passed (same object reference)
            call_args = mock_gen.call_args
            assert call_args[0][3] is var_offsets

    def test_func_name_passed_to_children(self):
        """Test that func_name is passed through to child statement handlers."""
        stmt = {"type": "BLOCK", "statements": [{"type": "CALL"}]}
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("call_code", 104)
            
            handle_block(stmt, "my_awesome_function", label_counter, var_offsets, 100)
            
            call_args = mock_gen.call_args
            assert call_args[0][1] == "my_awesome_function"

    def test_statements_missing_key_defaults_to_empty(self):
        """Test that missing 'statements' key defaults to empty list."""
        stmt = {"type": "BLOCK"}  # No statements key
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        
        code, offset = handle_block(stmt, "test", label_counter, var_offsets, 50)
        
        assert code == ""
        assert offset == 50

    def test_zero_offset_start(self):
        """Test block processing starting from offset 0."""
        stmt = {"type": "BLOCK", "statements": [{"type": "INIT"}]}
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.return_value = ("init_seq", 16)
            
            code, offset = handle_block(stmt, "main", label_counter, var_offsets, 0)
            
            assert code == "init_seq"
            assert offset == 16

    def test_large_offset_values(self):
        """Test block processing with large offset values."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "A"},
                {"type": "B"}
            ]
        }
        label_counter: Dict[str, int] = {}
        var_offsets: Dict[str, int] = {}
        
        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_block_package.handle_block_src.generate_statement_code"
        ) as mock_gen:
            mock_gen.side_effect = [
                ("code_a", 10000),
                ("code_b", 20000)
            ]
            
            code, offset = handle_block(stmt, "test", label_counter, var_offsets, 5000)
            
            assert code == "code_a\ncode_b"
            assert offset == 20000
