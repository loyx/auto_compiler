# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._current_token_package._current_token_src import _current_token
from ._consume_token_package._consume_token_src import _consume_token

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
#   "value": Any,
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
def _parse_primary(parser_state: ParserState) -> AST:
    """
    解析原子表达式（primary expression）。
    原子表达式：字面量、标识符、括号表达式、一元运算符。
    副作用：更新 parser_state["pos"]。
    异常：语法错误时抛出 SyntaxError。
    """
    token = _current_token(parser_state)
    
    if token is None:
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}")
    
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    token_line = token.get("line", 0)
    token_column = token.get("column", 0)
    
    # 字面量
    if token_type in ("NUMBER", "STRING", "BOOLEAN", "NULL"):
        _consume_token(parser_state)
        return {"type": "LITERAL", "value": token_value, "line": token_line, "column": token_column, "children": []}
    
    # 标识符
    if token_type == "IDENTIFIER":
        _consume_token(parser_state)
        return {"type": "IDENTIFIER", "value": token_value, "line": token_line, "column": token_column, "children": []}
    
    # 括号表达式
    if token_type == "LPAREN":
        _consume_token(parser_state)
        closing = _current_token(parser_state)
        if closing is None or closing.get("type") != "RPAREN":
            raise SyntaxError(f"Expected ')' but got {closing} in {parser_state.get('filename', '<unknown>')}")
        _consume_token(parser_state)
        return {"type": "PAREN", "value": None, "line": token_line, "column": token_column, "children": []}
    
    # 一元运算符
    if token_type in ("MINUS", "NOT", "BITWISE_NOT"):
        _consume_token(parser_state)
        operand = _parse_primary(parser_state)
        return {"type": "UNARY_OP", "value": token_value, "operator": token_type, "line": token_line, "column": token_column, "children": [operand]}
    
    raise SyntaxError(f"Unexpected token '{token_value}' (type: {token_type}) at line {token_line}, column {token_column} in {parser_state.get('filename', '<unknown>')}")

# === helper functions ===
# Helpers delegated to child functions

# === OOP compatibility layer ===
# Not required
