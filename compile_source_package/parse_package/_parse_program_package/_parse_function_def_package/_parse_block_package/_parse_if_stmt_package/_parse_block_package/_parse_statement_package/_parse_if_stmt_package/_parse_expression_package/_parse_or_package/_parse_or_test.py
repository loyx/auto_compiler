from unittest.mock import patch

from ._parse_or_src import _parse_or


class TestParseOr:
    """Test cases for _parse_or function."""

    def test_single_and_expression_no_or(self):
        """Test parsing a single AND expression without OR operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_node = {
            "type": "IDENTIFIER",
            "name": "a",
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.return_value = mock_and_node

            result = _parse_or(parser_state)

            assert result == mock_and_node
            assert parser_state["pos"] == 1
            mock_parse_and.assert_called_once()

    def test_one_or_operator(self):
        """Test parsing expression with one OR operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_node_a = {
            "type": "IDENTIFIER",
            "name": "a",
            "line": 1,
            "column": 1
        }
        mock_and_node_b = {
            "type": "IDENTIFIER",
            "name": "b",
            "line": 1,
            "column": 6
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [mock_and_node_a, mock_and_node_b]

            result = _parse_or(parser_state)

            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "||"
            assert result["left"] == mock_and_node_a
            assert result["right"] == mock_and_node_b
            assert result["line"] == 1
            assert result["column"] == 3
            assert parser_state["pos"] == 3
            assert mock_parse_and.call_count == 2

    def test_multiple_or_operators_left_associative(self):
        """Test parsing multiple OR operators with left-associativity."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OR", "value": "||", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_node_a = {
            "type": "IDENTIFIER",
            "name": "a",
            "line": 1,
            "column": 1
        }
        mock_and_node_b = {
            "type": "IDENTIFIER",
            "name": "b",
            "line": 1,
            "column": 6
        }
        mock_and_node_c = {
            "type": "IDENTIFIER",
            "name": "c",
            "line": 1,
            "column": 11
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [mock_and_node_a, mock_and_node_b, mock_and_node_c]

            result = _parse_or(parser_state)

            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "||"
            assert result["line"] == 1
            assert result["column"] == 8
            assert result["right"] == mock_and_node_c
            assert result["left"]["type"] == "BINARY_OP"
            assert result["left"]["operator"] == "||"
            assert result["left"]["left"] == mock_and_node_a
            assert result["left"]["right"] == mock_and_node_b
            assert parser_state["pos"] == 5
            assert mock_parse_and.call_count == 3

    def test_empty_tokens_eof(self):
        """Test parsing with empty tokens list (EOF)."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_node = {
            "type": "EOF",
            "line": 0,
            "column": 0
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.return_value = mock_and_node

            result = _parse_or(parser_state)

            assert result == mock_and_node
            assert parser_state["pos"] == 0
            mock_parse_and.assert_called_once()

    def test_or_at_end_missing_right_operand(self):
        """Test OR operator at end - _parse_and handles EOF case."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_node_a = {
            "type": "IDENTIFIER",
            "name": "a",
            "line": 1,
            "column": 1
        }
        mock_and_node_eof = {
            "type": "EOF",
            "line": 0,
            "column": 0
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [mock_and_node_a, mock_and_node_eof]

            result = _parse_or(parser_state)

            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "||"
            assert result["left"] == mock_and_node_a
            assert result["right"] == mock_and_node_eof
            assert parser_state["pos"] == 2
            assert mock_parse_and.call_count == 2

    def test_preserves_position_state(self):
        """Test that parser state position is correctly updated."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
                {"type": "OR", "value": "||", "line": 2, "column": 7},
                {"type": "NUMBER", "value": "42", "line": 2, "column": 10},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 12}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_node_x = {
            "type": "IDENTIFIER",
            "name": "x",
            "line": 2,
            "column": 5
        }
        mock_and_node_42 = {
            "type": "NUMBER",
            "value": "42",
            "literal_type": "int",
            "line": 2,
            "column": 10
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [mock_and_node_x, mock_and_node_42]

            result = _parse_or(parser_state)

            assert result["type"] == "BINARY_OP"
            assert parser_state["pos"] == 3
            assert mock_parse_and.call_count == 2

    def test_or_operator_location_in_ast(self):
        """Test that OR operator token location is preserved in AST."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "left", "line": 5, "column": 10},
                {"type": "OR", "value": "||", "line": 5, "column": 15},
                {"type": "IDENTIFIER", "value": "right", "line": 5, "column": 18}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_node_left = {
            "type": "IDENTIFIER",
            "name": "left",
            "line": 5,
            "column": 10
        }
        mock_and_node_right = {
            "type": "IDENTIFIER",
            "name": "right",
            "line": 5,
            "column": 18
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [mock_and_node_left, mock_and_node_right]

            result = _parse_or(parser_state)

            assert result["line"] == 5
            assert result["column"] == 15
            assert result["operator"] == "||"
