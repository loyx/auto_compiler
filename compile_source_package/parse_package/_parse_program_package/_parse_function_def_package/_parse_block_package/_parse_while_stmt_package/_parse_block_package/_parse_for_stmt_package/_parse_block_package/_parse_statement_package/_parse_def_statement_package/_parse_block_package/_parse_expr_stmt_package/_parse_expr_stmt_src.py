# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_expr_stmt(parser_state: ParserState) -> AST:
    """
    解析表达式语句。
    
    语法：expr_stmt := expression SEMICOLON
    
    输入：parser_state（pos 指向表达式起始 token）
    输出：EXPR AST 节点
    副作用：消费表达式和 SEMICOLON token，更新 parser_state["pos"]
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected expression")
    
    start_line = tokens[pos]["line"]
    start_column = tokens[pos]["column"]
    
    expr_ast = _parse_expression(parser_state)
    
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected ';'")
    
    if tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';' but got '{tokens[pos]['value']}'")
    
    parser_state["pos"] = pos + 1
    
    return {
        "type": "EXPR",
        "line": start_line,
        "column": start_column,
        "children": [expr_ast]
    }

# === helper functions ===
def _expect_semicolon(parser_state: ParserState) -> None:
    """
    验证并消费 SEMICOLON token。
    
    输入：parser_state（pos 指向期望的 SEMICOLON）
    副作用：若当前 token 是 SEMICOLON 则更新 pos，否则抛出 SyntaxError
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected ';'")
    
    if tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';' but got '{tokens[pos]['value']}'")
    
    parser_state["pos"] = pos + 1

# === OOP compatibility layer ===
