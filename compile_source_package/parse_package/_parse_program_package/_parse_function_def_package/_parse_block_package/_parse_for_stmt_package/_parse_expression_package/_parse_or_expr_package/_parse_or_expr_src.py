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
    """
    Parse 'or' expression (lowest precedence).
    Grammar: and_expr ('or' and_expr)*
    """
    # Parse first and_expr as left operand
    left = _parse_and_expr(parser_state)
    
    # Loop while current token is "OR"
    while _current_token_is_or(parser_state):
        # Record position for the operator
        op_line = left.get("line", 0)
        op_column = left.get("column", 0)
        
        # Consume the OR token
        _consume_token(parser_state)
        
        # Parse right operand
        right = _parse_and_expr(parser_state)
        
        # Build BINARY_OP node with left-associativity
        left = {
            "type": "BINARY_OP",
            "value": "or",
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
def _current_token_is_or(parser_state: ParserState) -> bool:
    """Check if current token is OR keyword."""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token.get("type") == "OR"

def _consume_token(parser_state: ParserState) -> None:
    """Advance parser position by one token."""
    parser_state["pos"] = parser_state.get("pos", 0) + 1

# === OOP compatibility layer ===
# Not needed for this parser function node
