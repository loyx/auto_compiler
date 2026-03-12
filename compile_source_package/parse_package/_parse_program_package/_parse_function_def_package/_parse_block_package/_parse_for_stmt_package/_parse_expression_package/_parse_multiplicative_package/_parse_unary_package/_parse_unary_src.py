# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_atom_package._parse_atom_src import _parse_atom

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
def _parse_unary(parser_state: ParserState) -> AST:
    """Parse unary expression (prefix operators or atom)."""
    token = _current_token(parser_state)
    if token is None:
        parser_state['error'] = "Unexpected end of input"
        return {"type": "ERROR", "value": "unexpected_eof", "children": [], "line": 0, "column": 0}
    
    if token.get("type") in ("MINUS", "PLUS", "NOT", "BITWISE_NOT"):
        op_token = token
        op_string = _token_to_unary_op(op_token)
        _consume_token(parser_state)
        operand = _parse_unary(parser_state)
        return {
            "type": "UNARY_OP",
            "value": op_string,
            "children": [operand],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    else:
        return _parse_atom(parser_state)

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """Get current token at parser_state['pos'], or None if out of bounds."""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos >= len(tokens):
        return None
    return tokens[pos]

def _consume_token(parser_state: ParserState) -> None:
    """Advance parser_state['pos'] by one."""
    parser_state["pos"] = parser_state.get("pos", 0) + 1

def _token_to_unary_op(token: Token) -> str:
    """Convert token type to operator string."""
    op_map = {
        "MINUS": "-",
        "PLUS": "+",
        "NOT": "not",
        "BITWISE_NOT": "~"
    }
    return op_map.get(token.get("type", ""), "?")

# === OOP compatibility layer ===
