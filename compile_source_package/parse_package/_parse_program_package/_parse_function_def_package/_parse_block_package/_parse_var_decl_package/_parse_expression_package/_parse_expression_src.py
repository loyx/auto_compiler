# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_binary_package._parse_binary_src import _parse_binary

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
def _parse_expression(parser_state: dict) -> dict:
    """解析表达式为 AST 节点。
    
    处理一元运算符、二元运算符（带优先级）、括号表达式。
    入口函数，委托给 _parse_binary 进行实际解析。
    """
    return _parse_binary(parser_state, 0)

# === helper functions ===
# No helper functions in this file - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for parser function node