# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any
import sys

# === Mock dependencies before importing the module under test ===
# We need to mock the sub-modules to prevent import errors from the long dependency chain
# The key is to mock using the full absolute path that the imports will look for

_base_pkg = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package'

# Mock _consume_token_package
_mock_consume_pkg = MagicMock()
_mock_consume_src = MagicMock()
_mock_consume_src._consume_token = MagicMock()
_mock_consume_pkg._consume_token_src = _mock_consume_src
sys.modules[f'{_base_pkg}._consume_token_package'] = _mock_consume_pkg
sys.modules[f'{_base_pkg}._consume_token_package._consume_token_src'] = _mock_consume_src

# Also mock with relative path
sys.modules['._consume_token_package'] = _mock_consume_pkg
sys.modules['._consume_token_package._consume_token_src'] = _mock_consume_src

# Mock _parse_or_expression_package (this is the key one that has long dependency chain)
_mock_or_pkg = MagicMock()
_mock_or_src = MagicMock()
_mock_or_src._parse_or_expression = MagicMock(return_value={"type": "error", "value": "Mocked", "line": 0, "column": 0})
_mock_or_pkg._parse_or_expression_src = _mock_or_src
sys.modules[f'{_base_pkg}._parse_or_expression_package'] = _mock_or_pkg
sys.modules[f'{_base_pkg}._parse_or_expression_package._parse_or_expression_src'] = _mock_or_src

# Also mock with relative path
sys.modules['._parse_or_expression_package'] = _mock_or_pkg
sys.modules['._parse_or_expression_package._parse_or_expression_src'] = _mock_or_src

# === sub function imports ===
from ._parse_primary_expression_src import _parse_primary_expression


# === Test Helpers ===
def create_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: list, pos: int = 0, filename: str = "test.cc") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": None
    }


