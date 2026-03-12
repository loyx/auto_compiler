# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_call_expr_package._parse_call_expr_src import _parse_call_expr
from ._parse_list_literal_package._parse_list_literal_src import _parse_list_literal

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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """
    解析初级表达式（标识符、字面量、括号表达式、列表、函数调用）。
    直接修改 parser_state["pos"]，返回 AST 节点。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]

    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "ERROR", "value": "Unexpected end of input", "line": 0, "column": 0, "children": []}

    token = tokens[pos]
    token_type = token["type"]
    token_line = token["line"]
    token_column = token["column"]

    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        next_pos = parser_state["pos"]
        if next_pos < len(tokens) and tokens[next_pos]["type"] == "LPAREN":
            return _parse_call_expr(parser_state, token)
        return {"type": "IDENTIFIER", "value": token["value"], "line": token_line, "column": token_column, "children": []}

    elif token_type in ("NUMBER", "STRING", "TRUE", "FALSE", "NONE"):
        parser_state["pos"] += 1
        return {"type": "LITERAL", "value": token["value"], "line": token_line, "column": token_column, "children": []}

    elif token_type == "LPAREN":
        parser_state["pos"] += 1
        from .expression_parser_src import _parse_expression
        inner_expr = _parse_expression(parser_state)
        pos = parser_state["pos"]
        if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
            parser_state["error"] = "Expected ')'"
            return {"type": "ERROR", "value": "Expected ')'", "line": token_line, "column": token_column, "children": []}
        parser_state["pos"] += 1
        return inner_expr

    elif token_type == "LBRACKET":
        parser_state["pos"] += 1
        return _parse_list_literal(parser_state, token)

    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return {"type": "ERROR", "value": f"Unexpected token: {token_type}", "line": token_line, "column": token_column, "children": []}


# === helper functions ===
# No helper functions; all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed
