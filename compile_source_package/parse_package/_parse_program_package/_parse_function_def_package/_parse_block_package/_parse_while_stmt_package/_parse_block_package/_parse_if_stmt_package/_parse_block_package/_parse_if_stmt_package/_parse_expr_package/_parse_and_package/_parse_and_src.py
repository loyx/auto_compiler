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
def _parse_and(parser_state: ParserState) -> AST:
    """Parse AND expression with left associativity."""
    left = _parse_comparison(parser_state)
    
    while _is_and_operator(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_comparison(parser_state)
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": "AND",
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _is_and_operator(parser_state: ParserState) -> bool:
    """Check if current token is AND operator."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token["type"] == "OPERATOR" and token["value"] == "AND"

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing pos."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
