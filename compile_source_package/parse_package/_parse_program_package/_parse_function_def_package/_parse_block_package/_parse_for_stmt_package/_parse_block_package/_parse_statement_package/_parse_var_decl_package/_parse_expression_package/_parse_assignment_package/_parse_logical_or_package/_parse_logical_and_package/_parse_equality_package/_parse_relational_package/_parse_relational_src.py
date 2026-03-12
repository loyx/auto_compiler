# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive
from ._current_token_package._current_token_src import _current_token
from ._consume_package._consume_src import _consume

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, CALL, BLOCK)
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
def _parse_relational(parser_state: ParserState) -> AST:
    """解析关系表达式（<, >, <=, >= 运算符）。"""
    left = _parse_additive(parser_state)
    
    relational_ops = {"<", ">", "<=", ">="}
    
    while True:
        token = _current_token(parser_state)
        if token is None or token.get("value") not in relational_ops:
            break
        
        op_token = _consume(parser_state, "OPERATOR")
        right = _parse_additive(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": op_token.get("value"),
            "line": op_token.get("line"),
            "column": op_token.get("column")
        }
    
    return left

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes
