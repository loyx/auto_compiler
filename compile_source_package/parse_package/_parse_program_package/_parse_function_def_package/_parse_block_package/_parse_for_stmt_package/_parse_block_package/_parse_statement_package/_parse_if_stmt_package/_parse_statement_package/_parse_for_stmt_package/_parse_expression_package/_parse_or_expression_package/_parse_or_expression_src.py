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
#   "value": str,
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
def _parse_or_expression(parser_state: dict) -> dict:
    """
    解析逻辑 OR 表达式（|| 运算符，最低优先级）。
    使用左递归消除后的迭代方式解析。
    """
    left = _parse_and_expression(parser_state)
    
    while _is_or_operator(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_and_expression(parser_state)
        
        left = {
            "type": "BINARY_EXPR",
            "operator": "||",
            "left": left,
            "right": right,
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left

# === helper functions ===
def _is_or_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 OR 运算符（||）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        return False
    
    token = tokens[pos]
    return token.get("type") == "OPERATOR" and token.get("value") == "||"

def _consume_token(parser_state: ParserState) -> Token:
    """消耗当前 token 并返回，同时更新 pos。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
# Not needed for this parser function node
