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
    """Parse comparison expression (==, !=, <, >, <=, >=)."""
    left = _parse_additive(parser_state)
    
    comp_ops = {"EQ", "NE", "LT", "GT", "LE", "GE"}
    op_map = {
        "EQ": "==",
        "NE": "!=",
        "LT": "<",
        "GT": ">",
        "LE": "<=",
        "GE": ">="
    }
    
    while True:
        tokens = parser_state.get("tokens", [])
        pos = parser_state.get("pos", 0)
        
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        token_type = current_token.get("type", "")
        
        if token_type not in comp_ops:
            break
        
        op_string = op_map[token_type]
        parser_state["pos"] = pos + 1
        
        right = _parse_additive(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": op_string,
            "children": [left, right],
            "line": left.get("line", current_token.get("line", 0)),
            "column": left.get("column", current_token.get("column", 0))
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
