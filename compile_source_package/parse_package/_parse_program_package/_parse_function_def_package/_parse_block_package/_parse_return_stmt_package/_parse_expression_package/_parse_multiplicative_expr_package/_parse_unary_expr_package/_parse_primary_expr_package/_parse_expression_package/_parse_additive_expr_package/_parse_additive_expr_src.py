# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """
    Parse additive expressions (+, -) with left-associativity.
    Calls _parse_multiplicative_expr for operands.
    Modifies parser_state["pos"] in place.
    """
    left = _parse_multiplicative_expr(parser_state)
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        token = tokens[pos]
        if token["type"] == "OPERATOR" and token["value"] in ["+", "-"]:
            parser_state["pos"] = pos + 1
            op_token = token
            right = _parse_multiplicative_expr(parser_state)
            left = {
                "type": "BINARY_OP",
                "operator": op_token["value"],
                "children": [left, right],
                "line": op_token["line"],
                "column": op_token["column"]
            }
            pos = parser_state["pos"]
        else:
            break
    
    return left

# === helper functions ===
# No helper functions needed - logic is contained in main function

# === OOP compatibility layer ===
# Not needed for parser function nodes