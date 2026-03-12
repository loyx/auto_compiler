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
#   "line": int,
#   "column": int,
#   "value": Any,
#   "literal_type": str,
#   "name": str,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "callee": AST,
#   "arguments": list
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
def _parse_and(parser_state: ParserState) -> AST:
    """解析 AND 表达式（&& 运算符），左结合，优先级高于 OR 低于比较。"""
    left = _parse_comparison(parser_state)
    
    while _is_and_operator(parser_state):
        op_token = _advance(parser_state)
        right = _parse_comparison(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "operator": "&&",
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前 token，如果越界返回 None。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos < len(tokens):
        return tokens[pos]
    return None

def _advance(parser_state: ParserState) -> Token:
    """前进到下一个 token 并返回原 token。"""
    token = _current_token(parser_state)
    parser_state["pos"] = parser_state["pos"] + 1
    return token

def _is_and_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 && 运算符。"""
    token = _current_token(parser_state)
    if token is None:
        return False
    return token["type"] == "AND" and token["value"] == "&&"

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node