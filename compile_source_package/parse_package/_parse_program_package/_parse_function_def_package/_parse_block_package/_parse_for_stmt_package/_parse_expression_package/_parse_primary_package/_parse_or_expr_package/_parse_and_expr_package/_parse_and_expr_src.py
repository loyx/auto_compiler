# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_not_expr_package._parse_not_expr_src import _parse_not_expr

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """Parse AND logical expression (medium precedence)."""
    left = _parse_not_expr(parser_state)
    
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        if token.get("value") == "AND":
            and_token = token
            parser_state["pos"] += 1
            right = _parse_not_expr(parser_state)
            left = {
                "type": "BINARY_OP",
                "value": "and",
                "children": [left, right],
                "line": and_token["line"],
                "column": and_token["column"]
            }
        else:
            break
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function