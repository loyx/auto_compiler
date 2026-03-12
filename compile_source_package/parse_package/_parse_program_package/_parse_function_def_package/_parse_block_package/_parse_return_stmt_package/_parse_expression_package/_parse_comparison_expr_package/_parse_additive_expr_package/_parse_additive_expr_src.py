# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """Parse additive expression with left associativity (handles +, - operators)."""
    left = _parse_multiplicative_expr(parser_state)
    
    while _is_additive_operator(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_multiplicative_expr(parser_state)
        left = _build_binary_op(left, right, op_token)
    
    return left

# === helper functions ===
def _is_additive_operator(parser_state: ParserState) -> bool:
    """Check if current token is additive operator (+ or -)."""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos >= len(tokens):
        return False
    token_type = tokens[pos].get("type", "")
    return token_type in ("PLUS", "MINUS")

def _consume_token(parser_state: ParserState) -> Token:
    """Consume and return current token, advancing position."""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

def _build_binary_op(left: AST, right: AST, op_token: Token) -> AST:
    """Build BINARY_OP AST node from operands and operator token."""
    return {
        "type": "BINARY_OP",
        "value": op_token.get("value"),
        "children": [left, right],
        "line": op_token.get("line"),
        "column": op_token.get("column")
    }

# === OOP compatibility layer ===
# Not required for parser function nodes
