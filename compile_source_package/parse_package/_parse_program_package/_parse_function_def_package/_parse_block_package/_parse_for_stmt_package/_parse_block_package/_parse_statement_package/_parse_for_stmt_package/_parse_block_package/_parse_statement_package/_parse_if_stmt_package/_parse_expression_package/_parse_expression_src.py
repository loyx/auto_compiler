# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_or_package._parse_logical_or_src import _parse_logical_or

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
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": str,
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
def _parse_expression(parser_state: dict) -> dict:
    """
    解析表达式入口函数。
    从当前位置开始解析完整表达式，支持所有运算符优先级。
    原地更新 parser_state["pos"] 到表达式结束位置。
    """
    return _parse_logical_or(parser_state)

# === helper functions ===
# No helper functions in this file - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function