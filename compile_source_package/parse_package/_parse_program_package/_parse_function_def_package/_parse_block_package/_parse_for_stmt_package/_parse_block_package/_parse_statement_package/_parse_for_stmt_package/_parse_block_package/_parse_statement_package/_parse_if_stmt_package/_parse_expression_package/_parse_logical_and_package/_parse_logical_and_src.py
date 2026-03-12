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
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": str,
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
def _parse_logical_and(parser_state: ParserState) -> AST:
    """Parse logical AND expressions (&& operator)."""
    left = _parse_comparison(parser_state)
    
    while _is_operator_at(parser_state, "&&"):
        op_token = _current_token(parser_state)
        _consume_token(parser_state)
        
        right = _parse_comparison(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "operator": "&&",
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """Get current token at parser_state['pos']."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    return tokens[pos]

def _consume_token(parser_state: ParserState) -> None:
    """Advance parser_state['pos'] by one."""
    parser_state["pos"] += 1

def _is_operator_at(parser_state: ParserState, op: str) -> bool:
    """Check if current token matches the operator."""
    token = _current_token(parser_state)
    return token["type"] == "OPERATOR" and token["value"] == op

# === OOP compatibility layer ===
