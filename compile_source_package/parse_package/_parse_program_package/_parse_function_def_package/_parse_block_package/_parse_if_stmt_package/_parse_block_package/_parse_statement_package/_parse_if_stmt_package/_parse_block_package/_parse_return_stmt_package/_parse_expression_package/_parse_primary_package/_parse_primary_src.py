# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_list_elements_package._parse_list_elements_src import _parse_list_elements

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
def _parse_primary(parser_state: ParserState) -> AST:
    """解析初级表达式（标识符、数字、字符串、布尔值、括号表达式、列表字面量）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "value": token_value, "line": line, "column": column}
    
    elif token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        numeric_value = float(token_value) if "." in token_value else int(token_value)
        return {"type": "NUMBER", "value": numeric_value, "line": line, "column": column}
    
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {"type": "STRING", "value": token_value, "line": line, "column": column}
    
    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "BOOLEAN", "value": True, "line": line, "column": column}
    
    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "BOOLEAN", "value": False, "line": line, "column": column}
    
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        expr_ast = _parse_expression(parser_state)
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ')' to close parenthesis")
        parser_state["pos"] = new_pos + 1
        return expr_ast
    
    elif token_type == "LBRACKET":
        parser_state["pos"] = pos + 1
        elements = _parse_list_elements(parser_state)
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RBRACKET":
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ']' to close list")
        parser_state["pos"] = new_pos + 1
        return {"type": "LIST", "elements": elements, "line": line, "column": column}
    
    else:
        raise SyntaxError(f"{filename}:{line}:{column}: Unexpected token '{token_value}' of type {token_type}")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not required for parser function nodes
