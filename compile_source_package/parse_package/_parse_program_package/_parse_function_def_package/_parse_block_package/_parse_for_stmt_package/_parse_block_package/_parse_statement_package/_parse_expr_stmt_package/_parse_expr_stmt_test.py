import pytest
from unittest.mock import patch

from ._parse_expr_stmt_src import _parse_expr_stmt


class TestParseExprStmt:
    """测试 _parse_expr_stmt 函数"""

    def test_happy_path_simple_identifier(self):
        """测试简单标识符表达式语句"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        mock_expr_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast

            result = _parse_expr_stmt(parser_state)

            assert result["type"] == "EXPR_STMT"
            assert len(result["children"]) == 1
            assert result["children"][0] == mock_expr_ast
            assert result["line"] == 1
            assert result["column"] == 0
            assert parser_state["pos"] == 2

    def test_happy_path_function_call(self):
        """测试函数调用表达式语句"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "func", "line": 2, "column": 4},
                {"type": "LPAREN", "value": "(", "line": 2, "column": 8},
                {"type": "NUMBER", "value": "42", "line": 2, "column": 9},
                {"type": "RPAREN", "value": ")", "line": 2, "column": 11},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 12}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        mock_expr_ast = {
            "type": "CALL",
            "children": [
                {"type": "IDENTIFIER", "value": "func", "line": 2, "column": 4},
                {"type": "LITERAL", "value": 42, "line": 2, "column": 9}
            ],
            "line": 2,
            "column": 4
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 4}) or mock_expr_ast

            result = _parse_expr_stmt(parser_state)

            assert result["type"] == "EXPR_STMT"
            assert result["children"][0]["type"] == "CALL"
            assert result["line"] == 2
            assert result["column"] == 4
            assert parser_state["pos"] == 5

    def test_happy_path_binary_expression(self):
        """测试二元表达式语句"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        mock_expr_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "LITERAL", "value": 1, "line": 1, "column": 0},
                {"type": "LITERAL", "value": 2, "line": 1, "column": 4}
            ],
            "value": "+",
            "line": 1,
            "column": 0
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 3}) or mock_expr_ast

            result = _parse_expr_stmt(parser_state)

            assert result["type"] == "EXPR_STMT"
            assert result["children"][0]["type"] == "BINARY_OP"
            assert result["children"][0]["value"] == "+"
            assert parser_state["pos"] == 4

    def test_boundary_empty_tokens(self):
        """测试 tokens 为空的边界情况"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_expr_stmt(parser_state)

        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.txt:0:0" in str(exc_info.value)

    def test_boundary_pos_at_end(self):
        """测试 pos 已到达 tokens 末尾的边界情况"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}
            ],
            "pos": 1,
            "filename": "test.txt"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_expr_stmt(parser_state)

        assert "Unexpected end of input" in str(exc_info.value)

    def test_error_missing_semicolon(self):
        """测试缺少分号的错误情况"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
                {"type": "NEWLINE", "value": "\n", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        mock_expr_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast

            with pytest.raises(SyntaxError) as exc_info:
                _parse_expr_stmt(parser_state)

            assert "Expected ';'" in str(exc_info.value)
            assert "test.txt:1:0" in str(exc_info.value)

    def test_error_invalid_token_after_expression(self):
        """测试表达式后跟无效 token（不是分号）的错误情况"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
                {"type": "COMMA", "value": ",", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        mock_expr_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast

            with pytest.raises(SyntaxError) as exc_info:
                _parse_expr_stmt(parser_state)

            assert "Expected ';'" in str(exc_info.value)
            assert "COMMA" in str(exc_info.value)

    def test_error_parse_expression_exception_propagation(self):
        """测试 _parse_expression 抛出异常时的传播"""
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "?", "line": 1, "column": 0},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = SyntaxError("test.txt:1:0: Invalid expression")

            with pytest.raises(SyntaxError) as exc_info:
                _parse_expr_stmt(parser_state)

            assert "Invalid expression" in str(exc_info.value)

    def test_error_no_filename_in_parser_state(self):
        """测试 parser_state 中没有 filename 字段的情况"""
        parser_state = {
            "tokens": [],
            "pos": 0
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_expr_stmt(parser_state)

        assert "unknown:0:0" in str(exc_info.value)

    def test_side_effect_pos_updated_correctly(self):
        """测试 parser_state pos 被正确更新"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "100", "line": 5, "column": 10},
                {"type": "SEMICOLON", "value": ";", "line": 5, "column": 13}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        mock_expr_ast = {"type": "LITERAL", "value": 100, "line": 5, "column": 10}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast

            _parse_expr_stmt(parser_state)

            assert parser_state["pos"] == 2

    def test_ast_node_structure(self):
        """测试返回的 AST 节点结构完整性"""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 3, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 3, "column": 10}
            ],
            "pos": 0,
            "filename": "test.txt"
        }

        mock_expr_ast = {"type": "LITERAL", "value": "hello", "line": 3, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 1}) or mock_expr_ast

            result = _parse_expr_stmt(parser_state)

            assert "type" in result
            assert "children" in result
            assert "line" in result
            assert "column" in result
            assert result["type"] == "EXPR_STMT"
            assert isinstance(result["children"], list)
            assert len(result["children"]) == 1
