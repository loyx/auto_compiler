# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_and_package._parse_logical_and_src import _parse_logical_and

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
def _parse_logical_or(parser_state: ParserState) -> AST:
    """
    解析逻辑 OR 表达式（|| 运算符）。
    这是运算符优先级链的最底层入口。
    """
    left = _parse_logical_and(parser_state)
    
    while _is_logical_or_token(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_logical_and(parser_state)
        left = _build_binary_op(op_token, left, right)
    
    return left

# === helper functions ===
def _is_logical_or_token(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 || 运算符。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "OPERATOR" and token.get("value") == "||"

def _consume_token(parser_state: ParserState) -> Token:
    """消耗当前 token 并前进位置。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

def _build_binary_op(op_token: Token, left: AST, right: AST) -> AST:
    """构建二元操作符 AST 节点。"""
    return {
        "type": "BINARY_OP",
        "value": op_token["value"],
        "children": [left, right],
        "line": op_token.get("line", 0),
        "column": op_token.get("column", 0)
    }

# === OOP compatibility layer ===
