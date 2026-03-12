# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary

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

# Operator precedence levels (higher = binds tighter)
PRECEDENCE = {
    "or": 1,
    "and": 2,
    "==": 3, "!=": 3, "<": 3, ">": 3, "<=": 3, ">=": 3,
    "+": 4, "-": 4,
    "*": 5, "/": 5,
}

BINARY_OPERATORS = set(PRECEDENCE.keys())

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """Parse complete expression with operator precedence and binary operations."""
    left = _parse_unary(parser_state)
    
    while _is_binary_operator(parser_state):
        op_token = _current_token(parser_state)
        op = op_token["value"]
        line = op_token.get("line", 0)
        column = op_token.get("column", 0)
        
        parser_state["pos"] += 1
        right = _parse_unary(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _is_binary_operator(parser_state: ParserState) -> bool:
    """Check if current token is a binary operator."""
    token = _current_token(parser_state)
    if token is None:
        return False
    return token.get("type") == "OPERATOR" and token.get("value") in BINARY_OPERATORS

def _current_token(parser_state: ParserState) -> Token:
    """Get current token at parser_state['pos']."""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos < len(tokens):
        return tokens[pos]
    return None

# === OOP compatibility layer ===
