from unittest.mock import patch
from typing import Dict, Any

from ._parse_unary_expr_src import _parse_unary_expr


def create_token(type_: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": type_,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseUnaryExpr:
    """Test cases for _parse_unary_expr function."""
    
    def test_parse_unary_minus(self):
        """Test parsing unary minus operator."""
        tokens = [
            create_token("MINUS", "-", 1, 1),
            create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = create_parser_state(tokens)
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["value"] == "-"
            assert result["line"] == 1
            assert result["column"] == 1
            assert len(result["children"]) == 1
            assert result["children"][0]["type"] == "IDENTIFIER"
            assert parser_state["pos"] == 2
    
    def test_parse_unary_plus(self):
        """Test parsing unary plus operator."""
        tokens = [
            create_token("PLUS", "+", 1, 1),
            create_token("NUMBER", "42", 1, 2)
        ]
        parser_state = create_parser_state(tokens)
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": "42",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["value"] == "+"
            assert len(result["children"]) == 1
    
    def test_parse_unary_not(self):
        """Test parsing unary NOT operator."""
        tokens = [
            create_token("NOT", "!", 1, 1),
            create_token("IDENTIFIER", "flag", 1, 2)
        ]
        parser_state = create_parser_state(tokens)
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["value"] == "!"
            assert len(result["children"]) == 1
    
    def test_parse_nested_unary_operators(self):
        """Test parsing nested unary operators (right-associativity)."""
        tokens = [
            create_token("MINUS", "-", 1, 1),
            create_token("MINUS", "-", 1, 2),
            create_token("IDENTIFIER", "x", 1, 3)
        ]
        parser_state = create_parser_state(tokens)
        
        def primary_side_effect(state):
            return {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
        
        with patch("._parse_unary_expr_src._parse_primary_expr", side_effect=primary_side_effect):
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["value"] == "-"
            assert len(result["children"]) == 1
            
            inner = result["children"][0]
            assert inner["type"] == "UNARY_OP"
            assert inner["value"] == "-"
            assert len(inner["children"]) == 1
            assert inner["children"][0]["type"] == "IDENTIFIER"
            
            assert parser_state["pos"] == 3
    
    def test_parse_no_unary_operator(self):
        """Test when current token is not a unary operator."""
        tokens = [
            create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = create_parser_state(tokens)
        
        expected_primary = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_unary_expr_src._parse_primary_expr", return_value=expected_primary) as mock_primary:
            result = _parse_unary_expr(parser_state)
            
            mock_primary.assert_called_once_with(parser_state)
            assert result == expected_primary
            assert parser_state["pos"] == 0
    
    def test_parse_error_in_operand(self):
        """Test error handling when operand parsing fails."""
        tokens = [
            create_token("MINUS", "-", 1, 1),
            create_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = create_parser_state(tokens)
        
        def primary_with_error(state):
            state["error"] = "Unexpected token"
            return {
                "type": "ERROR",
                "value": "Unexpected token",
                "children": [],
                "line": 0,
                "column": 0
            }
        
        with patch("._parse_unary_expr_src._parse_primary_expr", side_effect=primary_with_error):
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "ERROR"
            assert result["value"] == "Unexpected token"
            assert "error" in parser_state
    
    def test_empty_tokens(self):
        """Test with empty token list."""
        parser_state = create_parser_state([])
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "ERROR",
                "value": "No tokens",
                "children": [],
                "line": 0,
                "column": 0
            }
            
            result = _parse_unary_expr(parser_state)
            
            mock_primary.assert_called_once()
            assert result["type"] == "ERROR"
    
    def test_position_at_end(self):
        """Test when position is at end of tokens."""
        tokens = [
            create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = create_parser_state(tokens, pos=1)
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "ERROR",
                "value": "Unexpected end",
                "children": [],
                "line": 0,
                "column": 0
            }
            
            result = _parse_unary_expr(parser_state)
            
            mock_primary.assert_called_once()
            assert parser_state["pos"] == 1
    
    def test_unary_operator_preserves_position_on_error(self):
        """Test that position is updated even when operand fails."""
        tokens = [
            create_token("MINUS", "-", 1, 1),
            create_token("INVALID", "???", 1, 2)
        ]
        parser_state = create_parser_state(tokens)
        
        def primary_sets_error(state):
            state["error"] = "Invalid operand"
            return {
                "type": "ERROR",
                "value": "Invalid operand",
                "children": [],
                "line": 0,
                "column": 0
            }
        
        with patch("._parse_unary_expr_src._parse_primary_expr", side_effect=primary_sets_error):
            result = _parse_unary_expr(parser_state)
            
            assert parser_state["pos"] == 1
            assert result["type"] == "ERROR"
    
    def test_multiple_unary_operators_chain(self):
        """Test chain of three unary operators."""
        tokens = [
            create_token("NOT", "!", 1, 1),
            create_token("MINUS", "-", 1, 2),
            create_token("PLUS", "+", 1, 3),
            create_token("NUMBER", "5", 1, 4)
        ]
        parser_state = create_parser_state(tokens)
        
        with patch("._parse_unary_expr_src._parse_primary_expr") as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": "5",
                "children": [],
                "line": 1,
                "column": 4
            }
            
            result = _parse_unary_expr(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["value"] == "!"
            
            inner1 = result["children"][0]
            assert inner1["type"] == "UNARY_OP"
            assert inner1["value"] == "-"
            
            inner2 = inner1["children"][0]
            assert inner2["type"] == "UNARY_OP"
            assert inner2["value"] == "+"
            
            inner3 = inner2["children"][0]
            assert inner3["type"] == "LITERAL"
            assert inner3["value"] == "5"
            
            assert parser_state["pos"] == 4