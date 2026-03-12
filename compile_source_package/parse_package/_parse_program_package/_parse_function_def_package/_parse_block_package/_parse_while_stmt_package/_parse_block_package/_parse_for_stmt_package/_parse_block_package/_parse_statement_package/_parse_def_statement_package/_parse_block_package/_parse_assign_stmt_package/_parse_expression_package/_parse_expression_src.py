# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_package._parse_or_src import _parse_or

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": AST,
#   "args": list,
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
def _parse_expression(parser_state: ParserState) -> AST:
    """解析表达式入口函数。调用 _parse_or 处理最低优先级，递归下降解析整个表达式。"""
    return _parse_or(parser_state)


# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，若越界则返回 EOF token。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    return {"type": "EOF", "value": "", "line": -1, "column": -1}


# === OOP compatibility layer ===
