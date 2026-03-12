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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_return_statement(parser_state: ParserState) -> AST:
    """解析 return 语句。语法：RETURN (expression)? SEMICOLON"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 消费 RETURN token
    return_token = tokens[pos]
    line = return_token["line"]
    column = return_token["column"]
    parser_state["pos"] = pos + 1
    
    # 检查是否有返回值表达式
    children = []
    current_pos = parser_state["pos"]
    
    # 如果当前 token 不是分号，说明有表达式
    if current_pos < len(tokens) and tokens[current_pos]["type"] != "SEMICOLON":
        expr_ast = _parse_expression(parser_state)
        children.append(expr_ast)
    
    # 消费分号
    current_pos = parser_state["pos"]
    if current_pos >= len(tokens) or tokens[current_pos]["type"] != "SEMICOLON":
        raise SyntaxError("Expected ';' after return statement")
    
    parser_state["pos"] = current_pos + 1
    
    return {
        "type": "RETURN_STMT",
        "line": line,
        "column": column,
        "children": children
    }

# === helper functions ===

# === OOP compatibility layer ===
