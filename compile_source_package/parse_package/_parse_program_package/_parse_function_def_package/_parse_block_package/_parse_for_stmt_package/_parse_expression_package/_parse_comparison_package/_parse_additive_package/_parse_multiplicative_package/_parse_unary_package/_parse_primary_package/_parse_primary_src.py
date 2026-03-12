# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from .convert_literal_value_package.convert_literal_value_src import convert_literal_value
from .make_error_node_package.make_error_node_src import make_error_node

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
    """解析基础表达式（标识符、字面量、括号表达式等）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]

    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return make_error_node(pos, tokens)

    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]

    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "value": token_value, "children": [], "line": line, "column": column}

    elif token_type == "LITERAL":
        parser_state["pos"] = pos + 1
        literal_value = convert_literal_value(token_value)
        return {"type": "LITERAL", "value": literal_value, "children": [], "line": line, "column": column}

    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": True, "children": [], "line": line, "column": column}

    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": False, "children": [], "line": line, "column": column}

    elif token_type == "NIL":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": None, "children": [], "line": line, "column": column}

    elif token_type in ("LEFT_PAREN", "LPAREN"):
        parser_state["pos"] = pos + 1
        expr_ast = _parse_expression(parser_state)
        if parser_state.get("error"):
            return expr_ast
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            parser_state["error"] = "Expected ')' after expression"
            return make_error_node(new_pos, tokens)
        closing_token = tokens[new_pos]
        if closing_token["type"] not in ("RIGHT_PAREN", "RPAREN"):
            parser_state["error"] = f"Expected ')' but found {closing_token['type']}"
            return make_error_node(new_pos, tokens)
        parser_state["pos"] = new_pos + 1
        return expr_ast

    else:
        parser_state["error"] = f"Unexpected token: {token_type} at line {line}, column {column}"
        return {"type": "ERROR", "value": None, "children": [], "line": line, "column": column}


# === helper functions ===
# No helper functions in this file; all delegated to child nodes


# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
