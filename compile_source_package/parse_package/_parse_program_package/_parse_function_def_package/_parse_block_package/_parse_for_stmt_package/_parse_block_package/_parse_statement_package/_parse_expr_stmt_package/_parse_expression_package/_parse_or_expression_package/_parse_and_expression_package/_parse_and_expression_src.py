# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_expression_package._parse_equality_expression_src import _parse_equality_expression

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
def _parse_and_expression(parser_state: ParserState) -> AST:
    """Parse logical AND expression with && operator (left-associative)."""
    left = _parse_equality_expression(parser_state)
    
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        if token["type"] == "OPERATOR" and token["value"] == "&&":
            line = token["line"]
            column = token["column"]
            parser_state["pos"] += 1
            right = _parse_equality_expression(parser_state)
            left = {
                "type": "BINARY_OP",
                "children": [left, right],
                "value": "&&",
                "line": line,
                "column": column
            }
        else:
            break
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
