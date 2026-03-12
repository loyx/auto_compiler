# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_not_expr_package._parse_not_expr_src import _parse_not_expr
from ._current_token_package._current_token_src import _current_token
from ._advance_package._advance_src import _advance

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """解析 and 表达式（比 or 高一级优先级）。"""
    left = _parse_not_expr(parser_state)
    
    while True:
        token = _current_token(parser_state)
        if token.get("type") != "AND":
            break
        
        _advance(parser_state)
        right = _parse_not_expr(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": "and",
            "children": [left, right],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===
