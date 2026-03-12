# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expression_package._parse_or_expression_src import _parse_or_expression

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
#   "type": str,             # 节点类型
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
def _parse_expression(parser_state: dict) -> dict:
    """解析表达式入口，处理运算符优先级和各类表达式项。"""
    return _parse_or_expression(parser_state)

# === helper functions ===
# Helper functions are delegated to sub-modules

# === OOP compatibility layer ===
# Not needed for parser function
