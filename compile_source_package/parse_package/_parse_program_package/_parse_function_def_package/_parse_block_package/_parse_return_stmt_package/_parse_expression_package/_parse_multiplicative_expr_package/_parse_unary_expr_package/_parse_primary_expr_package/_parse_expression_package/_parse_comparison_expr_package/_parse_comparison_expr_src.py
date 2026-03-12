# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
def _parse_comparison_expr(parser_state: ParserState) -> AST:
    """Parse comparison expressions (==, !=, <, >, <=, >=) with left associativity."""
    COMPARISON_OPS = {"==", "!=", "<", ">", "<=", ">="}
    
    left = _parse_additive_expr(parser_state)
    
    while _is_comparison_op(parser_state, COMPARISON_OPS):
        op_token = _consume_token(parser_state)
        right = _parse_additive_expr(parser_state)
        left = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _is_comparison_op(parser_state: ParserState, comparison_ops: set) -> bool:
    """Check if current token is a comparison operator."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "OPERATOR" and token.get("value") in comparison_ops

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing pos."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    token = tokens[pos]
    parser_state["pos"] += 1
    return token

# === OOP compatibility layer ===
# Not needed for this parser function node
