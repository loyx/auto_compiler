# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_or_package._parse_logical_or_src import _parse_logical_or
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
def _parse_assignment(parser_state: ParserState) -> AST:
    """Parse assignment expression (lowest precedence). Syntax: identifier = expression"""
    left = _parse_logical_or(parser_state)
    token = _current_token(parser_state)
    
    if token is not None and token["type"] == "OPERATOR" and token["value"] == "=":
        if left["type"] != "IDENTIFIER":
            raise SyntaxError(f"Invalid assignment target at line {left.get('line', '?')}")
        _consume(parser_state, "OPERATOR")
        right = _parse_assignment(parser_state)
        return {
            "type": "BINARY_OP",
            "value": "=",
            "children": [left, right],
            "line": left.get("line"),
            "column": left.get("column")
        }
    return left

# === helper functions ===

# === OOP compatibility layer ===
