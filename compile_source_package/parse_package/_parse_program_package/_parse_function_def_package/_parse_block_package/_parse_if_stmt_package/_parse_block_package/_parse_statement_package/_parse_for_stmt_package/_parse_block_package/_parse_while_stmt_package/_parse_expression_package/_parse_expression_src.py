# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_binary_package._parse_binary_src import _parse_binary
from ._get_token_package._get_token_src import _get_token
from ._error_package._error_src import _error

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
    """
    解析表达式。
    输入：parser_state（pos 指向表达式起始 token）。
    输出：表达式 AST 节点。
    副作用：修改 parser_state["pos"] 指向表达式结束后的下一个 token。
    """
    # 先检查是否有 token
    token = _get_token(parser_state)
    if token is None:
        _error(parser_state, "Unexpected end of expression")
    
    # 使用优先级爬升算法解析表达式
    # 从最低优先级开始解析二元表达式
    result = _parse_binary(parser_state, 0)
    return result

# === helper functions ===
# Helper functions are delegated to sub-modules

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
