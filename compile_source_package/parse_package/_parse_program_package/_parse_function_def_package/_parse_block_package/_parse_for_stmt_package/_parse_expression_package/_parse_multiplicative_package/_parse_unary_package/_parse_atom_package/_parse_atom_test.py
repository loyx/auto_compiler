# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === relative imports ===
from ._parse_atom_src import _parse_atom


# === Test Helpers ===
def make_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser_state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": None
    }


# === Test Cases ===
class TestParseAtom(unittest.TestCase):
    """Test cases for _parse_atom function."""

    def test_eof_empty_tokens(self):
        """Test parsing when tokens list is empty."""
        parser_state = make_parser_state([])
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unexpected_eof")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_eof_at_position(self):
        """Test parsing when pos is beyond tokens length."""
        tokens = [make_token("IDENTIFIER", "x")]
        parser_state = make_parser_state(tokens, pos=1)
        result = _parse_atom(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unexpected_eof")
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_identifier_token(self, mock_handle_atom):
        """Test parsing an IDENTIFIER token."""
        mock_handle_atom.return_value = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        tokens = [make_token("IDENTIFIER", "x")]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_handle_atom.assert_called_once()
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 0)  # _handle_atom_token should update pos

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_number_literal_token(self, mock_handle_atom):
        """Test parsing a NUMBER literal token."""
        mock_handle_atom.return_value = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1,
            "children": []
        }
        
        tokens = [make_token("NUMBER", "42")]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_handle_atom.assert_called_once()
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_string_literal_token(self, mock_handle_atom):
        """Test parsing a STRING literal token."""
        mock_handle_atom.return_value = {
            "type": "LITERAL",
            "value": "hello",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        tokens = [make_token("STRING", "hello")]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_handle_atom.assert_called_once()
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_boolean_true_token(self, mock_handle_atom):
        """Test parsing a TRUE literal token."""
        mock_handle_atom.return_value = {
            "type": "LITERAL",
            "value": True,
            "line": 1,
            "column": 1,
            "children": []
        }
        
        tokens = [make_token("TRUE", "true")]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_handle_atom.assert_called_once()
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_boolean_false_token(self, mock_handle_atom):
        """Test parsing a FALSE literal token."""
        mock_handle_atom.return_value = {
            "type": "LITERAL",
            "value": False,
            "line": 1,
            "column": 1,
            "children": []
        }
        
        tokens = [make_token("FALSE", "false")]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_handle_atom.assert_called_once()
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_none_literal_token(self, mock_handle_atom):
        """Test parsing a NONE/NULL literal token."""
        mock_handle_atom.return_value = {
            "type": "LITERAL",
            "value": None,
            "line": 1,
            "column": 1,
            "children": []
        }
        
        tokens = [make_token("NONE", "None")]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_handle_atom.assert_called_once()
        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])

    @patch('._parse_atom_package._parse_atom_src._parse_expression')
    def test_lparen_success(self, mock_parse_expr):
        """Test parsing a parenthesized expression successfully."""
        mock_parse_expr.return_value = {
            "type": "BINARY_OP",
            "value": "+",
            "line": 1,
            "column": 2,
            "children": []
        }
        
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("NUMBER", "1", 1, 2),
            make_token("RPAREN", ")", 1, 3)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_parse_expr.assert_called_once()
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(parser_state["pos"], 3)  # Should consume LPAREN, inner expr, and RPAREN
        self.assertIsNone(parser_state.get("error"))

    @patch('._parse_atom_package._parse_atom_src._parse_expression')
    def test_lparen_error_in_inner_expr(self, mock_parse_expr):
        """Test parsing when inner expression has an error."""
        mock_parse_expr.return_value = {
            "type": "ERROR",
            "value": "syntax_error",
            "line": 1,
            "column": 2,
            "children": []
        }
        
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("NUMBER", "1", 1, 2)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        parser_state["error"] = "syntax error in expression"
        
        result = _parse_atom(parser_state)
        
        mock_parse_expr.assert_called_once()
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "syntax error in expression")

    @patch('._parse_atom_package._parse_atom_src._parse_expression')
    def test_lparen_missing_rparen_eof(self, mock_parse_expr):
        """Test parsing when RPAREN is missing due to EOF."""
        mock_parse_expr.return_value = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 2,
            "children": []
        }
        
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("IDENTIFIER", "x", 1, 2)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_parse_expr.assert_called_once()
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "missing_rparen")
        self.assertIn("Unexpected end of input", parser_state["error"])

    @patch('._parse_atom_package._parse_atom_src._parse_expression')
    def test_lparen_wrong_token_after_expr(self, mock_parse_expr):
        """Test parsing when token after expression is not RPAREN."""
        mock_parse_expr.return_value = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 2,
            "children": []
        }
        
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("IDENTIFIER", "x", 1, 2),
            make_token("COMMA", ",", 1, 3)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        result = _parse_atom(parser_state)
        
        mock_parse_expr.assert_called_once()
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "missing_rparen")
        self.assertIn("Expected ')'", parser_state["error"])

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_handle_atom_token_sets_error(self, mock_handle_atom):
        """Test when _handle_atom_token encounters an unsupported token."""
        mock_handle_atom.return_value = {
            "type": "ERROR",
            "value": "unsupported_token",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        tokens = [make_token("UNKNOWN", "???")]
        parser_state = make_parser_state(tokens, pos=0)
        parser_state["error"] = "Unsupported token type: UNKNOWN"
        
        result = _parse_atom(parser_state)
        
        mock_handle_atom.assert_called_once()
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "unsupported_token")

    def test_pos_updated_after_paren_parsing(self):
        """Test that pos is correctly updated after parsing parenthesized expression."""
        with patch('._parse_atom_package._parse_atom_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 2,
                "children": []
            }
            
            tokens = [
                make_token("LPAREN", "(", 1, 1),
                make_token("IDENTIFIER", "x", 1, 2),
                make_token("RPAREN", ")", 1, 3),
                make_token("NUMBER", "5", 1, 4)
            ]
            parser_state = make_parser_state(tokens, pos=0)
            result = _parse_atom(parser_state)
            
            self.assertEqual(parser_state["pos"], 3)  # Should point to token after RPAREN
            self.assertEqual(result["type"], "IDENTIFIER")

    @patch('._parse_atom_package._parse_atom_src._handle_atom_token')
    def test_multiple_atoms_sequential_parsing(self, mock_handle_atom):
        """Test parsing multiple atoms sequentially (pos management)."""
        mock_handle_atom.side_effect = [
            {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 1,
                "children": []
            },
            {
                "type": "LITERAL",
                "value": 42,
                "line": 1,
                "column": 3,
                "children": []
            }
        ]
        
        tokens = [
            make_token("IDENTIFIER", "x", 1, 1),
            make_token("NUMBER", "42", 1, 3)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        # Parse first atom
        result1 = _parse_atom(parser_state)
        self.assertEqual(result1["type"], "IDENTIFIER")
        self.assertEqual(result1["value"], "x")
        
        # Parse second atom
        result2 = _parse_atom(parser_state)
        self.assertEqual(result2["type"], "LITERAL")
        self.assertEqual(result2["value"], 42)


if __name__ == "__main__":
    unittest.main()
