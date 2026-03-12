# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_binary_package._parse_binary_src import _parse_binary

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
#   "type": str,             # BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL 等
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
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
    解析表达式。
    输入 parser_state（pos 指向表达式起始 token），返回表达式 AST 节点。
    副作用：更新 pos 到表达式结束。
    异常：语法错误抛出 SyntaxError。
    """
    ast_node = _parse_binary(parser_state, 0)
    return ast_node

# === helper functions ===

# === OOP compatibility layer ===
