# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """解析单个表达式。"""
    token = _peek_token(parser_state)
    if token is None:
        raise SyntaxError("Unexpected end of input")
    
    # 解析初级表达式（字面量、标识符、括号表达式）
    left = _parse_primary(parser_state)
    
    # 检查是否有二元运算符
    op_token = _peek_token(parser_state)
    if op_token is not None and op_token.get("type") in ("PLUS", "MINUS", "STAR", "SLASH", "EQ", "NE", "LT", "GT", "LE", "GE"):
        return _parse_binary_op(parser_state, left)
    
    return left

# === helper functions ===
# Helper functions are delegated to sub-modules

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
