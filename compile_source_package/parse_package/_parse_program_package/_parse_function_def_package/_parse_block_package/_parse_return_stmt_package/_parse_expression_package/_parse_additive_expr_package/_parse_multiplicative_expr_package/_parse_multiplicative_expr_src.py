# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """Parse multiplicative expression (*, /, % operators, left-associative)."""
    left = _parse_unary_expr(parser_state)
    
    while _is_multiplicative_token(parser_state):
        op_token = _consume_current_token(parser_state)
        operator_str = _token_to_operator(op_token)
        right = _parse_unary_expr(parser_state)
        left = _build_binary_op_node(left, right, operator_str, op_token)
    
    return left

# === helper functions ===
def _is_multiplicative_token(parser_state: ParserState) -> bool:
    """Check if current token is STAR, SLASH, or PERCENT."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return False
    token_type = tokens[pos].get("type", "")
    return token_type in ("STAR", "SLASH", "PERCENT")

def _consume_current_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing position."""
    token = parser_state["tokens"][parser_state["pos"]]
    parser_state["pos"] += 1
    return token

def _token_to_operator(token: Token) -> str:
    """Convert token type to operator string."""
    type_map = {
        "STAR": "*",
        "SLASH": "/",
        "PERCENT": "%"
    }
    return type_map.get(token["type"], token["type"])

def _build_binary_op_node(left: AST, right: AST, operator: str, token: Token) -> AST:
    """Build a BINARY_OP AST node."""
    return {
        "type": "BINARY_OP",
        "value": operator,
        "children": [left, right],
        "line": token.get("line", 0),
        "column": token.get("column", 0)
    }

# === OOP compatibility layer ===
