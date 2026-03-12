# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op
from ._parse_number_value_package._parse_number_value_src import _parse_number_value
from ._parse_string_value_package._parse_string_value_src import _parse_string_value

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
#   "name": str,
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
    解析基本表达式（primary expression）。
    
    支持：字面量（NUMBER/STRING/TRUE/FALSE/NIL）、标识符（IDENTIFIER）、
    括号分组表达式（LPAREN ... RPAREN）。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_line = current_token["line"]
    token_column = current_token["column"]
    
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        return {
            "type": "literal",
            "value": _parse_number_value(current_token["value"]),
            "line": token_line,
            "column": token_column
        }
    
    if token_type == "STRING":
        parser_state["pos"] += 1
        return {
            "type": "literal",
            "value": _parse_string_value(current_token["value"]),
            "line": token_line,
            "column": token_column
        }
    
    if token_type == "TRUE":
        parser_state["pos"] += 1
        return {"type": "literal", "value": True, "line": token_line, "column": token_column}
    
    if token_type == "FALSE":
        parser_state["pos"] += 1
        return {"type": "literal", "value": False, "line": token_line, "column": token_column}
    
    if token_type == "NIL":
        parser_state["pos"] += 1
        return {"type": "literal", "value": None, "line": token_line, "column": token_column}
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "identifier",
            "name": current_token["value"],
            "line": token_line,
            "column": token_column
        }
    
    if token_type == "LPAREN":
        parser_state["pos"] += 1
        expr = _parse_primary(parser_state)
        expr = _parse_binary_op(parser_state, 0, expr)
        
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"Missing ')' at line {token_line}")
        closing_token = tokens[parser_state["pos"]]
        if closing_token["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')' but got {closing_token['type']} at line {closing_token['line']}")
        parser_state["pos"] += 1
        
        return {
            "type": "grouping",
            "children": [expr],
            "line": token_line,
            "column": token_column
        }
    
    raise SyntaxError(f"Unexpected token {token_type} at line {token_line}, column {token_column}")


# === helper functions ===
# No helper functions in this file; all delegated to sub-functions.

# === OOP compatibility layer ===
# No OOP wrapper needed.
