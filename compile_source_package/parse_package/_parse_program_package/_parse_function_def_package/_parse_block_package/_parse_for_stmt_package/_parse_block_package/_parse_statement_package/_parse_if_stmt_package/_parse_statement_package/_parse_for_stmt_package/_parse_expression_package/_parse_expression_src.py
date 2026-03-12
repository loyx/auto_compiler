# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expression_package._parse_or_expression_src import _parse_or_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": str,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """
    解析表达式的入口函数。
    调用最低优先级的解析函数，逐步构建 AST。
    """
    ast_node = _parse_or_expression(parser_state)
    return ast_node

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前 token，若越界则返回 EOF token。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    if pos >= len(tokens):
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    return tokens[pos]

def _advance(parser_state: ParserState) -> Token:
    """前进到下一个 token 并返回当前 token。"""
    token = _current_token(parser_state)
    parser_state["pos"] = parser_state.get("pos", 0) + 1
    return token

def _match(parser_state: ParserState, *token_types: str) -> bool:
    """检查当前 token 是否匹配给定类型之一。"""
    current = _current_token(parser_state)
    return current.get("type") in token_types

def _expect(parser_state: ParserState, token_type: str) -> Token:
    """期望当前 token 为指定类型，否则抛出 SyntaxError。"""
    current = _current_token(parser_state)
    if current.get("type") != token_type:
        raise SyntaxError(
            f"Expected {token_type}, got {current.get('type')} "
            f"at line {current.get('line')}, column {current.get('column')}"
        )
    return _advance(parser_state)

# === OOP compatibility layer ===
