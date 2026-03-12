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
#   "left": Any,
#   "right": Any,
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
    """解析比较表达式 (<, >, <=, >=)。"""
    left = _parse_additive(parser_state)
    
    if parser_state.get("error"):
        return left
    
    comparison_ops = {"LT", "GT", "LTE", "GTE"}
    
    while parser_state["pos"] < len(parser_state["tokens"]):
        token = parser_state["tokens"][parser_state["pos"]]
        
        if token["type"] not in comparison_ops:
            break
        
        op_token = token
        parser_state["pos"] += 1
        
        right = _parse_additive(parser_state)
        
        if parser_state.get("error"):
            return {"type": "ERROR", "value": parser_state["error"]}
        
        left = {
            "type": "BINARY_OP",
            "operator": op_token["value"],
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
