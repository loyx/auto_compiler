# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_unary_op_package._parse_unary_op_src import _parse_unary_op
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op
from ._parse_function_call_package._parse_function_call_src import _parse_function_call

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_expression(parser_state: dict) -> dict:
    """
    解析表达式。支持标识符、字面量、一元运算、二元运算、函数调用、括号表达式。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        _raise_syntax_error(parser_state, "Unexpected end of input")
    
    # 先尝试解析一元表达式
    ast = _parse_unary_op(parser_state)
    
    # 如果不是一元表达式，解析 primary
    if ast is None:
        ast = _parse_primary(parser_state)
        if ast is None:
            _raise_syntax_error(parser_state, "Unexpected token")
    
    # 检查是否是函数调用
    if parser_state["pos"] < len(tokens):
        next_token = tokens[parser_state["pos"]]
        if next_token.get("type") == "LPAREN":
            ast = _parse_function_call(parser_state, ast)
    
    # 解析二元运算
    ast = _parse_binary_op(parser_state, ast, 0)
    
    return ast

# === helper functions ===
def _raise_syntax_error(parser_state: ParserState, message: str) -> None:
    """抛出语法错误异常。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 1)
        column = token.get("column", 1)
    else:
        line = 1
        column = 1
    
    raise SyntaxError(f"{filename}:{line}:{column}: {message}")

# === OOP compatibility layer ===
