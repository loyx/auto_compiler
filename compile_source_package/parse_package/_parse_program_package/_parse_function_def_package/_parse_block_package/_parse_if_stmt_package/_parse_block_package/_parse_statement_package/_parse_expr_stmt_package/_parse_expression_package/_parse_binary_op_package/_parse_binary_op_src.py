# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_binary_op(parser_state: dict, min_precedence: int, left: dict) -> dict:
    """Parse binary operations with operator precedence using precedence climbing."""
    tokens = parser_state["tokens"]
    filename = parser_state.get("filename", "<unknown>")
    
    while parser_state["pos"] < len(tokens):
        op_token = tokens[parser_state["pos"]]
        if op_token["type"] not in ("PLUS", "MINUS", "STAR", "SLASH"):
            break
        
        op_precedence = _get_precedence(op_token["type"])
        if op_precedence < min_precedence:
            break
        
        parser_state["pos"] += 1  # consume operator
        right = _parse_primary(parser_state)
        
        # Check for higher precedence operators and recursively parse
        while parser_state["pos"] < len(tokens):
            next_op = tokens[parser_state["pos"]]
            if next_op["type"] not in ("PLUS", "MINUS", "STAR", "SLASH"):
                break
            next_precedence = _get_precedence(next_op["type"])
            if next_precedence <= op_precedence:
                break
            right = _parse_binary_op(parser_state, next_precedence, right)
        
        left = {
            "type": "BINARY_EXPR",
            "value": op_token["type"],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _get_precedence(op_type: str) -> int:
    """Get operator precedence level."""
    if op_type in ("PLUS", "MINUS"):
        return 1
    elif op_type in ("STAR", "SLASH"):
        return 2
    return 0

# === OOP compatibility layer ===
