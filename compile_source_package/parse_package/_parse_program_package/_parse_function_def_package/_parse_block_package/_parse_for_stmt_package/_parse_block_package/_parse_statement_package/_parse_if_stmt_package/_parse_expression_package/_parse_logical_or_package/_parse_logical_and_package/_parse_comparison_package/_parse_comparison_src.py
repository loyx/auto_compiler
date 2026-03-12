# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive
from ._expect_token_package._expect_token_src import _expect_token

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
    """解析比较表达式（==, !=, <, >, <=, >= 运算符）。"""
    left = _parse_additive(parser_state)
    
    comparison_ops = ["EQ", "NE", "LT", "GT", "LE", "GE"]
    op_map = {
        "EQ": "==", "NE": "!=", "LT": "<",
        "GT": ">", "LE": "<=", "GE": ">="
    }
    
    while parser_state["pos"] < len(parser_state["tokens"]):
        current_token = parser_state["tokens"][parser_state["pos"]]
        if current_token["type"] not in comparison_ops:
            break
        
        op_token = _expect_token(parser_state, current_token["type"])
        right = _parse_additive(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": op_map[current_token["type"]],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
