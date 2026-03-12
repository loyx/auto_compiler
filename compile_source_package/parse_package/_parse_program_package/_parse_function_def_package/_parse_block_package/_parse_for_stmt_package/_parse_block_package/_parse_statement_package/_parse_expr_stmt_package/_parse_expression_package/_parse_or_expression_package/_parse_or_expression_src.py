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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_or_expression(parser_state: ParserState) -> AST:
    """
    解析逻辑或表达式（最低优先级）。
    处理 || 运算符，使用左递归消除后的循环结构。
    """
    left = _parse_and_expression(parser_state)
    
    while _is_or_operator(parser_state):
        op_token = _current_token(parser_state)
        line = op_token.get("line", 0)
        column = op_token.get("column", 0)
        parser_state["pos"] += 1
        right = _parse_and_expression(parser_state)
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": "||",
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前 token，越界时返回空 token。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos < len(tokens):
        return tokens[pos]
    return {"type": "EOF", "value": "", "line": 0, "column": 0}

def _is_or_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 || 运算符。"""
    token = _current_token(parser_state)
    return token.get("type") == "OPERATOR" and token.get("value") == "||"

# === OOP compatibility layer ===
