# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse a full expression (entry point for expression parsing).
    Delegates to _parse_comparison which handles operator precedence.
    """
    return _parse_comparison(parser_state)

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """Get current token or return None if at end."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    return None

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing pos."""
    token = _current_token(parser_state)
    if token is None:
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}")
    parser_state["pos"] += 1
    return token

def _expect_token_type(parser_state: ParserState, expected_type: str) -> Token:
    """Expect current token to be of given type, consume and return it."""
    token = _current_token(parser_state)
    if token is None or token["type"] != expected_type:
        actual = token["value"] if token else "EOF"
        raise SyntaxError(
            f"Expected token type '{expected_type}', got '{actual}' "
            f"in {parser_state.get('filename', '<unknown>')}"
        )
    return _consume_token(parser_state)

# === OOP compatibility layer ===
