# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_or_package._parse_logical_or_src import _parse_logical_or

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
def _parse_expression(parser_state: dict) -> dict:
    """
    Parse expression entry point.
    Delegates to _parse_logical_or (lowest precedence).
    Input: parser_state with pos at expression start.
    Output: AST node for the expression.
    Side effect: updates parser_state['pos'] to expression end.
    """
    return _parse_logical_or(parser_state)

# === helper functions ===
# No helper functions in this file - all logic delegated to subfunctions

# === OOP compatibility layer ===
# Not required for parser function nodes