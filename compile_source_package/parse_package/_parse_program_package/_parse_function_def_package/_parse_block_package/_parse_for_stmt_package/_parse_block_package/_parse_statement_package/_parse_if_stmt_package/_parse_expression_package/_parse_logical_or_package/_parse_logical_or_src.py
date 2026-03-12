# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_and_package._parse_logical_and_src import _parse_logical_and
from ._expect_token_package._expect_token_src import _expect_token

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (PLUS, MINUS, STAR, SLASH, PERCENT, EQ, NE, LT, GT, LE, GE, AND, OR, BANG, IDENTIFIER, INTEGER, STRING, LPAREN, RPAREN)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL)
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
def _parse_logical_or(parser_state: dict) -> dict:
    """解析逻辑 OR 表达式（|| 运算符），左结合。"""
    left = _parse_logical_and(parser_state)
    
    while _current_token_type(parser_state) == "OR":
        or_token = _expect_token(parser_state, "OR")
        right = _parse_logical_and(parser_state)
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": "||",
            "line": left["line"],
            "column": left["column"]
        }
    
    return left

# === helper functions ===
def _current_token_type(parser_state: ParserState) -> str:
    """获取当前 token 的类型，若无 token 则返回空字符串。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]["type"]
    return ""

# === OOP compatibility layer ===
