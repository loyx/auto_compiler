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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    表达式解析主入口。
    调用最低优先级的 _parse_or 开始递归下降解析。
    """
    return _parse_or(parser_state)

# === helper functions ===
# 无 helper 函数，所有逻辑委托给子函数

# === OOP compatibility layer ===
# 不需要 OOP wrapper
