# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative

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
def _parse_additive(parser_state: ParserState) -> AST:
    """
    解析加法/减法表达式（+、- 运算符）。
    优先级高于比较表达式，低于乘除表达式。
    左结合：((a + b) + c)
    """
    left = _parse_multiplicative(parser_state)
    
    while parser_state["pos"] < len(parser_state["tokens"]):
        current_token = parser_state["tokens"][parser_state["pos"]]
        
        if current_token["type"] in ("PLUS", "MINUS"):
            op_token = current_token
            parser_state["pos"] += 1
            
            right = _parse_multiplicative(parser_state)
            
            left = {
                "type": "BINARY_OP",
                "value": op_token["value"],
                "children": [left, right],
                "line": op_token["line"],
                "column": op_token["column"]
            }
        else:
            break
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
