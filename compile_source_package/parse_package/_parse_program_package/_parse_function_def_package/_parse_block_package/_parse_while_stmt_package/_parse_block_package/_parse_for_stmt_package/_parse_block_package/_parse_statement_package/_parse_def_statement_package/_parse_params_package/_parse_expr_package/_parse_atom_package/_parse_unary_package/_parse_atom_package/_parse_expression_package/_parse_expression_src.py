# === std / third-party imports ===
from typing import Any, Dict, Optional

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
#   "line": int,
#   "column": int,
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST
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
    """解析完整表达式，支持运算符优先级和括号。"""
    return _parse_or(parser_state)

# === helper functions ===
def _current_token_type(parser_state: ParserState) -> Optional[str]:
    """获取当前 token 类型，若越界则返回 None。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]["type"]
    return None

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function
