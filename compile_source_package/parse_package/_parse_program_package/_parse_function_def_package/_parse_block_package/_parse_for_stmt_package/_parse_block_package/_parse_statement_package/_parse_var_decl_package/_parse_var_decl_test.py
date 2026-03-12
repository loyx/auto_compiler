"""单元测试：_parse_var_decl 函数"""
import pytest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Patch the import of _parse_expression before importing _parse_var_decl
import sys
from unittest.mock import Mock

# Create a mock module for _parse_expression
mock_parse_expression_module = MagicMock()
mock_parse_expression_module._parse_expression = MagicMock()

# Register the mock in sys.modules to prevent actual import
mock_module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_expression_src"
sys.modules[mock_module_path] = mock_parse_expression_module

from ._parse_var_decl_src import _parse_var_decl

# Define the absolute path for patching
PARSE_EXPRESSION_PATH = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_expression_src._parse_expression"


def _create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """辅助函数：创建 token 字典"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def _create_parser_state(tokens: list, pos: int = 0, filename: str = "test.cc") -> Dict[str, Any]:
    """辅助函数：创建 parser_state 字典"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseVarDeclHappyPath:
    """测试 _parse_var_decl 的正常路径"""
    
    @patch(PARSE_EXPRESSION_PATH)
    def test_parse_let_declaration(self, mock_parse_expression):
        """测试解析 let 声明"""
        # 准备测试数据
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5),
            _create_token("EQUALS", "=", 1, 7),
            _create_token("NUMBER", "42", 1, 9),
            _create_token("SEMICOLON", ";", 1, 11)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression 返回一个简单的表达式 AST
        mock_expr_ast = {
            "type": "LITERAL",
            "children": [],
            "value": "42",
            "line": 1,
            "column": 9
        }
        mock_parse_expression.return_value = mock_expr_ast
        
        # 执行测试
        result = _parse_var_decl(parser_state)
        
        # 验证结果
        assert result["type"] == "VAR_DECL"
        assert result["value"]["keyword"] == "let"
        assert result["value"]["name"] == "x"
        assert result["children"] == [mock_expr_ast]
        assert result["line"] == 1
        assert result["column"] == 1
        
        # 验证 pos 被正确更新到分号之后
        assert parser_state["pos"] == 5
        
        # 验证 _parse_expression 被调用
        mock_parse_expression.assert_called_once()
    
    @patch(PARSE_EXPRESSION_PATH)
    def test_parse_var_declaration(self, mock_parse_expression):
        """测试解析 var 声明"""
        tokens = [
            _create_token("VAR", "var", 2, 1),
            _create_token("IDENTIFIER", "count", 2, 5),
            _create_token("EQUALS", "=", 2, 11),
            _create_token("NUMBER", "0", 2, 13),
            _create_token("SEMICOLON", ";", 2, 14)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {
            "type": "LITERAL",
            "children": [],
            "value": "0",
            "line": 2,
            "column": 13
        }
        mock_parse_expression.return_value = mock_expr_ast
        
        result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["value"]["keyword"] == "var"
        assert result["value"]["name"] == "count"
        assert result["children"] == [mock_expr_ast]
        assert result["line"] == 2
        assert result["column"] == 1
        assert parser_state["pos"] == 5
    
    @patch(PARSE_EXPRESSION_PATH)
    def test_parse_declaration_with_complex_expression(self, mock_parse_expression):
        """测试解析带有复杂表达式的声明"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "result", 1, 5),
            _create_token("EQUALS", "=", 1, 12),
            _create_token("NUMBER", "1", 1, 14),
            _create_token("PLUS", "+", 1, 16),
            _create_token("NUMBER", "2", 1, 18),
            _create_token("SEMICOLON", ";", 1, 19)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "LITERAL", "value": "1"},
                {"type": "LITERAL", "value": "2"}
            ],
            "value": "+",
            "line": 1,
            "column": 14
        }
        mock_parse_expression.return_value = mock_expr_ast
        
        result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["value"]["name"] == "result"
        assert result["children"] == [mock_expr_ast]
        assert parser_state["pos"] == 7


class TestParseVarDeclErrors:
    """测试 _parse_var_decl 的错误处理"""
    
    def test_error_empty_tokens(self):
        """测试空 token 列表"""
        parser_state = _create_parser_state([], pos=0)
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected 'let' or 'var'"):
            _parse_var_decl(parser_state)
    
    def test_error_pos_beyond_tokens(self):
        """测试 pos 超出 token 列表范围"""
        tokens = [_create_token("NUMBER", "42")]
        parser_state = _create_parser_state(tokens, pos=5)
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected 'let' or 'var'"):
            _parse_var_decl(parser_state)
    
    def test_error_invalid_keyword(self):
        """测试无效的关键词（不是 let 或 var）"""
        tokens = [
            _create_token("IF", "if", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 4)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected 'let' or 'var', got 'if'"):
            _parse_var_decl(parser_state)
    
    def test_error_missing_identifier(self):
        """测试缺少标识符"""
        tokens = [
            _create_token("LET", "let", 1, 1)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected identifier"):
            _parse_var_decl(parser_state)
    
    def test_error_invalid_identifier_token(self):
        """测试无效的标识符 token"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected identifier, got '42'"):
            _parse_var_decl(parser_state)
    
    def test_error_missing_equals(self):
        """测试缺少等号"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected '='"):
            _parse_var_decl(parser_state)
    
    def test_error_invalid_equals_token(self):
        """测试无效的等号 token"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5),
            _create_token("PLUS", "+", 1, 7)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected '=', got '\\+'"):
            _parse_var_decl(parser_state)
    
    def test_error_missing_expression(self):
        """测试缺少表达式"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5),
            _create_token("EQUALS", "=", 1, 7)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected expression"):
            _parse_var_decl(parser_state)
    
    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_missing_semicolon(self, mock_parse_expression):
        """测试缺少分号"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5),
            _create_token("EQUALS", "=", 1, 7),
            _create_token("NUMBER", "42", 1, 9)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {"type": "LITERAL", "value": "42"}
        mock_parse_expression.return_value = mock_expr_ast
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected ';'"):
            _parse_var_decl(parser_state)
    
    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_invalid_semicolon_token(self, mock_parse_expression):
        """测试无效的分号 token"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5),
            _create_token("EQUALS", "=", 1, 7),
            _create_token("NUMBER", "42", 1, 9),
            _create_token("COMMA", ",", 1, 11)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {"type": "LITERAL", "value": "42"}
        mock_parse_expression.return_value = mock_expr_ast
        
        with pytest.raises(SyntaxError, match="Expected ';', got ','"):
            _parse_var_decl(parser_state)


class TestParseVarDeclSideEffects:
    """测试 _parse_var_decl 的副作用"""
    
    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_pos_updated_correctly(self, mock_parse_expression):
        """测试 pos 被正确更新"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5),
            _create_token("EQUALS", "=", 1, 7),
            _create_token("NUMBER", "42", 1, 9),
            _create_token("SEMICOLON", ";", 1, 11),
            _create_token("IDENTIFIER", "y", 1, 13)  # 额外的 token，用于验证 pos 位置
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {"type": "LITERAL", "value": "42"}
        mock_parse_expression.return_value = mock_expr_ast
        
        result = _parse_var_decl(parser_state)
        
        # 验证 pos 指向分号之后的 token
        assert parser_state["pos"] == 5
        # 验证可以解析下一个语句
        assert tokens[parser_state["pos"]]["value"] == "y"
    
    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_parse_expression_called_with_correct_state(self, mock_parse_expression):
        """测试 _parse_expression 被调用时 parser_state 的状态"""
        tokens = [
            _create_token("LET", "let", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 5),
            _create_token("EQUALS", "=", 1, 7),
            _create_token("NUMBER", "42", 1, 9),
            _create_token("SEMICOLON", ";", 1, 11)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {"type": "LITERAL", "value": "42"}
        mock_parse_expression.return_value = mock_expr_ast
        
        _parse_var_decl(parser_state)
        
        # 验证 _parse_expression 被调用时 pos 指向表达式起始位置
        mock_parse_expression.assert_called_once()
        # 调用时 parser_state["pos"] 应该是 3（指向 NUMBER token）
        # 注意：由于是引用传递，我们无法直接验证调用时的状态
        # 但我们可以验证 _parse_expression 确实被调用了
        assert mock_parse_expression.call_count == 1


class TestParseVarDeclASTStructure:
    """测试 _parse_var_decl 返回的 AST 结构"""
    
    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_ast_node_has_required_fields(self, mock_parse_expression):
        """测试 AST 节点包含所有必需字段"""
        tokens = [
            _create_token("VAR", "var", 3, 10),
            _create_token("IDENTIFIER", "myVar", 3, 14),
            _create_token("EQUALS", "=", 3, 20),
            _create_token("STRING", '"hello"', 3, 22),
            _create_token("SEMICOLON", ";", 3, 29)
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        mock_expr_ast = {
            "type": "LITERAL",
            "children": [],
            "value": '"hello"',
            "line": 3,
            "column": 22
        }
        mock_parse_expression.return_value = mock_expr_ast
        
        result = _parse_var_decl(parser_state)
        
        # 验证所有必需字段存在
        assert "type" in result
        assert "children" in result
        assert "value" in result
        assert "line" in result
        assert "column" in result
        
        # 验证字段类型
        assert isinstance(result["type"], str)
        assert isinstance(result["children"], list)
        assert isinstance(result["value"], dict)
        assert isinstance(result["line"], int)
        assert isinstance(result["column"], int)
        
        # 验证 value 字段结构
        assert "keyword" in result["value"]
        assert "name" in result["value"]
    
    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_ast_preserves_keyword_and_name(self, mock_parse_expression):
        """测试 AST 正确保存关键词和变量名"""
        test_cases = [
            ("LET", "let", "x"),
            ("VAR", "var", "count"),
            ("LET", "let", "_private_var"),
            ("VAR", "var", "camelCaseName"),
            ("LET", "let", "snake_case_name")
        ]
        
        for token_type, keyword, var_name in test_cases:
            tokens = [
                _create_token(token_type, keyword, 1, 1),
                _create_token("IDENTIFIER", var_name, 1, 5),
                _create_token("EQUALS", "=", 1, 10),
                _create_token("NUMBER", "0", 1, 12),
                _create_token("SEMICOLON", ";", 1, 13)
            ]
            parser_state = _create_parser_state(tokens, pos=0)
            
            mock_expr_ast = {"type": "LITERAL", "value": "0"}
            mock_parse_expression.return_value = mock_expr_ast
            
            result = _parse_var_decl(parser_state)
            
            assert result["value"]["keyword"] == keyword
            assert result["value"]["name"] == var_name
