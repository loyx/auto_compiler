from unittest.mock import patch
from typing import Dict, Any, List

# Relative import for the module under test
from ._parse_expression_src import _parse_expression


def create_token(type_: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dictionary."""
    return {
        "type": type_,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dictionary."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": ""
    }


class TestParseExpression:
    """Test cases for _parse_expression function."""
    
    def test_single_term_no_operators(self):
        """Test parsing a single term without any operators."""
        term_node = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token:
            mock_parse_term.return_value = term_node
            mock_current_token.return_value = None  # EOF
            
            parser_state = create_parser_state([create_token("NUMBER", "42")])
            result = _parse_expression(parser_state)
            
            assert result == term_node
            mock_parse_term.assert_called_once_with(parser_state)
            mock_current_token.assert_called_once_with(parser_state)
    
    def test_two_terms_with_plus(self):
        """Test parsing two terms with PLUS operator."""
        term1 = {"type": "NUMBER", "value": "10", "line": 1, "column": 1, "children": []}
        term2 = {"type": "NUMBER", "value": "20", "line": 1, "column": 5, "children": []}
        plus_token = create_token("PLUS", "+", 1, 3)
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token, \
             patch("._parse_expression_src._consume_token") as mock_consume_token:
            mock_parse_term.side_effect = [term1, term2]
            mock_current_token.side_effect = [plus_token, None]
            mock_consume_token.return_value = plus_token
            
            parser_state = create_parser_state([
                create_token("NUMBER", "10"),
                create_token("PLUS", "+"),
                create_token("NUMBER", "20")
            ])
            result = _parse_expression(parser_state)
            
            assert result["type"] == "PLUS"
            assert result["value"] is None
            assert result["line"] == 1
            assert result["column"] == 3
            assert len(result["children"]) == 2
            assert result["children"][0] == term1
            assert result["children"][1] == term2
            
            assert mock_parse_term.call_count == 2
            assert mock_current_token.call_count == 2
            mock_consume_token.assert_called_once_with(parser_state)
    
    def test_two_terms_with_minus(self):
        """Test parsing two terms with MINUS operator."""
        term1 = {"type": "NUMBER", "value": "100", "line": 2, "column": 1, "children": []}
        term2 = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5, "children": []}
        minus_token = create_token("MINUS", "-", 2, 3)
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token, \
             patch("._parse_expression_src._consume_token") as mock_consume_token:
            mock_parse_term.side_effect = [term1, term2]
            mock_current_token.side_effect = [minus_token, None]
            mock_consume_token.return_value = minus_token
            
            parser_state = create_parser_state([
                create_token("NUMBER", "100"),
                create_token("MINUS", "-"),
                create_token("IDENTIFIER", "x")
            ])
            result = _parse_expression(parser_state)
            
            assert result["type"] == "MINUS"
            assert result["line"] == 2
            assert result["column"] == 3
            assert len(result["children"]) == 2
            assert result["children"][0] == term1
            assert result["children"][1] == term2
    
    def test_multiple_operators_left_associative(self):
        """Test that multiple operators are left-associative: a + b - c = (a + b) - c."""
        term1 = {"type": "NUMBER", "value": "1", "line": 1, "column": 1, "children": []}
        term2 = {"type": "NUMBER", "value": "2", "line": 1, "column": 3, "children": []}
        term3 = {"type": "NUMBER", "value": "3", "line": 1, "column": 5, "children": []}
        plus_token = create_token("PLUS", "+", 1, 2)
        minus_token = create_token("MINUS", "-", 1, 4)
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token, \
             patch("._parse_expression_src._consume_token") as mock_consume_token:
            mock_parse_term.side_effect = [term1, term2, term3]
            mock_current_token.side_effect = [plus_token, minus_token, None]
            mock_consume_token.side_effect = [plus_token, minus_token]
            
            parser_state = create_parser_state([
                create_token("NUMBER", "1"),
                create_token("PLUS", "+"),
                create_token("NUMBER", "2"),
                create_token("MINUS", "-"),
                create_token("NUMBER", "3")
            ])
            result = _parse_expression(parser_state)
            
            # Should be: (1 + 2) - 3
            # Outer node is MINUS
            assert result["type"] == "MINUS"
            assert result["line"] == 1
            assert result["column"] == 4
            assert len(result["children"]) == 2
            
            # Left child should be PLUS node
            left_child = result["children"][0]
            assert left_child["type"] == "PLUS"
            assert left_child["line"] == 1
            assert left_child["column"] == 2
            assert len(left_child["children"]) == 2
            assert left_child["children"][0] == term1
            assert left_child["children"][1] == term2
            
            # Right child should be term3
            assert result["children"][1] == term3
    
    def test_many_plus_operators(self):
        """Test parsing multiple PLUS operators in sequence."""
        tokens = [create_token("NUMBER", str(i)) for i in range(5)]
        plus_tokens = [create_token("PLUS", "+", 1, i*2+1) for i in range(4)]
        
        term_nodes = [{"type": "NUMBER", "value": str(i), "line": 1, "column": i*2, "children": []} for i in range(5)]
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token, \
             patch("._parse_expression_src._consume_token") as mock_consume_token:
            mock_parse_term.side_effect = term_nodes
            mock_current_token.side_effect = plus_tokens + [None]
            mock_consume_token.side_effect = plus_tokens
            
            parser_state = create_parser_state(tokens + plus_tokens)
            result = _parse_expression(parser_state)
            
            # Verify left-associative structure
            assert result["type"] == "PLUS"
            current = result
            for i in range(4):
                assert current["type"] == "PLUS"
                assert current["children"][0] == term_nodes[i] or (
                    i > 0 and current["children"][0]["type"] == "PLUS"
                )
                if i < 3:
                    current = current["children"][0]
            
            assert mock_parse_term.call_count == 5
            assert mock_current_token.call_count == 5
    
    def test_stops_at_semicolon(self):
        """Test that expression parsing stops at SEMICOLON token."""
        term_node = {"type": "NUMBER", "value": "42", "line": 1, "column": 1, "children": []}
        semicolon_token = create_token("SEMICOLON", ";", 1, 3)
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token:
            mock_parse_term.return_value = term_node
            mock_current_token.return_value = semicolon_token
            
            parser_state = create_parser_state([
                create_token("NUMBER", "42"),
                create_token("SEMICOLON", ";")
            ])
            result = _parse_expression(parser_state)
            
            assert result == term_node
            mock_parse_term.assert_called_once()
    
    def test_stops_at_other_operator(self):
        """Test that expression parsing stops at non-PLUS/MINUS operators like MUL."""
        term1 = {"type": "NUMBER", "value": "10", "line": 1, "column": 1, "children": []}
        term2 = {"type": "NUMBER", "value": "20", "line": 1, "column": 4, "children": []}
        mul_token = create_token("MUL", "*", 1, 3)
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token, \
             patch("._parse_expression_src._consume_token") as mock_consume_token:
            mock_parse_term.side_effect = [term1, term2]
            mock_current_token.side_effect = [mul_token, None]
            
            parser_state = create_parser_state([
                create_token("NUMBER", "10"),
                create_token("MUL", "*"),
                create_token("NUMBER", "20")
            ])
            result = _parse_expression(parser_state)
            
            # Should only parse the first term, stopping at MUL
            assert result == term1
            mock_parse_term.assert_called_once()
            mock_consume_token.assert_not_called()
    
    def test_position_advancement(self):
        """Test that parser_state pos is advanced correctly."""
        term1 = {"type": "NUMBER", "value": "1", "line": 1, "column": 1, "children": []}
        term2 = {"type": "NUMBER", "value": "2", "line": 1, "column": 3, "children": []}
        plus_token = create_token("PLUS", "+", 1, 2)
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token, \
             patch("._parse_expression_src._consume_token") as mock_consume_token:
            mock_parse_term.side_effect = [term1, term2]
            mock_current_token.side_effect = [plus_token, None]
            mock_consume_token.return_value = plus_token
            
            parser_state = create_parser_state([
                create_token("NUMBER", "1"),
                create_token("PLUS", "+"),
                create_token("NUMBER", "2")
            ], pos=0)
            
            _parse_expression(parser_state)
            
            # pos should be advanced past all consumed tokens
            assert parser_state["pos"] == 3
    
    def test_empty_token_list(self):
        """Test parsing with empty token list."""
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token:
            mock_parse_term.return_value = {"type": "NUMBER", "value": "0", "line": 1, "column": 1, "children": []}
            mock_current_token.return_value = None
            
            parser_state = create_parser_state([])
            result = _parse_expression(parser_state)
            
            assert result["type"] == "NUMBER"
            assert result["value"] == "0"
    
    def test_mixed_plus_minus_operators(self):
        """Test parsing expression with mixed PLUS and MINUS operators."""
        term1 = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1, "children": []}
        term2 = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3, "children": []}
        term3 = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5, "children": []}
        term4 = {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 7, "children": []}
        
        plus_token = create_token("PLUS", "+", 1, 2)
        minus_token1 = create_token("MINUS", "-", 1, 4)
        plus_token2 = create_token("PLUS", "+", 1, 6)
        
        with patch("._parse_expression_src._parse_term") as mock_parse_term, \
             patch("._parse_expression_src._current_token") as mock_current_token, \
             patch("._parse_expression_src._consume_token") as mock_consume_token:
            mock_parse_term.side_effect = [term1, term2, term3, term4]
            mock_current_token.side_effect = [plus_token, minus_token1, plus_token2, None]
            mock_consume_token.side_effect = [plus_token, minus_token1, plus_token2]
            
            parser_state = create_parser_state([
                create_token("IDENTIFIER", "a"),
                create_token("PLUS", "+"),
                create_token("IDENTIFIER", "b"),
                create_token("MINUS", "-"),
                create_token("IDENTIFIER", "c"),
                create_token("PLUS", "+"),
                create_token("IDENTIFIER", "d")
            ])
            result = _parse_expression(parser_state)
            
            # Should be: ((a + b) - c) + d
            assert result["type"] == "PLUS"
            assert result["column"] == 6
            
            # Left child should be MINUS: (a + b) - c
            left = result["children"][0]
            assert left["type"] == "MINUS"
            assert left["column"] == 4
            
            # Left-left should be PLUS: a + b
            left_left = left["children"][0]
            assert left_left["type"] == "PLUS"
            assert left_left["column"] == 2
            assert left_left["children"][0] == term1
            assert left_left["children"][1] == term2
            
            # Left-right should be c
            assert left["children"][1] == term3
            
            # Right should be d
            assert result["children"][1] == term4
