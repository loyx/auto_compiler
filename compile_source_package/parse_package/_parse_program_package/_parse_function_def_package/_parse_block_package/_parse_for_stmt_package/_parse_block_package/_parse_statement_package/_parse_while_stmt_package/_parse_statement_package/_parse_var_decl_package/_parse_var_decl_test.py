# === std / third-party imports ===
import pytest
from unittest.mock import patch
from typing import Dict, Any

# === UUT import ===
from ._parse_var_decl_src import _parse_var_decl

# === Test Helpers ===
def create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }

def create_parser_state(tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }

# === Test Cases ===

class TestParseVarDeclHappyPath:
    """Test happy path scenarios for _parse_var_decl."""
    
    def test_parse_simple_var_decl(self):
        """Test parsing: var x;"""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5),
            create_token("SEMICOLON", ";", 1, 6)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["line"] == 1
        assert result["column"] == 1
        assert len(result["children"]) == 3
        assert result["children"][0]["type"] == "IDENTIFIER"
        assert result["children"][1] is None  # No type
        assert result["children"][2] is None  # No initializer
        assert parser_state["pos"] == 3  # Consumed all tokens
    
    def test_parse_var_decl_with_type(self):
        """Test parsing: var x: int;"""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("IDENTIFIER", "int", 1, 8),
            create_token("SEMICOLON", ";", 1, 11)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["children"][0]["value"] == "x"
        assert result["children"][1]["type"] == "IDENTIFIER"
        assert result["children"][1]["value"] == "int"
        assert result["children"][2] is None  # No initializer
        assert parser_state["pos"] == 5
    
    def test_parse_var_decl_with_initializer(self):
        """Test parsing: var x = 5;"""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5),
            create_token("EQUALS", "=", 1, 7),
            create_token("NUMBER", "5", 1, 9),
            create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        def mock_expression_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "NUMBER",
                "children": [],
                "value": 5,
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            with patch('._parse_expression_package._parse_expression_src._parse_expression', side_effect=mock_expression_side_effect):
                result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["children"][0]["value"] == "x"
        assert result["children"][1] is None  # No type
        assert result["children"][2]["type"] == "NUMBER"
        assert result["children"][2]["value"] == 5
        assert parser_state["pos"] == 5
    
    def test_parse_var_decl_with_type_and_initializer(self):
        """Test parsing: var x: int = 5;"""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("IDENTIFIER", "int", 1, 8),
            create_token("EQUALS", "=", 1, 12),
            create_token("NUMBER", "5", 1, 14),
            create_token("SEMICOLON", ";", 1, 15)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        def mock_expression_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "NUMBER",
                "children": [],
                "value": 5,
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            with patch('._parse_expression_package._parse_expression_src._parse_expression', side_effect=mock_expression_side_effect):
                result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["children"][0]["value"] == "x"
        assert result["children"][1]["value"] == "int"
        assert result["children"][2]["value"] == 5
        assert parser_state["pos"] == 7


