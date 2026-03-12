# === std / third-party imports ===
import pytest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

# === UUT import ===
from ._parse_if_stmt_src import _parse_if_stmt

# === Test Helpers ===
def create_token(type_: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": type_,
        "value": value,
        "line": line,
        "column": column
    }


# === Test Cases ===
class TestParseIfStmt:
    """Test cases for _parse_if_stmt function."""

    def test_parse_simple_if_without_else(self):
        """Test parsing a simple if statement without else branch."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
            create_token("IDENTIFIER", "x", 1, 4),
            create_token("RPAREN", ")", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("IDENTIFIER", "stmt", 1, 8),
            create_token("SEMICOLON", ";", 1, 12),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        mock_then_block_ast = {"type": "BODY", "children": [], "line": 1, "column": 8}

        with patch.object(_parse_expression, '__call__', return_value=mock_condition_ast) as mock_expr, \
             patch.object(_parse_block, '__call__', return_value=mock_then_block_ast) as mock_block:
            
            def expr_side_effect(state):
                state["pos"] = 3
                return mock_condition_ast
            
            def block_side_effect(state):
                state["pos"] = 7
                return mock_then_block_ast
            
            mock_expr.side_effect = expr_side_effect
            mock_block.side_effect = block_side_effect

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF"
            assert result["line"] == 1
            assert result["column"] == 1
            assert len(result["children"]) == 2
            assert result["children"][0] == mock_condition_ast
            assert result["children"][1] == mock_then_block_ast
            assert parser_state["pos"] == 7

    def test_parse_if_with_else(self):
        """Test parsing an if statement with else branch."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
            create_token("IDENTIFIER", "x", 1, 4),
            create_token("RPAREN", ")", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("IDENTIFIER", "stmt1", 1, 8),
            create_token("SEMICOLON", ";", 1, 13),
            create_token("ELSE", "else", 2, 1),
            create_token("COLON", ":", 2, 5),
            create_token("IDENTIFIER", "stmt2", 2, 7),
            create_token("SEMICOLON", ";", 2, 12),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        mock_then_block_ast = {"type": "BODY", "children": [], "line": 1, "column": 8}
        mock_else_block_ast = {"type": "BODY", "children": [], "line": 2, "column": 7}

        call_tracker = {"count": 0}
        
        def expr_side_effect(state):
            state["pos"] = 3
            return mock_condition_ast
        
        def block_dispatcher(state):
            call_tracker["count"] += 1
            if call_tracker["count"] == 1:
                state["pos"] = 7
                return mock_then_block_ast
            else:
                state["pos"] = 11
                return mock_else_block_ast

        with patch.object(_parse_expression, '__call__', side_effect=expr_side_effect) as mock_expr, \
             patch.object(_parse_block, '__call__', side_effect=block_dispatcher) as mock_block:

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF"
            assert result["line"] == 1
            assert result["column"] == 1
            assert len(result["children"]) == 3
            assert result["children"][0] == mock_condition_ast
            assert result["children"][1] == mock_then_block_ast
            assert result["children"][2] == mock_else_block_ast
            assert parser_state["pos"] == 11

    def test_missing_if_keyword(self):
        """Test that SyntaxError is raised when IF keyword is missing."""
        tokens = [
            create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError, match="Expected IF keyword"):
            _parse_if_stmt(parser_state)

    def test_missing_lparen(self):
        """Test that SyntaxError is raised when LPAREN is missing."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("IDENTIFIER", "x", 1, 3),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError, match="Expected '\\('"):
            _parse_if_stmt(parser_state)

    def test_missing_rparen(self):
        """Test that SyntaxError is raised when RPAREN is missing."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
            create_token("IDENTIFIER", "x", 1, 4),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}

        with patch.object(_parse_expression, '__call__', return_value=mock_condition_ast) as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 2
                return mock_condition_ast
            
            mock_expr.side_effect = expr_side_effect

            with pytest.raises(SyntaxError, match="Expected '\\)'"):
                _parse_if_stmt(parser_state)

    def test_missing_colon_after_condition(self):
        """Test that SyntaxError is raised when COLON is missing after condition."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
            create_token("IDENTIFIER", "x", 1, 4),
            create_token("RPAREN", ")", 1, 5),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}

        with patch.object(_parse_expression, '__call__', return_value=mock_condition_ast) as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 3
                return mock_condition_ast
            
            mock_expr.side_effect = expr_side_effect

            with pytest.raises(SyntaxError, match="Expected ':'"):
                _parse_if_stmt(parser_state)

    def test_missing_colon_after_else(self):
        """Test that SyntaxError is raised when COLON is missing after ELSE."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
            create_token("IDENTIFIER", "x", 1, 4),
            create_token("RPAREN", ")", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("IDENTIFIER", "stmt", 1, 8),
            create_token("SEMICOLON", ";", 1, 12),
            create_token("ELSE", "else", 2, 1),
            create_token("IDENTIFIER", "stmt2", 2, 6),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        mock_then_block_ast = {"type": "BODY", "children": [], "line": 1, "column": 8}

        with patch.object(_parse_expression, '__call__', return_value=mock_condition_ast) as mock_expr, \
             patch.object(_parse_block, '__call__', return_value=mock_then_block_ast) as mock_block:
            
            def expr_side_effect(state):
                state["pos"] = 3
                return mock_condition_ast
            
            def block_side_effect(state):
                state["pos"] = 7
                return mock_then_block_ast
            
            mock_expr.side_effect = expr_side_effect
            mock_block.side_effect = block_side_effect

            with pytest.raises(SyntaxError, match="Expected ':' after ELSE"):
                _parse_if_stmt(parser_state)

    def test_eof_scenarios(self):
        """Test various EOF scenarios."""
        # EOF right after IF
        tokens = [create_token("IF", "if", 1, 1)]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        with pytest.raises(SyntaxError):
            _parse_if_stmt(parser_state)

        # EOF after LPAREN
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        with pytest.raises(SyntaxError):
            _parse_if_stmt(parser_state)

    def test_pos_updated_correctly(self):
        """Test that parser_state pos is updated correctly throughout parsing."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
            create_token("IDENTIFIER", "x", 1, 4),
            create_token("RPAREN", ")", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("IDENTIFIER", "stmt", 1, 8),
            create_token("SEMICOLON", ";", 1, 12),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        mock_then_block_ast = {"type": "BODY", "children": [], "line": 1, "column": 8}

        with patch.object(_parse_expression, '__call__', return_value=mock_condition_ast) as mock_expr, \
             patch.object(_parse_block, '__call__', return_value=mock_then_block_ast) as mock_block:
            
            def expr_side_effect(state):
                state["pos"] = 3
                return mock_condition_ast
            
            def block_side_effect(state):
                state["pos"] = 7
                return mock_then_block_ast
            
            mock_expr.side_effect = expr_side_effect
            mock_block.side_effect = block_side_effect

            _parse_if_stmt(parser_state)

            assert parser_state["pos"] == 7

    def test_ast_structure(self):
        """Test that the AST node has correct structure."""
        tokens = [
            create_token("IF", "if", 1, 1),
            create_token("LPAREN", "(", 1, 3),
            create_token("IDENTIFIER", "x", 1, 4),
            create_token("RPAREN", ")", 1, 5),
            create_token("COLON", ":", 1, 6),
            create_token("IDENTIFIER", "stmt", 1, 8),
            create_token("SEMICOLON", ";", 1, 12),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        mock_condition_ast = {"type": "EXPR", "children": [], "line": 1, "column": 4}
        mock_then_block_ast = {"type": "BODY", "children": [], "line": 1, "column": 8}

        with patch.object(_parse_expression, '__call__', return_value=mock_condition_ast) as mock_expr, \
             patch.object(_parse_block, '__call__', return_value=mock_then_block_ast) as mock_block:
            
            def expr_side_effect(state):
                state["pos"] = 3
                return mock_condition_ast
            
            def block_side_effect(state):
                state["pos"] = 7
                return mock_then_block_ast
            
            mock_expr.side_effect = expr_side_effect
            mock_block.side_effect = block_side_effect

            result = _parse_if_stmt(parser_state)

            # Verify required fields
            assert "type" in result
            assert "line" in result
            assert "column" in result
            assert "children" in result
            assert result["type"] == "IF"
            assert isinstance(result["children"], list)
            assert len(result["children"]) >= 2
