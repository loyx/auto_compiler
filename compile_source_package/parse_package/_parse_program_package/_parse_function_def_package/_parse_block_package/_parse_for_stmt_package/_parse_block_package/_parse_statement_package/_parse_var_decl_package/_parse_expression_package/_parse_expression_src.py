# === std / third-party imports ===
from typing import Any, Dict, Optional

# === sub function imports ===
from ._parse_assignment_package._parse_assignment_src import _parse_assignment

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, CALL)
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
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse expression with operator precedence. Entry point for expression parsing."""
    return _parse_assignment(parser_state)

# === helper functions ===
def _current_token(parser_state: ParserState) -> Optional[Token]:
    """Get current token at parser_state['pos']."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    return tokens[pos] if pos < len(tokens) else None

def _consume(parser_state: ParserState) -> Token:
    """Consume current token and advance pos."""
    token = _current_token(parser_state)
    if token is None:
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    parser_state["pos"] += 1
    return token

def _expect(parser_state: ParserState, token_type: str, value: Optional[str] = None) -> Token:
    """Expect specific token type/value, consume and return it."""
    token = _current_token(parser_state)
    if token is None:
        raise SyntaxError(f"Expected {token_type} but got EOF in {parser_state.get('filename', 'unknown')}")
    if token["type"] != token_type or (value is not None and token["value"] != value):
        raise SyntaxError(f"Expected {token_type}{' ' + value if value else ''} but got {token['type']} {token['value']} at line {token['line']}")
    return _consume(parser_state)

# === OOP compatibility layer ===
# Not needed - this is a helper function node