class TestParseVarDeclErrors:
    """Test error scenarios for _parse_var_decl."""
    
    def test_error_missing_var_keyword(self):
        """Test error when first token is not VAR."""
        tokens = [
            create_token("IDENTIFIER", "x", 1, 1),
            create_token("SEMICOLON", ";", 1, 2)
        ]
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_var_decl(parser_state)
        
        assert "expected 'var' keyword" in str(exc_info.value)
        assert "test.cc:1:1" in str(exc_info.value)
    
    def test_error_missing_identifier_after_var(self):
        """Test error when no identifier after VAR."""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("SEMICOLON", ";", 1, 5)
        ]
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_var_decl(parser_state)
        
        assert "expected identifier after 'var'" in str(exc_info.value)
        assert "test.cc:1:5" in str(exc_info.value)
    
    def test_error_end_of_tokens_after_var(self):
        """Test error when tokens end after VAR."""
        tokens = [
            create_token("VAR", "var", 1, 1)
        ]
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_var_decl(parser_state)
        
        assert "expected identifier after 'var'" in str(exc_info.value)
    
    def test_error_missing_type_after_colon(self):
        """Test error when no type identifier after COLON."""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("SEMICOLON", ";", 1, 7)
        ]
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            with pytest.raises(SyntaxError) as exc_info:
                _parse_var_decl(parser_state)
        
        assert "expected type identifier after ':'" in str(exc_info.value)
        assert "test.cc:1:7" in str(exc_info.value)
    
    def test_error_end_of_tokens_after_colon(self):
        """Test error when tokens end after COLON."""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5),
            create_token("COLON", ":", 1, 6)
        ]
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            with pytest.raises(SyntaxError) as exc_info:
                _parse_var_decl(parser_state)
        
        assert "expected type identifier after ':'" in str(exc_info.value)
    
    def test_error_missing_semicolon(self):
        """Test error when no SEMICOLON at end."""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5)
        ]
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            with pytest.raises(SyntaxError) as exc_info:
                _parse_var_decl(parser_state)
        
        assert "expected ';' at end of variable declaration" in str(exc_info.value)
        assert "test.cc:1:5" in str(exc_info.value)
    
    def test_error_end_of_tokens_before_semicolon(self):
        """Test error when tokens end before SEMICOLON."""
        tokens = [
            create_token("VAR", "var", 1, 1),
            create_token("IDENTIFIER", "x", 1, 5),
            create_token("EQUALS", "=", 1, 7),
            create_token("NUMBER", "5", 1, 9)
        ]
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        def mock_expression_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "NUMBER",
                "children": [],
                "value": 5,
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            with patch('._parse_expression_package._parse_expression_src._parse_expression', side_effect=mock_expression_side_effect):
                with pytest.raises(SyntaxError) as exc_info:
                    _parse_var_decl(parser_state)
        
        assert "expected ';' at end of variable declaration" in str(exc_info.value)
    
    def test_error_empty_tokens(self):
        """Test error when tokens list is empty."""
        tokens = []
        parser_state = create_parser_state(tokens, 0, "test.cc")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_var_decl(parser_state)
        
        assert "expected 'var' keyword" in str(exc_info.value)
        assert "test.cc:0:0" in str(exc_info.value)


class TestParseVarDeclEdgeCases:
    """Test edge cases for _parse_var_decl."""
    
    def test_var_decl_at_different_position(self):
        """Test parsing var decl when pos is not at start."""
        tokens = [
            create_token("NUMBER", "1", 1, 1),
            create_token("VAR", "var", 1, 3),
            create_token("IDENTIFIER", "x", 1, 7),
            create_token("SEMICOLON", ";", 1, 8)
        ]
        parser_state = create_parser_state(tokens, 1)  # Start at VAR token
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            result = _parse_var_decl(parser_state)
        
        assert result["type"] == "VAR_DECL"
        assert result["line"] == 1
        assert result["column"] == 3
        assert parser_state["pos"] == 4
    
    def test_var_decl_with_custom_filename(self):
        """Test that error messages include custom filename."""
        tokens = [
            create_token("VAR", "var", 1, 1)
        ]
        parser_state = create_parser_state(tokens, 0, "my_custom_file.cc")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_var_decl(parser_state)
        
        assert "my_custom_file.cc" in str(exc_info.value)
    
    def test_var_decl_preserves_token_positions(self):
        """Test that AST node preserves original token line/column."""
        tokens = [
            create_token("VAR", "var", 10, 25),
            create_token("IDENTIFIER", "x", 10, 29),
            create_token("SEMICOLON", ";", 10, 30)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        def mock_identifier_side_effect(state):
            pos = state["pos"]
            token = tokens[pos]
            state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "children": [],
                "value": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
        
        with patch('._parse_identifier_package._parse_identifier_src._parse_identifier', side_effect=mock_identifier_side_effect):
            result = _parse_var_decl(parser_state)
        
        assert result["line"] == 10
        assert result["column"] == 25
