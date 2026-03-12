# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_assignment_package._parse_assignment_src import _parse_assignment

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
#   "operator": str,
#   "callee": dict,
#   "args": list
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
    """
    解析表达式（处理运算符优先级）。
    输入：parser_state（pos 指向表达式起始 token）。
    输出：expression AST 节点。
    副作用：消费表达式相关 token，更新 pos。
    解析失败则抛出 SyntaxError。
    """
    return _parse_assignment(parser_state)

# === helper functions ===
# 无 helper 函数，所有逻辑已委托给子函数

# === OOP compatibility layer ===
# 不需要 OOP wrapper