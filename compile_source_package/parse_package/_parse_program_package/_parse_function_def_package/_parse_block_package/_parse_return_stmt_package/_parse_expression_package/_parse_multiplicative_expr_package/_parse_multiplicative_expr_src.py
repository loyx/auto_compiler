# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from _parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """
    解析乘法表达式（处理 *, / 运算符，左结合）。
    """
    left = _parse_unary_expr(parser_state)
    
    while _is_multiplicative_operator(parser_state):
        op_token = _consume_current_token(parser_state)
        operator_str = op_token["value"]
        line = op_token["line"]
        column = op_token["column"]
        
        right = _parse_unary_expr(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": operator_str,
            "children": [left, right],
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _is_multiplicative_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为乘法运算符 (*, /)。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    return current_token["type"] in ("STAR", "SLASH")

def _consume_current_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，同时推进 pos。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===
# Not required for this parser function node
