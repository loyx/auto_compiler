# === std / third-party imports ===
from unittest.mock import patch

# === relative imports ===
from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode:
    """Test suite for generate_statement_code function."""

    def test_assign_statement_dispatch(self):
        """Test ASSIGN statement dispatches to handle_assign_stmt."""
        stmt = {"type": "ASSIGN", "target": "x", "value": {"type": "CONST", "value": 5}}
        func_name = "test_func"
        label_counter = {"while_cond": 0}
        var_offsets = {"x": 0}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.handle_assign_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("STORE_OFFSET x0, [sp, #0]", 16)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("STORE_OFFSET x0, [sp, #0]", 16)

    def test_if_statement_dispatch(self):
        """Test IF statement dispatches to handle_if_stmt."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CMP", "left": {"type": "VAR", "name": "x"}, "right": {"type": "CONST", "value": 0}},
            "then_body": [{"type": "PASS"}],
            "else_body": [],
        }
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.handle_if_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("CBZ x0, L_if_else_0\nL_if_end_0:", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("CBZ x0, L_if_else_0\nL_if_end_0:", 8)

    def test_while_statement_dispatch(self):
        """Test WHILE statement dispatches to handle_while_stmt."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CMP", "left": {"type": "VAR", "name": "i"}, "right": {"type": "CONST", "value": 10}},
            "body": [{"type": "PASS"}],
        }
        func_name = "test_func"
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.handle_while_stmt_src.handle_while_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("L_while_cond_0:\nB L_while_end_0", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("L_while_cond_0:\nB L_while_end_0", 8)

    def test_return_statement_dispatch(self):
        """Test RETURN statement dispatches to handle_return_stmt."""
        stmt = {"type": "RETURN", "expression": {"type": "CONST", "value": 0}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.handle_return_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("MOV x0, #0\nret", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("MOV x0, #0\nret", 8)

    def test_call_statement_dispatch(self):
        """Test CALL statement dispatches to handle_call_stmt."""
        stmt = {"type": "CALL", "function": "printf", "args": [{"type": "CONST", "value": 42}]}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_call_stmt_package.handle_call_stmt_src.handle_call_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("MOV x0, #42\nbl printf", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("MOV x0, #42\nbl printf", 8)

    def test_break_statement_dispatch(self):
        """Test BREAK statement dispatches to handle_break_stmt."""
        stmt = {"type": "BREAK"}
        func_name = "test_func"
        label_counter = {"break": 0}
        var_offsets = {}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_break_stmt_package.handle_break_stmt_src.handle_break_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("B L_while_end_0", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("B L_while_end_0", 8)

    def test_continue_statement_dispatch(self):
        """Test CONTINUE statement dispatches to handle_continue_stmt."""
        stmt = {"type": "CONTINUE"}
        func_name = "test_func"
        label_counter = {"continue": 0}
        var_offsets = {}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_continue_stmt_package.handle_continue_stmt_src.handle_continue_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("B L_while_cond_0", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("B L_while_cond_0", 8)

    def test_pass_statement_dispatch(self):
        """Test PASS statement dispatches to handle_pass_stmt."""
        stmt = {"type": "PASS"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_pass_stmt_package.handle_pass_stmt_src.handle_pass_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            mock_handler.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            assert result == ("", 8)

    def test_unknown_statement_type(self):
        """Test unknown statement type returns empty code and unchanged offset."""
        stmt = {"type": "UNKNOWN_TYPE"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        assert result == ("", 8)

    def test_missing_statement_type(self):
        """Test missing type field returns empty code and unchanged offset."""
        stmt = {"target": "x", "value": {"type": "CONST", "value": 5}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        assert result == ("", 8)

    def test_empty_statement_dict(self):
        """Test empty statement dict returns empty code and unchanged offset."""
        stmt = {}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

        assert result == ("", 8)

    def test_label_counter_modified_in_place(self):
        """Test that label_counter can be modified by handlers (verified through mock)."""
        stmt = {"type": "IF", "condition": {}, "then_body": [], "else_body": []}
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 8

        def side_effect(s, f, lc, v, n):
            lc["if_else"] = 1
            lc["if_end"] = 1
            return ("", 8)

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.handle_if_stmt_src.handle_if_stmt"
        ) as mock_handler:
            mock_handler.side_effect = side_effect
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            assert label_counter["if_else"] == 1
            assert label_counter["if_end"] == 1
            assert result == ("", 8)

    def test_var_offsets_modified_in_place(self):
        """Test that var_offsets can be modified by handlers (verified through mock)."""
        stmt = {"type": "ASSIGN", "target": "y", "value": {"type": "CONST", "value": 10}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {"x": 0}
        next_offset = 8

        def side_effect(s, f, lc, vo, n):
            vo["y"] = 8
            return ("", 16)

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.handle_assign_stmt"
        ) as mock_handler:
            mock_handler.side_effect = side_effect
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            assert var_offsets["y"] == 8
            assert result == ("", 16)

    def test_next_offset_updated(self):
        """Test that next_offset is properly updated and returned."""
        stmt = {"type": "ASSIGN", "target": "x", "value": {"type": "CONST", "value": 5}}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_assign_stmt_package.handle_assign_stmt_src.handle_assign_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("STORE_OFFSET", 24)
            code, new_offset = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            assert new_offset == 24
            assert code == "STORE_OFFSET"

    def test_handler_return_type_tuple(self):
        """Test that handler returns proper Tuple[str, int] type."""
        stmt = {"type": "PASS"}
        func_name = "test_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 8

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_pass_stmt_package.handle_pass_stmt_src.handle_pass_stmt"
        ) as mock_handler:
            mock_handler.return_value = ("", 8)
            result = generate_statement_code(stmt, func_name, label_counter, var_offsets, next_offset)

            assert isinstance(result, tuple)
            assert len(result) == 2
            assert isinstance(result[0], str)
            assert isinstance(result[1], int)
