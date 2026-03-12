# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

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
#   "type": str,             # BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, CALL_EXPR 等
#   "children": list,        # 子节点列表（如操作数）
#   "value": Any,            # 节点值（如运算符、字面量值）
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
    解析表达式。支持运算符优先级和括号。
    
    语法（按优先级从低到高）：
    - 逻辑或：||
    - 逻辑与：&&
    - 相等：==, !=
    - 关系：<, >, <=, >=
    - 加减：+, -
    - 乘除：*, /
    - 一元：-, !
    - 调用：identifier(...)
    - 原子：IDENTIFIER, LITERAL, ( expression )
    """
    # 解析左操作数（原子表达式）
    left = _parse_primary(parser_state)
    
    # 解析二元运算符（最小优先级为 0）
    result = _parse_binary_op(parser_state, 0, left)
    
    return result

# === helper functions ===
# No helper functions in this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node
