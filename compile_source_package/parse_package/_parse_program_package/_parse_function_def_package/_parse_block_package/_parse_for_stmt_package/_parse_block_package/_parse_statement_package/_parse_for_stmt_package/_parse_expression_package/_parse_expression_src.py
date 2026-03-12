# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expr_package._parse_or_expr_src import _parse_or_expr
from ._get_current_position_package._get_current_position_src import _get_current_position

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (NUMBER, STRING, TRUE, FALSE, IDENTIFIER, OPERATOR, LPAREN, RPAREN, KEYWORD)
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
def _parse_expression(parser_state: ParserState) -> AST:
    """解析任意表达式，返回 AST 节点。"""
    start_line, start_col = _get_current_position(parser_state)
    result = _parse_or_expr(parser_state)
    result["line"] = start_line
    result["column"] = start_col
    return result

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node