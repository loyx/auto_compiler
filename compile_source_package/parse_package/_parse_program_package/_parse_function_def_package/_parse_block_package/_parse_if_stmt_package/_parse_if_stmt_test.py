import pytest
from unittest.mock import patch

from ._parse_if_stmt_src import _parse_if_stmt


class TestParseIfStmt:
    """Test cases for _parse_if_stmt function."""

    def test_simple_if_statement(self):
        """Test parsing a simple if statement without elif/else."""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition = {"type": "BINARY_OP", "value": ">", "line": 1, "column": 4}
        mock_body = {"type": "BLOCK", "children": [], "line": 1, "column": 10}

        with patch(
            "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_expression",
            return_value=mock_condition,
        ):
            with patch(
                "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_block",
                return_value=mock_body,
            ):
                result = _parse_if_stmt(parser_state)

        assert result["type"] == "IF_STMT"
        assert len(result["children"]) == 2
        assert result["children"][0] == mock_condition
        assert result["children"][1] == mock_body
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_if_with_elif(self):
        """Test parsing if statement with one elif clause."""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "ELIF", "value": "elif", "line": 2, "column": 1},
            {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_if_condition = {"type": "BINARY_OP", "value": ">", "line": 1, "column": 4}
        mock_if_body = {"type": "BLOCK", "children": [], "line": 1, "column": 10}
        mock_elif_condition = {"type": "BINARY_OP", "value": "<", "line": 2, "column": 6}
        mock_elif_body = {"type": "BLOCK", "children": [], "line": 2, "column": 12}

        call_count = {"value": 0}

        def mock_parse_expression(state):
            call_count["value"] += 1
            if call_count["value"] == 1:
                return mock_if_condition
            else:
                return mock_elif_condition

        def mock_parse_block(state):
            if call_count["value"] == 1:
                return mock_if_body
            else:
                return mock_elif_body

        with patch(
            "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_expression",
            side_effect=mock_parse_expression,
        ):
            with patch(
                "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_block",
                side_effect=mock_parse_block,
            ):
                result = _parse_if_stmt(parser_state)

        assert result["type"] == "IF_STMT"
        assert len(result["children"]) == 3
        assert result["children"][0] == mock_if_condition
        assert result["children"][1] == mock_if_body
        assert result["children"][2]["type"] == "ELIF_STMT"
        assert result["children"][2]["children"][0] == mock_elif_condition
        assert result["children"][2]["children"][1] == mock_elif_body
        assert result["children"][2]["line"] == 2
        assert result["children"][2]["column"] == 1

    def test_if_with_multiple_elif(self):
        """Test parsing if statement with multiple elif clauses."""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "ELIF", "value": "elif", "line": 2, "column": 1},
            {"type": "ELIF", "value": "elif", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_if_condition = {"type": "BINARY_OP", "value": "==", "line": 1, "column": 4}
        mock_if_body = {"type": "BLOCK", "children": [], "line": 1, "column": 10}
        mock_elif1_condition = {"type": "BINARY_OP", "value": ">", "line": 2, "column": 6}
        mock_elif1_body = {"type": "BLOCK", "children": [], "line": 2, "column": 12}
        mock_elif2_condition = {"type": "BINARY_OP", "value": "<", "line": 3, "column": 6}
        mock_elif2_body = {"type": "BLOCK", "children": [], "line": 3, "column": 12}

        call_sequence = [
            (mock_if_condition, mock_if_body),
            (mock_elif1_condition, mock_elif1_body),
            (mock_elif2_condition, mock_elif2_body),
        ]
        call_index = {"value": 0}

        def mock_parse_expression(state):
            idx = call_index["value"]
            return call_sequence[idx][0]

        def mock_parse_block(state):
            idx = call_index["value"]
            result = call_sequence[idx][1]
            call_index["value"] += 1
            return result

        with patch(
            "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_expression",
            side_effect=mock_parse_expression,
        ):
            with patch(
                "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_block",
                side_effect=mock_parse_block,
            ):
                result = _parse_if_stmt(parser_state)

        assert result["type"] == "IF_STMT"
        assert len(result["children"]) == 4
        assert result["children"][2]["type"] == "ELIF_STMT"
        assert result["children"][3]["type"] == "ELIF_STMT"

    def test_if_with_else(self):
        """Test parsing if statement with else clause."""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "ELSE", "value": "else", "line": 2, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition = {"type": "BINARY_OP", "value": ">", "line": 1, "column": 4}
        mock_if_body = {"type": "BLOCK", "children": [], "line": 1, "column": 10}
        mock_else_body = {"type": "BLOCK", "children": [], "line": 2, "column": 6}

        call_count = {"value": 0}

        def mock_parse_expression(state):
            call_count["value"] += 1
            return mock_condition

        def mock_parse_block(state):
            if call_count["value"] == 1:
                return mock_if_body
            else:
                return mock_else_body

        with patch(
            "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_expression",
            side_effect=mock_parse_expression,
        ):
            with patch(
                "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_block",
                side_effect=mock_parse_block,
            ):
                result = _parse_if_stmt(parser_state)

        assert result["type"] == "IF_STMT"
        assert len(result["children"]) == 3
        assert result["children"][0] == mock_condition
        assert result["children"][1] == mock_if_body
        assert result["children"][2]["type"] == "ELSE_STMT"
        assert result["children"][2]["children"][0] == mock_else_body
        assert result["children"][2]["line"] == 2
        assert result["children"][2]["column"] == 1

    def test_if_with_elif_and_else(self):
        """Test parsing if statement with both elif and else clauses."""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "ELIF", "value": "elif", "line": 2, "column": 1},
            {"type": "ELSE", "value": "else", "line": 3, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_if_condition = {"type": "BINARY_OP", "value": "==", "line": 1, "column": 4}
        mock_if_body = {"type": "BLOCK", "children": [], "line": 1, "column": 10}
        mock_elif_condition = {"type": "BINARY_OP", "value": ">", "line": 2, "column": 6}
        mock_elif_body = {"type": "BLOCK", "children": [], "line": 2, "column": 12}
        mock_else_body = {"type": "BLOCK", "children": [], "line": 3, "column": 6}

        call_sequence = [
            (mock_if_condition, mock_if_body),
            (mock_elif_condition, mock_elif_body),
        ]
        call_index = {"value": 0}

        def mock_parse_expression(state):
            idx = call_index["value"]
            return call_sequence[idx][0]

        def mock_parse_block(state):
            idx = call_index["value"]
            result = call_sequence[idx][1]
            call_index["value"] += 1
            return result

        with patch(
            "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_expression",
            side_effect=mock_parse_expression,
        ):
            with patch(
                "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_block",
                side_effect=mock_parse_block,
            ):
                result = _parse_if_stmt(parser_state)

        assert result["type"] == "IF_STMT"
        assert len(result["children"]) == 4
        assert result["children"][2]["type"] == "ELIF_STMT"
        assert result["children"][3]["type"] == "ELSE_STMT"

    def test_missing_if_token_raises_syntax_error(self):
        """Test that missing IF token raises SyntaxError."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_if_stmt(parser_state)

        assert "Expected IF token at position 0" in str(exc_info.value)

    def test_missing_if_token_at_end_raises_syntax_error(self):
        """Test that IF token missing at end of tokens raises SyntaxError."""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_if_stmt(parser_state)

        assert "Expected IF token at position 0" in str(exc_info.value)

    def test_if_token_at_wrong_position_raises_syntax_error(self):
        """Test that IF token at wrong position raises SyntaxError."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "IF", "value": "if", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_if_stmt(parser_state)

        assert "Expected IF token at position 0" in str(exc_info.value)

    def test_parser_state_position_updated_correctly(self):
        """Test that parser state position is updated correctly after parsing."""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "ELSE", "value": "else", "line": 2, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition = {"type": "BINARY_OP", "value": ">", "line": 1, "column": 4}
        mock_if_body = {"type": "BLOCK", "children": [], "line": 1, "column": 10}
        mock_else_body = {"type": "BLOCK", "children": [], "line": 2, "column": 6}

        call_count = {"value": 0}

        def mock_parse_expression(state):
            call_count["value"] += 1
            return mock_condition

        def mock_parse_block(state):
            if call_count["value"] == 1:
                return mock_if_body
            else:
                return mock_else_body

        with patch(
            "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_expression",
            side_effect=mock_parse_expression,
        ):
            with patch(
                "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_block",
                side_effect=mock_parse_block,
            ):
                result = _parse_if_stmt(parser_state)

        assert parser_state["pos"] == 2

    def test_if_statement_preserves_line_column_info(self):
        """Test that IF statement preserves line and column information from IF token."""
        tokens = [
            {"type": "IF", "value": "if", "line": 5, "column": 10},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition = {"type": "BINARY_OP", "value": ">", "line": 5, "column": 13}
        mock_body = {"type": "BLOCK", "children": [], "line": 5, "column": 19}

        with patch(
            "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_expression",
            return_value=mock_condition,
        ):
            with patch(
                "compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_block",
                return_value=mock_body,
            ):
                result = _parse_if_stmt(parser_state)

        assert result["line"] == 5
        assert result["column"] == 10
