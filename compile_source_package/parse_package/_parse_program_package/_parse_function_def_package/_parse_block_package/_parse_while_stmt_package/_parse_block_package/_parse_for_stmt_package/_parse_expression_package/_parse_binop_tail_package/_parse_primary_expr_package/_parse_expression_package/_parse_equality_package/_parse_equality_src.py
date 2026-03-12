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
def _parse_equality(parser_state: ParserState) -> AST:
    """Parse equality expressions (==, !=) with left associativity."""
    left = _parse_comparison(parser_state)
    
    if parser_state.get("error"):
        return left
    
    tokens = parser_state["tokens"]
    
    while parser_state["pos"] < len(tokens):
        token = tokens[parser_state["pos"]]
        if token["type"] not in ("EQEQ", "NEQ"):
            break
        
        op = token["value"]
        op_line = token["line"]
        op_column = token["column"]
        
        parser_state["pos"] += 1
        
        right = _parse_comparison(parser_state)
        
        if parser_state.get("error"):
            return {"type": "ERROR", "value": parser_state["error"]}
        
        left = {
            "type": "BINARY_OP",
            "operator": op,
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function