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
    """解析比较表达式（==, !=, <, >, <=, >=）。"""
    COMPARISON_OPS = {"==", "!=", "<", ">", "<=", ">="}
    
    left = _parse_additive(parser_state)
    
    while True:
        pos = parser_state["pos"]
        tokens = parser_state["tokens"]
        
        if pos >= len(tokens):
            break
        
        token = tokens[pos]
        if token.get("type") != "OPERATOR" or token.get("value") not in COMPARISON_OPS:
            break
        
        op_token = tokens[pos]
        parser_state["pos"] = pos + 1
        
        right = _parse_additive(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_token["value"],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
