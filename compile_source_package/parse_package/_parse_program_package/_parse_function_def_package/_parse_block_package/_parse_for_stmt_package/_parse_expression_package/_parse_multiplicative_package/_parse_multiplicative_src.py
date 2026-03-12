# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary

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
def _parse_multiplicative(parser_state: ParserState) -> AST:
    """Parse multiplicative expression (*, /, %).
    
    Grammar: unary_expr (mul_op unary_expr)*
    Mul ops: STAR (*), SLASH (/), PERCENT (%)
    Left-associative, builds BINARY_OP AST nodes.
    """
    left = _parse_unary(parser_state)
    
    while _is_multiplicative_op(parser_state):
        op_token = _current_token(parser_state)
        op_string = _token_to_op(op_token)
        line = left.get("line", op_token.get("line", 0))
        column = left.get("column", op_token.get("column", 0))
        
        _consume_token(parser_state)
        right = _parse_unary(parser_state)
        
        left = {
            "type": "BINARY_OP",
            "value": op_string,
            "children": [left, right],
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _is_multiplicative_op(parser_state: ParserState) -> bool:
    """Check if current token is a multiplicative operator."""
    token = _current_token(parser_state)
    if token is None:
        return False
    return token.get("type") in ("STAR", "SLASH", "PERCENT")

def _current_token(parser_state: ParserState) -> Token:
    """Get current token without consuming."""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos < len(tokens):
        return tokens[pos]
    return None

def _consume_token(parser_state: ParserState) -> None:
    """Advance parser position by one token."""
    parser_state["pos"] = parser_state.get("pos", 0) + 1

def _token_to_op(token: Token) -> str:
    """Convert token type to operator string."""
    type_map = {
        "STAR": "*",
        "SLASH": "/",
        "PERCENT": "%"
    }
    return type_map.get(token.get("type"), token.get("value", ""))

# === OOP compatibility layer ===
