from unittest.mock import patch
from typing import Dict, Any, List

# Relative import for the function under test
from ._parse_block_src import _parse_block


def create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dictionary."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dictionary."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseBlock:
    """Test cases for _parse_block function."""

    def test_empty_block(self):
        """Test parsing an empty block {}."""
        tokens = [
            create_token("LBRACE", "{", line=1, column=1),
            create_token("RBRACE", "}", line=1, column=2)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_block(parser_state)
        
        assert result["type"] == "BLOCK"
        assert result["children"] == []
        assert result["value"] is None
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 2

    def test_block_with_single_statement(self):
        """Test parsing a block with a single statement."""
        tokens = [
            create_token("LBRACE", "{", line=1, column=1),
            create_token("IDENT", "x", line=1, column=2),
            create_token("RBRACE", "}", line=1, column=3)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_stmt = {
            "type": "EXPR_STMT",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = lambda state: (state.update({"pos": 2}), mock_stmt)[1]
            result = _parse_block(parser_state)
        
        assert result["type"] == "BLOCK"
        assert len(result["children"]) == 1
        assert result["children"][0]["type"] == "EXPR_STMT"
        assert parser_state["pos"] == 3

    def test_block_with_multiple_statements(self):
        """Test parsing a block with multiple statements."""
        tokens = [
            create_token("LBRACE", "{", line=1, column=1),
            create_token("IDENT", "x", line=1, column=2),
            create_token("IDENT", "y", line=2, column=2),
            create_token("IDENT", "z", line=3, column=2),
            create_token("RBRACE", "}", line=3, column=3)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_stmts = [
            {"type": "EXPR_STMT", "children": [], "value": "x", "line": 1, "column": 2},
            {"type": "EXPR_STMT", "children": [], "value": "y", "line": 2, "column": 2},
            {"type": "EXPR_STMT", "children": [], "value": "z", "line": 3, "column": 2}
        ]
        
        call_count = [0]
        def mock_parse_statement_side_effect(state):
            stmt = mock_stmts[call_count[0]]
            call_count[0] += 1
            state["pos"] = call_count[0] + 1
            return stmt
        
        with patch("._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = mock_parse_statement_side_effect
            result = _parse_block(parser_state)
        
        assert result["type"] == "BLOCK"
        assert len(result["children"]) == 3
        assert result["children"][0]["value"] == "x"
        assert result["children"][1]["value"] == "y"
        assert result["children"][2]["value"] == "z"
        assert parser_state["pos"] == 5

    def test_block_preserves_start_position_info(self):
        """Test that BLOCK node preserves the starting token's line and column."""
        tokens = [
            create_token("LBRACE", "{", line=5, column=10),
            create_token("RBRACE", "}", line=5, column=11)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_block(parser_state)
        
        assert result["line"] == 5
        assert result["column"] == 10

    def test_block_no_rbrace_until_end(self):
        """Test parsing when RBRACE is not found until end of tokens."""
        tokens = [
            create_token("LBRACE", "{", line=1, column=1),
            create_token("IDENT", "x", line=1, column=2)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_stmt = {
            "type": "EXPR_STMT",
            "children": [],
            "value": "x",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = lambda state: (state.update({"pos": 2}), mock_stmt)[1]
            result = _parse_block(parser_state)
        
        assert result["type"] == "BLOCK"
        assert len(result["children"]) == 1
        assert parser_state["pos"] == 2

    def test_block_updates_parser_state_pos(self):
        """Test that parser_state pos is updated to after RBRACE."""
        tokens = [
            create_token("LBRACE", "{", line=1, column=1),
            create_token("RBRACE", "}", line=1, column=2),
            create_token("IDENT", "after", line=1, column=3)
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        result = _parse_block(parser_state)
        
        assert parser_state["pos"] == 2
        assert result["type"] == "BLOCK"

    def test_block_initializes_pos_correctly(self):
        """Test parsing block when pos starts at non-zero position."""
        tokens = [
            create_token("IDENT", "before", line=1, column=1),
            create_token("LBRACE", "{", line=1, column=2),
            create_token("RBRACE", "}", line=1, column=3)
        ]
        parser_state = create_parser_state(tokens, pos=1)
        
        result = _parse_block(parser_state)
        
        assert result["type"] == "BLOCK"
        assert result["line"] == 1
        assert result["column"] == 2
        assert parser_state["pos"] == 3
