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
def _parse_expr_stmt(parser_state: ParserState) -> AST:
    """Parse expression statement: expression ;"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected expression")
    
    start_line = tokens[pos].get("line", 0)
    start_column = tokens[pos].get("column", 0)
    
    expr_ast = _parse_expression(parser_state)
    
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{start_line}:{start_column}: Expected ';' after expression")
    
    if tokens[pos].get("type") != "SEMICOLON":
        raise SyntaxError(f"{filename}:{tokens[pos].get('line', 0)}:{tokens[pos].get('column', 0)}: Expected ';' after expression, got '{tokens[pos].get('value', '')}'")
    
    parser_state["pos"] = pos + 1
    
    return {
        "type": "EXPR_STMT",
        "children": [expr_ast],
        "line": start_line,
        "column": start_column
    }

# === helper functions ===

# === OOP compatibility layer ===
