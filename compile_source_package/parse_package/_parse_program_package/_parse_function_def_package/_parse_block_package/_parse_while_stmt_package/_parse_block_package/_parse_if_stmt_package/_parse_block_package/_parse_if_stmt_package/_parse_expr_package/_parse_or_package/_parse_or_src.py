# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and

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
def _parse_or(parser_state: ParserState) -> AST:
    """Parse OR expression (lowest precedence) with left-associativity."""
    left = _parse_and(parser_state)
    
    while _is_current_token_or(parser_state):
        or_token = _consume_current_token(parser_state)
        right = _parse_and(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": "OR",
            "line": or_token.get("line", 0),
            "column": or_token.get("column", 0)
        }
    
    return left

# === helper functions ===
def _is_current_token_or(parser_state: ParserState) -> bool:
    """Check if current token is OR operator."""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        return False
    
    token = tokens[pos]
    return (token.get("type") == "OPERATOR" and 
            token.get("value", "").upper() == "OR")

def _consume_current_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing pos."""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
