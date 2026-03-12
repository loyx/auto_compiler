# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_expr_package._parse_comparison_expr_src import _parse_comparison_expr

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
#   "value": Any,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """Parse && logical AND operators with left-associativity."""
    left = _parse_comparison_expr(parser_state)
    
    while (
        parser_state["pos"] < len(parser_state["tokens"])
        and parser_state["tokens"][parser_state["pos"]].get("type") == "OPERATOR"
        and parser_state["tokens"][parser_state["pos"]].get("value") == "&&"
    ):
        op_token = parser_state["tokens"][parser_state["pos"]]
        parser_state["pos"] += 1
        right = _parse_comparison_expr(parser_state)
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
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function