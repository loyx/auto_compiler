# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expr_package._parse_or_expr_src import _parse_or_expr

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
    """
    Parse expression entry point.
    Delegates to _parse_or_expr (lowest precedence level).
    Input: parser_state with pos at expression start token.
    Output: AST node for the expression.
    Updates parser_state["pos"] past the expression.
    """
    return _parse_or_expr(parser_state)

# === helper functions ===
# No helper functions in this file; logic delegated to sub-functions.

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes.
