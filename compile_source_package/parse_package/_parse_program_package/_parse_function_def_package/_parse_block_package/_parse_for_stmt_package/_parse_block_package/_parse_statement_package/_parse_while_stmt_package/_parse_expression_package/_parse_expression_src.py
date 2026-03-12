# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
from ._parse_logical_or_package._parse_logical_or_src import _parse_logical_or

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
    """Parse expression with operator precedence."""
    # Entry point delegates to lowest precedence level
    return _parse_logical_or(parser_state)

# === helper functions ===
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """Get current token without consuming."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    return None

def _expect(parser_state: ParserState, token_type: str) -> Token:
    """Expect and consume a specific token type."""
    token = _current_token(parser_state)
    if token is None or token["type"] != token_type:
        raise SyntaxError(f"Expected {token_type}")
    parser_state["pos"] += 1
    return token

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper parser function