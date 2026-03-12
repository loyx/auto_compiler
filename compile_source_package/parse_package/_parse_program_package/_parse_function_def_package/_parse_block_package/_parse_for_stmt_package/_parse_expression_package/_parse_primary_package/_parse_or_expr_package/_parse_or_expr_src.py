# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

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
def _parse_or_expr(parser_state: ParserState) -> AST:
    """Parse OR expression (lowest precedence)."""
    left = _parse_and_expr(parser_state)
    
    while True:
        token = _get_current_token(parser_state)
        if token is None or token.get("type") != "OR":
            break
        
        _consume_token(parser_state)
        right = _parse_and_expr(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": "or",
            "children": [left, right],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    return left

# === helper functions ===
def _get_current_token(parser_state: ParserState) -> Token:
    """Get current token without consuming it."""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos < len(tokens):
        return tokens[pos]
    return None

def _consume_token(parser_state: ParserState) -> None:
    """Advance parser position by one token."""
    parser_state["pos"] = parser_state.get("pos", 0) + 1

# === OOP compatibility layer ===
