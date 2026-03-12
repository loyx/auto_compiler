import pytest
from unittest.mock import patch

# Relative import from the same package structure
import sys
sys.path.insert(0, '/Users/loyx/projects/autoapp_workspace/workspace/projects/cc/files')
from main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_var_decl_package._parse_var_decl_src import _parse_var_decl


class TestParseVarDecl:
    """Test suite for _parse_var_decl function"""

    def test_simple_var_decl_int(self):
        """Test simple variable declaration with int type"""
        tokens = [
            {"type": "INT", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["value"]["var_type"] == "int"
        assert result["value"]["var_name"] == "x"
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 3

    def test_var_decl_with_initialization(self):
        """Test variable declaration with initialization expression"""
        tokens = [
            {"type": "INT", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 9},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        mock_expr_node = {"type": "LITERAL", "value": 5, "line": 1, "column": 9}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_var_decl_package._parse_var_decl_src._get_parse_expression") as mock_get_parse_expr:
            mock_get_parse_expr.return_value = lambda ps: mock_expr_node
            mock_parse_expr.return_value = mock_expr_node
            result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["value"]["var_type"] == "int"
        assert result["value"]["var_name"] == "x"
        assert len(result["children"]) == 1
        assert result["children"][0] == mock_expr_node
        assert parser_state["pos"] == 5
        mock_parse_expr.assert_called_once()

    def test_var_decl_float_type(self):
        """Test variable declaration with float type"""
        tokens = [
            {"type": "FLOAT", "value": "float", "line": 2, "column": 1},
            {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 7},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 8},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["value"]["var_type"] == "float"
        assert result["value"]["var_name"] == "y"

    def test_var_decl_bool_type(self):
        """Test variable declaration with bool type"""
        tokens = [
            {"type": "BOOL", "value": "bool", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 6},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        result = _parse_var_decl(parser_state)
        
        assert result["value"]["var_type"] == "bool"
        assert result["value"]["var_name"] == "flag"

    def test_var_decl_string_type(self):
        """Test variable declaration with string type"""
        tokens = [
            {"type": "STRING", "value": "string", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "name", "line": 1, "column": 8},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 12},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        result = _parse_var_decl(parser_state)
        
        assert result["value"]["var_type"] == "string"
        assert result["value"]["var_name"] == "name"

    def test_var_decl_custom_type(self):
        """Test variable declaration with custom type (IDENTIFIER as type)"""
        tokens = [
            {"type": "IDENTIFIER", "value": "MyType", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "obj", "line": 1, "column": 8},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        result = _parse_var_decl(parser_state)
        
        assert result["value"]["var_type"] == "MyType"
        assert result["value"]["var_name"] == "obj"

    def test_var_decl_no_semicolon(self):
        """Test variable declaration without semicolon (should still work)"""
        tokens = [
            {"type": "INT", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["value"]["var_type"] == "int"
        assert result["value"]["var_name"] == "x"
        assert parser_state["pos"] == 2

    def test_var_decl_with_init_no_semicolon(self):
        """Test variable declaration with initialization but no semicolon"""
        tokens = [
            {"type": "INT", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        mock_expr_node = {"type": "LITERAL", "value": 10, "line": 1, "column": 9}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_var_decl_package._parse_var_decl_src._get_parse_expression") as mock_get_parse_expr:
            mock_get_parse_expr.return_value = lambda ps: mock_expr_node
            mock_parse_expr.return_value = mock_expr_node
            result = _parse_var_decl(parser_state)
        
        assert result["value"]["var_type"] == "int"
        assert len(result["children"]) == 1
        assert parser_state["pos"] == 4

    def test_error_end_of_input_no_type(self):
        """Test error when input ends before type identifier"""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected type identifier"):
            _parse_var_decl(parser_state)

    def test_error_invalid_type_token(self):
        """Test error when type token is not a valid type"""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with pytest.raises(SyntaxError, match="Expected type identifier, got NUMBER"):
            _parse_var_decl(parser_state)

    def test_error_end_of_input_no_var_name(self):
        """Test error when input ends before variable name"""
        tokens = [
            {"type": "INT", "value": "int", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with pytest.raises(SyntaxError, match="Unexpected end of input, expected variable name"):
            _parse_var_decl(parser_state)

    def test_error_invalid_var_name(self):
        """Test error when variable name is not an identifier"""
        tokens = [
            {"type": "INT", "value": "int", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with pytest.raises(SyntaxError, match="Expected variable name, got NUMBER"):
            _parse_var_decl(parser_state)

    def test_position_updated_correctly_with_init(self):
        """Test that parser position is updated correctly with initialization"""
        tokens = [
            {"type": "FLOAT", "value": "float", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 9},
            {"type": "NUMBER", "value": "3.14", "line": 1, "column": 11},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 15},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        mock_expr_node = {"type": "LITERAL", "value": 3.14, "line": 1, "column": 11}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_var_decl_package._parse_var_decl_src._get_parse_expression") as mock_get_parse_expr:
            mock_get_parse_expr.return_value = lambda ps: mock_expr_node
            mock_parse_expr.return_value = mock_expr_node
            _parse_var_decl(parser_state)
        
        assert parser_state["pos"] == 5

    def test_position_updated_correctly_no_init(self):
        """Test that parser position is updated correctly without initialization"""
        tokens = [
            {"type": "BOOL", "value": "bool", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 6},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        _parse_var_decl(parser_state)
        
        assert parser_state["pos"] == 3

    def test_error_invalid_type_string_token(self):
        """Test error with another invalid type token (STRING token type)"""
        tokens = [
            {"type": "STRING", "value": "hello", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        # STRING token type with value "hello" is invalid as a type identifier
        # Only STRING as a type keyword is valid
        with pytest.raises(SyntaxError, match="Expected type identifier, got STRING"):
            _parse_var_decl(parser_state)