# === Test Cases ===
class TestParsePrimaryExpression(unittest.TestCase):
    """Test cases for _parse_primary_expression function."""

    def test_parse_ident_token(self):
        """Test parsing an IDENT token returns identifier AST node."""
        tokens = [create_token("IDENT", "myVar", 1, 5)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        mock_consume.assert_called_once_with(parser_state, "IDENT")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_token(self):
        """Test parsing a STRING token returns string_literal AST node."""
        tokens = [create_token("STRING", "hello world", 2, 10)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "string_literal")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        mock_consume.assert_called_once_with(parser_state, "STRING")

    def test_parse_number_token_integer(self):
        """Test parsing a NUMBER token (integer) returns number_literal with int value."""
        tokens = [create_token("NUMBER", "42", 1, 1)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "number_literal")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        mock_consume.assert_called_once_with(parser_state, "NUMBER")

    def test_parse_number_token_float_with_dot(self):
        """Test parsing a NUMBER token with decimal point returns float value."""
        tokens = [create_token("NUMBER", "3.14", 1, 1)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "number_literal")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)

    def test_parse_number_token_invalid_int_fallback_to_float(self):
        """Test parsing a NUMBER token that fails int conversion falls back to float."""
        tokens = [create_token("NUMBER", "1e10", 1, 1)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "number_literal")
        self.assertEqual(result["value"], 1e10)
        self.assertIsInstance(result["value"], float)

    def test_parse_true_token(self):
        """Test parsing a TRUE token returns boolean_literal with True."""
        tokens = [create_token("TRUE", "true", 3, 7)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "boolean_literal")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        mock_consume.assert_called_once_with(parser_state, "TRUE")

    def test_parse_false_token(self):
        """Test parsing a FALSE token returns boolean_literal with False."""
        tokens = [create_token("FALSE", "false", 3, 7)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "boolean_literal")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        mock_consume.assert_called_once_with(parser_state, "FALSE")

    def test_parse_parenthesized_expression(self):
        """Test parsing LPAREN ... RPAREN returns inner expression AST."""
        tokens = [
            create_token("LPAREN", "(", 1, 1),
            create_token("IDENT", "x", 1, 2),
            create_token("RPAREN", ")", 1, 3)
        ]
        parser_state = create_parser_state(tokens, 0)
        inner_ast = {"type": "identifier", "value": "x", "line": 1, "column": 2}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_parse_or:
                mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
                mock_parse_or.return_value = inner_ast
                
                result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result, inner_ast)
        self.assertEqual(mock_consume.call_count, 2)
        mock_consume.assert_any_call(parser_state, "LPAREN")
        mock_consume.assert_any_call(parser_state, "RPAREN")
        mock_parse_or.assert_called_once_with(parser_state)

    def test_parse_parenthesized_expression_with_error(self):
        """Test parsing LPAREN when inner expression has error propagates error."""
        tokens = [
            create_token("LPAREN", "(", 1, 1),
            create_token("IDENT", "x", 1, 2)
        ]
        parser_state = create_parser_state(tokens, 0)
        error_ast = {"type": "error", "value": "Parse error", "line": 1, "column": 2}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_parse_or:
                def parse_or_side_effect(ps):
                    ps["error"] = "Parse error"
                    return error_ast
                
                mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
                mock_parse_or.side_effect = parse_or_side_effect
                
                result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "error")
        self.assertIn("error", parser_state)

    def test_parse_parenthesized_missing_rparen(self):
        """Test parsing LPAREN without matching RPAREN sets error."""
        tokens = [
            create_token("LPAREN", "(", 1, 1),
            create_token("IDENT", "x", 1, 2)
        ]
        parser_state = create_parser_state(tokens, 0)
        inner_ast = {"type": "identifier", "value": "x", "line": 1, "column": 2}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_parse_or:
                mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
                mock_parse_or.return_value = inner_ast
                
                result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "error")
        self.assertIn("Expected ')'", parser_state.get("error", ""))

    def test_parse_parenthesized_wrong_closing_token(self):
        """Test parsing LPAREN with wrong closing token sets error."""
        tokens = [
            create_token("LPAREN", "(", 1, 1),
            create_token("IDENT", "x", 1, 2),
            create_token("SEMICOLON", ";", 1, 3)
        ]
        parser_state = create_parser_state(tokens, 0)
        inner_ast = {"type": "identifier", "value": "x", "line": 1, "column": 2}
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_or_expression_package._parse_or_expression_src._parse_or_expression") as mock_parse_or:
                mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
                mock_parse_or.return_value = inner_ast
                
                result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "error")
        self.assertIn("Expected ')'", parser_state.get("error", ""))
        self.assertIn("SEMICOLON", parser_state.get("error", ""))

    def test_parse_empty_tokens(self):
        """Test parsing with empty tokens list returns error."""
        tokens = []
        parser_state = create_parser_state(tokens, 0)
        
        result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state.get("error"), "Unexpected end of input")

    def test_parse_pos_beyond_tokens(self):
        """Test parsing when pos >= len(tokens) returns error."""
        tokens = [create_token("IDENT", "x", 1, 1)]
        parser_state = create_parser_state(tokens, 2)  # pos beyond tokens
        
        result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["value"], "Unexpected end of input")

    def test_parse_eof_token(self):
        """Test parsing EOF token returns error."""
        tokens = [create_token("EOF", "", 1, 1)]
        parser_state = create_parser_state(tokens, 0)
        
        result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "error")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state.get("error"), "Unexpected end of input")

    def test_parse_unknown_token_type(self):
        """Test parsing unknown token type returns error."""
        tokens = [create_token("UNKNOWN", "???", 1, 1)]
        parser_state = create_parser_state(tokens, 0)
        
        result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "error")
        self.assertIn("Unexpected token: UNKNOWN", parser_state.get("error", ""))

    def test_parse_ident_updates_pos(self):
        """Test that parsing IDENT correctly updates pos in parser_state."""
        tokens = [create_token("IDENT", "var", 1, 1)]
        parser_state = create_parser_state(tokens, 0)
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            _parse_primary_expression(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_with_existing_error(self):
        """Test parsing when parser_state already has error still processes."""
        tokens = [create_token("IDENT", "x", 1, 1)]
        parser_state = create_parser_state(tokens, 0)
        parser_state["error"] = "Previous error"
        
        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = lambda ps, expected: ps.update({"pos": ps.get("pos", 0) + 1})
            
            result = _parse_primary_expression(parser_state)
        
        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "x")


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()
