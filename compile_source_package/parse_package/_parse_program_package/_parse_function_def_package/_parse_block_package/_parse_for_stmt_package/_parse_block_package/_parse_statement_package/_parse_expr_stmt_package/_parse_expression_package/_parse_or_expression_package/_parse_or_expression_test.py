import pytest
from unittest.mock import patch

from ._parse_or_expression_src import (
    _parse_or_expression,
    _current_token,
    _is_or_operator
)


class TestCurrentToken:
    """测试 _current_token 辅助函数"""
    
    def test_returns_token_when_pos_valid(self):
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
            ],
            "pos": 0
        }
        result = _current_token(parser_state)
        assert result == {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
    
    def test_returns_token_when_pos_middle(self):
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
            ],
            "pos": 1
        }
        result = _current_token(parser_state)
        assert result == {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
    
    def test_returns_eof_when_pos_at_end(self):
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1
        }
        result = _current_token(parser_state)
        assert result == {"type": "EOF", "value": "", "line": 0, "column": 0}
    
    def test_returns_eof_when_pos_beyond_end(self):
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5
        }
        result = _current_token(parser_state)
        assert result == {"type": "EOF", "value": "", "line": 0, "column": 0}
    
    def test_returns_eof_when_tokens_empty(self):
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        result = _current_token(parser_state)
        assert result == {"type": "EOF", "value": "", "line": 0, "column": 0}
    
    def test_handles_missing_pos(self):
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ]
        }
        result = _current_token(parser_state)
        assert result == {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
    
    def test_handles_missing_tokens(self):
        parser_state = {
            "pos": 0
        }
        result = _current_token(parser_state)
        assert result == {"type": "EOF", "value": "", "line": 0, "column": 0}


class TestIsOrOperator:
    """测试 _is_or_operator 辅助函数"""
    
    def test_returns_true_for_or_operator(self):
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 1},
            ],
            "pos": 0
        }
        assert _is_or_operator(parser_state) is True
    
    def test_returns_false_for_different_operator(self):
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 1},
            ],
            "pos": 0
        }
        assert _is_or_operator(parser_state) is False
    
    def test_returns_false_for_identifier(self):
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0
        }
        assert _is_or_operator(parser_state) is False
    
    def test_returns_false_for_eof(self):
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        assert _is_or_operator(parser_state) is False
    
    def test_returns_false_when_type_missing(self):
        parser_state = {
            "tokens": [
                {"value": "||", "line": 1, "column": 1},
            ],
            "pos": 0
        }
        assert _is_or_operator(parser_state) is False
    
    def test_returns_false_when_value_missing(self):
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "line": 1, "column": 1},
            ],
            "pos": 0
        }
        assert _is_or_operator(parser_state) is False


class TestParseOrExpression:
    """测试 _parse_or_expression 主函数"""
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_single_expression_no_or(self, mock_parse_and):
        """测试不含 || 的单个表达式"""
        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_parse_and.return_value = left_ast
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0
        }
        
        result = _parse_or_expression(parser_state)
        
        assert result == left_ast
        mock_parse_and.assert_called_once_with(parser_state)
        assert parser_state["pos"] == 0
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_single_or_operator(self, mock_parse_and):
        """测试含一个 || 运算符的表达式"""
        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
        mock_parse_and.side_effect = [left_ast, right_ast]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
            ],
            "pos": 0
        }
        
        result = _parse_or_expression(parser_state)
        
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "||"
        assert result["line"] == 1
        assert result["column"] == 3
        assert len(result["children"]) == 2
        assert result["children"][0] == left_ast
        assert result["children"][1] == right_ast
        assert parser_state["pos"] == 2
        assert mock_parse_and.call_count == 2
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_multiple_or_operators_left_associative(self, mock_parse_and):
        """测试多个 || 运算符，验证左结合性"""
        ast_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        ast_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ast_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        mock_parse_and.side_effect = [ast_a, ast_b, ast_c]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            ],
            "pos": 0
        }
        
        result = _parse_or_expression(parser_state)
        
        # 左结合：(a || b) || c
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "||"
        assert result["line"] == 1
        assert result["column"] == 7
        
        left_child = result["children"][0]
        assert left_child["type"] == "BINARY_OP"
        assert left_child["value"] == "||"
        assert left_child["line"] == 1
        assert left_child["column"] == 3
        assert left_child["children"][0] == ast_a
        assert left_child["children"][1] == ast_b
        
        assert result["children"][1] == ast_c
        assert parser_state["pos"] == 4
        assert mock_parse_and.call_count == 3
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_or_with_complex_left_operand(self, mock_parse_and):
        """测试 || 左侧为复杂表达式（由 _parse_and_expression 返回）"""
        complex_left = {
            "type": "BINARY_OP",
            "value": "&&",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "line": 1,
            "column": 3
        }
        right_ast = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10}
        mock_parse_and.side_effect = [complex_left, right_ast]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10},
            ],
            "pos": 3
        }
        
        result = _parse_or_expression(parser_state)
        
        assert result["type"] == "BINARY_OP"
        assert result["value"] == "||"
        assert result["children"][0] == complex_left
        assert result["children"][1] == right_ast
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_preserves_line_column_from_operator_token(self, mock_parse_and):
        """验证 AST 节点的 line/column 来自运算符 token"""
        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 1}
        mock_parse_and.side_effect = [left_ast, right_ast]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 5, "column": 10},
                {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 1},
            ],
            "pos": 0
        }
        
        result = _parse_or_expression(parser_state)
        
        assert result["line"] == 5
        assert result["column"] == 10
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_handles_missing_line_column_in_token(self, mock_parse_and):
        """验证当 token 缺少 line/column 时使用默认值 0"""
        left_ast = {"type": "IDENTIFIER", "value": "x"}
        right_ast = {"type": "IDENTIFIER", "value": "y"}
        mock_parse_and.side_effect = [left_ast, right_ast]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "OPERATOR", "value": "||"},
                {"type": "IDENTIFIER", "value": "y"},
            ],
            "pos": 0
        }
        
        result = _parse_or_expression(parser_state)
        
        assert result["line"] == 0
        assert result["column"] == 0
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_empty_tokens(self, mock_parse_and):
        """测试空 token 列表"""
        mock_parse_and.return_value = {"type": "EOF", "value": ""}
        
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        result = _parse_or_expression(parser_state)
        
        assert result == {"type": "EOF", "value": ""}
        mock_parse_and.assert_called_once()
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_pos_at_end(self, mock_parse_and):
        """测试 pos 已在末尾"""
        mock_parse_and.return_value = {"type": "EOF", "value": ""}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1
        }
        
        result = _parse_or_expression(parser_state)
        
        assert result == {"type": "EOF", "value": ""}
        assert parser_state["pos"] == 1
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_parse_and_expression_raises_error(self, mock_parse_and):
        """测试 _parse_and_expression 抛出异常时的传播"""
        mock_parse_and.side_effect = SyntaxError("Invalid expression")
        
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "@", "line": 1, "column": 1},
            ],
            "pos": 0
        }
        
        with pytest.raises(SyntaxError, match="Invalid expression"):
            _parse_or_expression(parser_state)
    
    @patch('._parse_or_expression_src._parse_and_expression')
    def test_state_modified_in_place(self, mock_parse_and):
        """验证 parser_state 被原地修改"""
        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
        mock_parse_and.side_effect = [left_ast, right_ast]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.ccp"
        }
        
        original_id = id(parser_state)
        result = _parse_or_expression(parser_state)
        
        assert id(parser_state) == original_id
        assert parser_state["filename"] == "test.ccp"
        assert parser_state["pos"] == 2
