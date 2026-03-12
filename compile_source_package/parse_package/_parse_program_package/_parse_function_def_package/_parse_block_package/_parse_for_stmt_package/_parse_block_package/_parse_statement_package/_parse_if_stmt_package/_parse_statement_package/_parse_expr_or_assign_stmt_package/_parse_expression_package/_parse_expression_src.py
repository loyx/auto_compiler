# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_or_package._parse_logical_or_src import _parse_logical_or

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
def _parse_expression(parser_state: dict) -> dict:
    """Parse expression with operator precedence. Entry point delegates to lowest precedence level."""
    return _parse_logical_or(parser_state)

# === helper functions ===
def _current_token(parser_state: dict) -> dict:
    """Get current token or return None if at end."""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos < len(tokens):
        return tokens[pos]
    return None

def _advance(parser_state: dict) -> dict:
    """Advance position and return consumed token."""
    token = _current_token(parser_state)
    parser_state["pos"] = parser_state.get("pos", 0) + 1
    return token

def _expect(parser_state: dict, token_type: str, value: str = None) -> dict:
    """Expect specific token, advance if matches, else raise SyntaxError."""
    token = _current_token(parser_state)
    if token is None:
        raise SyntaxError(f"Unexpected end of input, expected {token_type}")
    if token.get("type") != token_type:
        raise SyntaxError(f"Expected {token_type}, got {token.get('type')}")
    if value is not None and token.get("value") != value:
        raise SyntaxError(f"Expected '{value}', got '{token.get('value')}'")
    return _advance(parser_state)

# === OOP compatibility layer ===
