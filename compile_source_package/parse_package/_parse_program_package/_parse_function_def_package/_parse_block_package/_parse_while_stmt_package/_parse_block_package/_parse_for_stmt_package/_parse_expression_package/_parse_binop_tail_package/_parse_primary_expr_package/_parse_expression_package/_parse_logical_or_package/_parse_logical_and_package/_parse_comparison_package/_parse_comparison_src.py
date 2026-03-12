# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive

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
def _parse_comparison(parser_state: ParserState) -> AST:
    """Parse comparison expressions (<, >, <=, >=, ==, !=)."""
    left = _parse_additive(parser_state)
    
    if parser_state.get("error"):
        return left
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return left
    
    current_token = tokens[pos]
    comparison_ops = {"LT", "GT", "LTE", "GTE", "EQ", "NEQ"}
    
    if current_token.get("type") not in comparison_ops:
        return left
    
    op = current_token.get("value")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    parser_state["pos"] = pos + 1
    
    right = _parse_additive(parser_state)
    
    if parser_state.get("error"):
        return {
            "type": "ERROR",
            "value": parser_state["error"],
            "line": line,
            "column": column
        }
    
    return {
        "type": "BINARY_OP",
        "operator": op,
        "children": [left, right],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
