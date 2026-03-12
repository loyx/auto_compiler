# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary

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
def _parse_multiplicative(parser_state: ParserState) -> AST:
    """
    解析乘法/除法表达式（*, /, %）。
    优先级高于加减运算符但低于一元运算符。
    左结合性。
    """
    left = _parse_unary(parser_state)
    
    if parser_state.get("error"):
        return left
    
    while True:
        current_token = _get_current_token(parser_state)
        if current_token is None:
            break
        
        op_type = current_token.get("type")
        if op_type not in ("STAR", "SLASH", "PERCENT"):
            break
        
        operator = current_token.get("value")
        line = current_token.get("line")
        column = current_token.get("column")
        
        parser_state["pos"] += 1
        
        right = _parse_unary(parser_state)
        
        if parser_state.get("error"):
            return right
        
        left = {
            "type": "BINARY_OP",
            "operator": operator,
            "children": [left, right],
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，如果越界则返回 None。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        return None
    
    return tokens[pos]

# === OOP compatibility layer ===
