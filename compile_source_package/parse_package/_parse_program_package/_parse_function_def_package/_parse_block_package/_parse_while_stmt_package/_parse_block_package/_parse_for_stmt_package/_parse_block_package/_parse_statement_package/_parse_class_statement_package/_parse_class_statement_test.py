# === std / third-party imports ===
import pytest
from unittest.mock import patch
from typing import Any, Dict

# === sub function imports ===
from ._parse_class_statement_src import _parse_class_statement


# === Test Helpers ===
def create_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
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


# === Test Cases ===

class TestParseClassStatementHappyPath:
    """Test happy path scenarios for _parse_class_statement."""
    
    def test_simple_class_definition(self):
        """Test parsing a simple class definition without inheritance."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("COLON", ":", 1, 14),
            create_token("STATEMENT", "pass", 2, 4),
            create_token("SEMICOLON", ";", 2, 8),
        ]
        parser_state = create_parser_state(tokens)
        
        mock_block = {
            "type": "BLOCK",
            "line": 2,
            "column": 4,
            "children": []
        }
        
        def mock_parse_block(state):
            state["pos"] = 4  # Move past STATEMENT token to SEMICOLON
            return mock_block
        
        import sys
        module_name = _parse_class_statement.__module__
        if module_name in sys.modules:
            module = sys.modules[module_name]
            with patch.object(module, '_parse_block', side_effect=mock_parse_block):
                result = _parse_class_statement(parser_state)
        
        assert result["type"] == "CLASS_STMT"
        assert result["line"] == 1
        assert result["column"] == 1
        assert len(result["children"]) == 2  # NAME and BODY
        assert result["children"][0]["type"] == "NAME"
        assert result["children"][0]["value"] == "MyClass"
        assert result["children"][1]["type"] == "BODY"
        assert parser_state["pos"] == 5  # All tokens consumed
    
    def test_class_with_inheritance(self):
        """Test parsing a class definition with base classes."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("LPAREN", "(", 1, 14),
            create_token("IDENT", "Base1", 1, 15),
            create_token("COMMA", ",", 1, 20),
            create_token("IDENT", "Base2", 1, 22),
            create_token("RPAREN", ")", 1, 27),
            create_token("COLON", ":", 1, 29),
            create_token("STATEMENT", "pass", 2, 4),
            create_token("SEMICOLON", ";", 2, 8),
        ]
        parser_state = create_parser_state(tokens)
        
        mock_bases = [
            {"type": "BASE", "value": "Base1"},
            {"type": "BASE", "value": "Base2"}
        ]
        
        def mock_parse_base_class_list(state):
            state["pos"] = 6  # Move to RPAREN (will be consumed by caller)
            return mock_bases
        
        mock_block = {
            "type": "BLOCK",
            "line": 2,
            "column": 4,
            "children": []
        }
        
        def mock_parse_block(state):
            state["pos"] = 9  # Move past STATEMENT token to SEMICOLON
            return mock_block
        
        import sys
        module_name = _parse_class_statement.__module__
        if module_name in sys.modules:
            module = sys.modules[module_name]
            with patch.object(module, '_parse_base_class_list', side_effect=mock_parse_base_class_list):
                with patch.object(module, '_parse_block', side_effect=mock_parse_block):
                    result = _parse_class_statement(parser_state)
        
        assert result["type"] == "CLASS_STMT"
        assert len(result["children"]) == 3  # NAME, BASES, and BODY
        assert result["children"][0]["type"] == "NAME"
        assert result["children"][1]["type"] == "BASES"
        assert result["children"][1]["children"] == mock_bases
        assert result["children"][2]["type"] == "BODY"


