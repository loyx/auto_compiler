# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._parse_additive_package._parse_additive_src import _parse_additive

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
def _parse_comparison(parser_state: ParserState) -> AST:
    """Parse comparison expressions with operators ==, !=, <, >, <=, >=."""
    left = _parse_additive(parser_state)
    
    comparison_ops = {"==", "!=", "<", ">", "<=", ">="}
    
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        if token["value"] not in comparison_ops:
            break
        
        op = token["value"]
        line = token["line"]
        column = token["column"]
        parser_state["pos"] += 1
        
        right = _parse_additive(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function