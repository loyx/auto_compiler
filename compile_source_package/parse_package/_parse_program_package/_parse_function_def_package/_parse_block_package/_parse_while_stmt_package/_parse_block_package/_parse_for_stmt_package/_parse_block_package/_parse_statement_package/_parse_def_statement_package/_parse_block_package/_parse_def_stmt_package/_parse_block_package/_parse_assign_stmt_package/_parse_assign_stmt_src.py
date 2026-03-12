# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_target_package._parse_target_src import _parse_target

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
def _parse_assign_stmt(parser_state: ParserState) -> AST:
    """解析赋值语句：target ASSIGN expression [SEMICOLON]"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at line {parser_state.get('filename', 'unknown')}")
    
    start_token = tokens[pos]
    start_line = start_token["line"]
    start_column = start_token["column"]
    
    # 解析左侧 target
    target_ast = _parse_target(parser_state)
    
    # 消费 ASSIGN token
    pos = parser_state["pos"]
    if pos >= len(tokens) or tokens[pos]["type"] != "ASSIGN":
        raise SyntaxError(
            f"Missing ASSIGN after target at line {start_line}, column {start_column} in {parser_state.get('filename', 'unknown')}"
        )
    parser_state["pos"] = pos + 1
    
    # 解析右侧表达式
    expression_ast = _parse_expression(parser_state)
    
    # 消费可选的 SEMICOLON
    pos = parser_state["pos"]
    if pos < len(tokens) and tokens[pos]["type"] == "SEMICOLON":
        parser_state["pos"] = pos + 1
    
    return {
        "type": "ASSIGN_STMT",
        "children": [target_ast, expression_ast],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===

# === OOP compatibility layer ===
