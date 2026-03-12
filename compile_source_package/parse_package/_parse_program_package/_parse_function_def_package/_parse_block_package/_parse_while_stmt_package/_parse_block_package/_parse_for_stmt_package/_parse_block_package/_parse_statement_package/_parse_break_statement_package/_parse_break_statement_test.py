# === test file for _parse_break_statement ===
import pytest
from typing import Any, Dict

from ._parse_break_statement_src import _parse_break_statement


def _create_parser_state(tokens: list, pos: int = 0, filename: str = "test.cc") -> Dict[str, Any]:
    """Helper to create parser state."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def _create_token(token_type: str, value: str, line: int, column: int) -> Dict[str, Any]:
    """Helper to create a token."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestParseBreakStatementHappyPath:
    """Test happy path scenarios for _parse_break_statement."""
    
    def test_parse_break_statement_simple(self):
        """Test parsing a simple break statement."""
        tokens = [
            _create_token("BREAK", "break", 1, 1),
            _create_token("SEMICOLON", ";", 1, 6),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        result = _parse_break_statement(parser_state)
        
        assert result["type"] == "BREAK_STMT"
        assert result["line"] == 1
        assert result["column"] == 1
        assert result["children"] == []
        assert parser_state["pos"] == 2
    
    def test_parse_break_statement_with_surrounding_tokens(self):
        """Test parsing break statement with tokens before and after."""
        tokens = [
            _create_token("IF", "if", 1, 1),
            _create_token("BREAK", "break", 2, 5),
            _create_token("SEMICOLON", ";", 2, 10),
            _create_token("RETURN", "return", 3, 1),
        ]
        parser_state = _create_parser_state(tokens, pos=1)
        
        result = _parse_break_statement(parser_state)
        
        assert result["type"] == "BREAK_STMT"
        assert result["line"] == 2
        assert result["column"] == 5
        assert parser_state["pos"] == 3
    
    def test_parse_break_statement_preserves_other_state_fields(self):
        """Test that other parser_state fields are preserved."""
        tokens = [
            _create_token("BREAK", "break", 5, 10),
            _create_token("SEMICOLON", ";", 5, 15),
        ]
        parser_state = _create_parser_state(tokens, pos=0, filename="my_file.cc")
        parser_state["extra_field"] = "should_remain"
        
        result = _parse_break_statement(parser_state)
        
        assert parser_state["filename"] == "my_file.cc"
        assert parser_state["extra_field"] == "should_remain"
        assert parser_state["pos"] == 2


class TestParseBreakStatementBoundary:
    """Test boundary scenarios for _parse_break_statement."""
    
    def test_parse_break_statement_at_end_of_tokens_no_semicolon(self):
        """Test break at end of tokens without semicolon raises SyntaxError."""
        tokens = [
            _create_token("BREAK", "break", 1, 1),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_break_statement(parser_state)
        
        assert "Expected ';' after break statement" in str(exc_info.value)
        assert parser_state["pos"] == 1  # BREAK was consumed before error
    
    def test_parse_break_statement_followed_by_non_semicolon(self):
        """Test break followed by non-semicolon token raises SyntaxError."""
        tokens = [
            _create_token("BREAK", "break", 1, 1),
            _create_token("IDENTIFIER", "x", 1, 7),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_break_statement(parser_state)
        
        assert "Expected ';' after break statement" in str(exc_info.value)
        assert parser_state["pos"] == 1  # BREAK was consumed before error
    
    def test_parse_break_statement_empty_tokens_list(self):
        """Test with empty tokens list raises appropriate error."""
        tokens = []
        parser_state = _create_parser_state(tokens, pos=0)
        
        # This should fail when trying to access tokens[pos]
        with pytest.raises(IndexError):
            _parse_break_statement(parser_state)
    
    def test_parse_break_statement_pos_out_of_bounds(self):
        """Test with pos out of bounds raises appropriate error."""
        tokens = [
            _create_token("BREAK", "break", 1, 1),
        ]
        parser_state = _create_parser_state(tokens, pos=1)
        
        with pytest.raises(IndexError):
            _parse_break_statement(parser_state)


class TestParseBreakStatementASTStructure:
    """Test AST node structure returned by _parse_break_statement."""
    
    def test_parse_break_statement_ast_has_required_fields(self):
        """Test that returned AST has all required fields."""
        tokens = [
            _create_token("BREAK", "break", 10, 20),
            _create_token("SEMICOLON", ";", 10, 25),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        result = _parse_break_statement(parser_state)
        
        assert "type" in result
        assert "line" in result
        assert "column" in result
        assert "children" in result
        assert isinstance(result["children"], list)
    
    def test_parse_break_statement_ast_type_is_break_stmt(self):
        """Test that AST type is exactly BREAK_STMT."""
        tokens = [
            _create_token("BREAK", "break", 1, 1),
            _create_token("SEMICOLON", ";", 1, 6),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        result = _parse_break_statement(parser_state)
        
        assert result["type"] == "BREAK_STMT"
    
    def test_parse_break_statement_position_tracking(self):
        """Test that line and column are correctly tracked from BREAK token."""
        test_cases = [
            (1, 1),
            (5, 10),
            (100, 50),
            (1, 100),
        ]
        
        for line, column in test_cases:
            tokens = [
                _create_token("BREAK", "break", line, column),
                _create_token("SEMICOLON", ";", line, column + 5),
            ]
            parser_state = _create_parser_state(tokens, pos=0)
            
            result = _parse_break_statement(parser_state)
            
            assert result["line"] == line, f"Failed for line={line}"
            assert result["column"] == column, f"Failed for column={column}"


class TestParseBreakStatementSideEffects:
    """Test side effects of _parse_break_statement."""
    
    def test_parse_break_statement_consumes_both_tokens(self):
        """Test that both BREAK and SEMICOLON tokens are consumed."""
        tokens = [
            _create_token("BREAK", "break", 1, 1),
            _create_token("SEMICOLON", ";", 1, 6),
            _create_token("RETURN", "return", 2, 1),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        result = _parse_break_statement(parser_state)
        
        # Should have consumed BREAK and SEMICOLON (2 tokens)
        assert parser_state["pos"] == 2
    
    def test_parse_break_statement_multiple_calls(self):
        """Test multiple consecutive break statements."""
        tokens = [
            _create_token("BREAK", "break", 1, 1),
            _create_token("SEMICOLON", ";", 1, 6),
            _create_token("BREAK", "break", 2, 1),
            _create_token("SEMICOLON", ";", 2, 6),
        ]
        parser_state = _create_parser_state(tokens, pos=0)
        
        result1 = _parse_break_statement(parser_state)
        assert parser_state["pos"] == 2
        assert result1["line"] == 1
        
        result2 = _parse_break_statement(parser_state)
        assert parser_state["pos"] == 4
        assert result2["line"] == 2
