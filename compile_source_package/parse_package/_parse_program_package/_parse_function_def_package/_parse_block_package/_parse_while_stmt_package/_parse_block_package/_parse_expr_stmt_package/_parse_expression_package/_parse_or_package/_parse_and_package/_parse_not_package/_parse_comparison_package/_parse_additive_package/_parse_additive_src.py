# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative

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
def _parse_additive(parser_state: ParserState) -> AST:
    """Parse additive expressions (+, -)."""
    left = _parse_multiplicative(parser_state)
    
    while not _is_at_end(parser_state):
        token = _get_current_token(parser_state)
        if token.get("type") == "ARITH_OP" and token.get("value") in ("+", "-"):
            op_token = _consume_token(parser_state)
            right = _parse_multiplicative(parser_state)
            left = {
                "type": "BINARY_OP",
                "operator": op_token["value"],
                "children": [left, right],
                "line": op_token["line"],
                "column": op_token["column"]
            }
        else:
            break
    
    return left

# === helper functions ===
def _is_at_end(parser_state: ParserState) -> bool:
    """Check if parser has reached end of tokens."""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    return pos >= len(tokens)

def _get_current_token(parser_state: ParserState) -> Token:
    """Get current token without consuming it."""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos < len(tokens):
        return tokens[pos]
    return None

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing position."""
    token = _get_current_token(parser_state)
    if token is None:
        filename = parser_state.get("filename", "unknown")
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    parser_state["pos"] = parser_state.get("pos", 0) + 1
    return token

# === OOP compatibility layer ===
# Not required for parser function nodes
