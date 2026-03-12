# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_relational_expression_package._parse_relational_expression_src import _parse_relational_expression

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
def _parse_equality_expression(parser_state: ParserState) -> AST:
    """Parse equality expression (== and != operators)."""
    left = _parse_relational_expression(parser_state)
    
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        if token["value"] in ("==", "!="):
            op_token = token
            parser_state["pos"] += 1
            right = _parse_relational_expression(parser_state)
            left = {
                "type": "BINARY_OP",
                "children": [left, right],
                "value": op_token["value"],
                "line": op_token["line"],
                "column": op_token["column"]
            }
        else:
            break
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
