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
#   "line": int,
#   "column": int,
#   "value": Any,
#   "literal_type": str,
#   "name": str,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "callee": AST,
#   "arguments": list
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
    """Parse OR expression (|| operator) with left-associativity."""
    left = _parse_and(parser_state)
    
    while _is_or_operator(parser_state):
        op_token = _advance(parser_state)
        right = _parse_and(parser_state)
        left = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """Get current token without advancing."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos < len(tokens):
        return tokens[pos]
    return {"type": "EOF", "value": "", "line": 0, "column": 0}

def _advance(parser_state: ParserState) -> Token:
    """Advance position and return the token that was at pos."""
    token = _current_token(parser_state)
    parser_state["pos"] = parser_state["pos"] + 1
    return token

def _is_or_operator(parser_state: ParserState) -> bool:
    """Check if current token is OR operator (||)."""
    token = _current_token(parser_state)
    return token.get("type") == "OR"

def _syntax_error(parser_state: ParserState, message: str) -> None:
    """Raise syntax error with location info."""
    token = _current_token(parser_state)
    filename = parser_state.get("filename", "<unknown>")
    raise SyntaxError(
        f"{filename}:{token['line']}:{token['column']}: {message}"
    )

# === OOP compatibility layer ===
# Not required for parser function nodes