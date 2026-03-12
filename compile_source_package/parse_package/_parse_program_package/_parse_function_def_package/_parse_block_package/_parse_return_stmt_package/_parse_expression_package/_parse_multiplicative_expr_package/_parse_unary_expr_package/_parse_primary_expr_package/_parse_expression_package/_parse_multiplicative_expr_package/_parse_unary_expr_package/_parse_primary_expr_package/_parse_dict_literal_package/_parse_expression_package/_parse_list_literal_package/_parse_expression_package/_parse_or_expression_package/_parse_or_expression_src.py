# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expression_package._parse_and_expression_src import _parse_and_expression

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_or_expression(parser_state: ParserState) -> AST:
    """
    解析 or 表达式（优先级最低的二元运算符）。
    支持左结合：a or b or c → BinaryOp(OR, BinaryOp(OR, a, b), c)
    """
    left = _parse_and_expression(parser_state)
    
    while _is_current_token_or(parser_state):
        or_token = _consume_current_token(parser_state)
        right = _parse_and_expression(parser_state)
        
        left = {
            "type": "BinaryOp",
            "children": [left, right],
            "value": "or",
            "line": or_token.get("line", 0),
            "column": or_token.get("column", 0)
        }
    
    return left

# === helper functions ===
def _is_current_token_or(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 OR 运算符。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    return current_token.get("type") == "OR"

def _consume_current_token(parser_state: ParserState) -> Token:
    """消耗当前 token 并推进 pos。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
