import pytest
from unittest.mock import patch

# Relative import from the same package
from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr:
    """Tests for _parse_unary_expr function"""

    def test_single_negative_operator(self):
        """Test parsing a single negative unary operator"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "-"
        assert result["operand"] == mock_primary_result
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_single_positive_operator(self):
        """Test parsing a single positive unary operator"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 2, "column": 5},
                {"type": "NUMBER", "value": "42", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "42", "line": 2, "column": 6}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "+"
        assert result["operand"] == mock_primary_result
        assert result["line"] == 2
        assert result["column"] == 5

    def test_consecutive_unary_operators(self):
        """Test parsing consecutive unary operators like --x"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        # Outer unary op
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "-"
        assert result["line"] == 1
        assert result["column"] == 1
        
        # Inner unary op
        inner = result["operand"]
        assert inner["type"] == "UNARY_OP"
        assert inner["operator"] == "-"
        assert inner["line"] == 1
        assert inner["column"] == 2
        assert inner["operand"] == mock_primary_result

    def test_mixed_unary_operators(self):
        """Test parsing mixed unary operators like -+x"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "-"
        assert result["operand"]["type"] == "UNARY_OP"
        assert result["operand"]["operator"] == "+"
        assert result["operand"]["operand"] == mock_primary_result

    def test_no_unary_operator_delegates_to_primary(self):
        """Test that non-unary tokens delegate to _parse_primary_expr"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        assert result == mock_primary_result
        assert parser_state["pos"] == 0  # Position should not change

    def test_other_operator_type_delegates_to_primary(self):
        """Test that non-OPERATOR type tokens delegate to _parse_primary_expr"""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "not", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "KEYWORD", "value": "not", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        assert result == mock_primary_result

    def test_other_operator_value_delegates_to_primary(self):
        """Test that OPERATOR tokens with values other than - or + delegate to _parse_primary_expr"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "*", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        assert result == mock_primary_result

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with pytest.raises(SyntaxError, match="Unexpected end of input while parsing unary expression"):
            _parse_unary_expr(parser_state)

    def test_position_beyond_tokens_raises_syntax_error(self):
        """Test that position beyond tokens list raises SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        with pytest.raises(SyntaxError, match="Unexpected end of input while parsing unary expression"):
            _parse_unary_expr(parser_state)

    def test_unary_operator_at_end_raises_syntax_error(self):
        """Test that unary operator at end of tokens raises SyntaxError from recursive call"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with pytest.raises(SyntaxError, match="Unexpected end of input while parsing unary expression"):
            _parse_unary_expr(parser_state)

    def test_token_missing_type_field_delegates_to_primary(self):
        """Test that tokens without type field delegate to _parse_primary_expr"""
        parser_state = {
            "tokens": [
                {"value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        assert result == mock_primary_result

    def test_token_missing_value_field_delegates_to_primary(self):
        """Test that OPERATOR tokens without value field delegate to _parse_primary_expr"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "0", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        assert result == mock_primary_result

    def test_position_advances_correctly_for_unary(self):
        """Test that position advances correctly after consuming unary operator"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            _parse_unary_expr(parser_state)
        
        assert parser_state["pos"] == 1

    def test_position_unchanged_when_delegating(self):
        """Test that position remains unchanged when delegating to primary expr"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            _parse_unary_expr(parser_state)
        
        assert parser_state["pos"] == 0

    def test_line_column_preserved_in_ast_node(self):
        """Test that line and column from operator token are preserved in AST node"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 10, "column": 25},
                {"type": "NUMBER", "value": "100", "line": 10, "column": 26}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "100", "line": 10, "column": 26}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        assert result["line"] == 10
        assert result["column"] == 25

    def test_default_line_column_when_missing(self):
        """Test that default line/column 0 is used when missing from token"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "-"},
                {"type": "NUMBER", "value": "5"}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_primary_result = {"type": "NUMBER", "value": "5"}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = mock_primary_result
            result = _parse_unary_expr(parser_state)
        
        assert result["line"] == 0
        assert result["column"] == 0