class TestParseClassStatementErrors:
    """Test error scenarios for _parse_class_statement."""
    
    def test_missing_class_keyword(self):
        """Test error when CLASS token is missing."""
        tokens = [
            create_token("IDENT", "MyClass", 1, 1),
        ]
        parser_state = create_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_class_statement(parser_state)
        
        assert "Expected 'class' keyword" in str(exc_info.value)
    
    def test_missing_class_name(self):
        """Test error when class name is missing after CLASS keyword."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("COLON", ":", 1, 7),
        ]
        parser_state = create_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_class_statement(parser_state)
        
        assert "Expected class name" in str(exc_info.value)
    
    def test_missing_rparen_after_bases(self):
        """Test error when RPAREN is missing after base class list."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("LPAREN", "(", 1, 14),
            create_token("IDENT", "Base1", 1, 15),
            create_token("COLON", ":", 1, 20),
        ]
        parser_state = create_parser_state(tokens)
        
        mock_bases = [{"type": "BASE", "value": "Base1"}]
        
        import sys
        module_name = _parse_class_statement.__module__
        if module_name in sys.modules:
            module = sys.modules[module_name]
            with patch.object(module, '_parse_base_class_list', return_value=mock_bases):
                with pytest.raises(SyntaxError) as exc_info:
                    _parse_class_statement(parser_state)
        
        assert "Expected ')'" in str(exc_info.value)
    
    def test_missing_colon(self):
        """Test error when COLON is missing after class signature."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("STATEMENT", "pass", 1, 15),
        ]
        parser_state = create_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_class_statement(parser_state)
        
        assert "Expected ':'" in str(exc_info.value)
    
    def test_missing_class_body(self):
        """Test error when class body is missing after COLON."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("COLON", ":", 1, 14),
        ]
        parser_state = create_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_class_statement(parser_state)
        
        assert "Expected class body" in str(exc_info.value)
    
    def test_missing_semicolon(self):
        """Test error when SEMICOLON is missing after class body."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("COLON", ":", 1, 14),
            create_token("STATEMENT", "pass", 2, 4),
        ]
        parser_state = create_parser_state(tokens)
        
        mock_block = {
            "type": "BLOCK",
            "line": 2,
            "column": 4,
            "children": []
        }
        
        def mock_parse_block(state):
            state["pos"] = 4  # Move past STATEMENT token to SEMICOLON
            return mock_block
        
        import sys
        module_name = _parse_class_statement.__module__
        if module_name in sys.modules:
            module = sys.modules[module_name]
            with patch.object(module, '_parse_block', side_effect=mock_parse_block):
                with pytest.raises(SyntaxError) as exc_info:
                    _parse_class_statement(parser_state)
        
        assert "Expected ';'" in str(exc_info.value)
    
    def test_empty_tokens(self):
        """Test error when token list is empty."""
        parser_state = create_parser_state([])
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_class_statement(parser_state)
        
        assert "Expected 'class' keyword" in str(exc_info.value)


class TestParseClassStatementEdgeCases:
    """Test edge cases for _parse_class_statement."""
    
    def test_class_at_end_of_file_without_semicolon(self):
        """Test class definition at end of tokens without SEMICOLON."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("COLON", ":", 1, 14),
        ]
        parser_state = create_parser_state(tokens)
        
        with pytest.raises(SyntaxError):
            _parse_class_statement(parser_state)
    
    def test_position_advancement(self):
        """Test that parser_state position is correctly advanced."""
        tokens = [
            create_token("CLASS", "class", 1, 1),
            create_token("IDENT", "MyClass", 1, 7),
            create_token("COLON", ":", 1, 14),
            create_token("STATEMENT", "pass", 2, 4),
            create_token("SEMICOLON", ";", 2, 8),
            create_token("EOF", "", 2, 9),
        ]
        parser_state = create_parser_state(tokens)
        
        mock_block = {
            "type": "BLOCK",
            "line": 2,
            "column": 4,
            "children": []
        }
        
        def mock_parse_block(state):
            state["pos"] = 4  # Move past STATEMENT token to SEMICOLON
            return mock_block
        
        import sys
        module_name = _parse_class_statement.__module__
        if module_name in sys.modules:
            module = sys.modules[module_name]
            with patch.object(module, '_parse_block', side_effect=mock_parse_block):
                _parse_class_statement(parser_state)
        
        assert parser_state["pos"] == 5  # Position after SEMICOLON
    
    def test_ast_node_line_column_preservation(self):
        """Test that AST node preserves line and column from CLASS token."""
        tokens = [
            create_token("CLASS", "class", 5, 10),
            create_token("IDENT", "MyClass", 5, 16),
            create_token("COLON", ":", 5, 23),
            create_token("STATEMENT", "pass", 6, 4),
            create_token("SEMICOLON", ";", 6, 8),
        ]
        parser_state = create_parser_state(tokens)
        
        mock_block = {
            "type": "BLOCK",
            "line": 6,
            "column": 4,
            "children": []
        }
        
        def mock_parse_block(state):
            state["pos"] = 4  # Move past STATEMENT token to SEMICOLON
            return mock_block
        
        import sys
        module_name = _parse_class_statement.__module__
        if module_name in sys.modules:
            module = sys.modules[module_name]
            with patch.object(module, '_parse_block', side_effect=mock_parse_block):
                result = _parse_class_statement(parser_state)
        
        assert result["line"] == 5
        assert result["column"] == 10
        assert result["children"][0]["line"] == 5
        assert result["children"][0]["column"] == 16


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
