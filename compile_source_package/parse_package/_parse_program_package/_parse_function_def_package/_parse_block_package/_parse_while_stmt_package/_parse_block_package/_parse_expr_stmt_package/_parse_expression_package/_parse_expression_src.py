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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """解析表达式，返回表达式 AST 节点。
    
    输入：parser_state（当前位置指向表达式第一个 token）
    处理：原地修改 parser_state["pos"] 消费表达式 token
    输出：表达式 AST 节点（LITERAL、IDENTIFIER、UNARY_OP、BINARY_OP 等）
    异常：表达式语法错误时 raise SyntaxError
    """
    return _parse_or(parser_state)

# === helper functions ===
# 无 helper 函数，所有逻辑已委托给子函数

# === OOP compatibility layer ===
# 不需要 OOP wrapper，这是内部解析函数
