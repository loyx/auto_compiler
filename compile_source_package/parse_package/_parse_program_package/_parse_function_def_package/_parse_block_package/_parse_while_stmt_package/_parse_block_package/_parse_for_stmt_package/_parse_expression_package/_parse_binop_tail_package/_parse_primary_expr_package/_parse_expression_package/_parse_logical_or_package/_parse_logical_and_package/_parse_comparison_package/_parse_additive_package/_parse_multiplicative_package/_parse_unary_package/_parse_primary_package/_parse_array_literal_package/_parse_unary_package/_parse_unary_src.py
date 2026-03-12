# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_array_literal_package._parse_array_literal_src import _parse_array_literal
from ._parse_object_literal_package._parse_object_literal_src import _parse_object_literal

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
#   "operator": str,
#   "operand": AST,
#   "elements": list,
#   "properties": list,
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
def _parse_unary(parser_state: ParserState) -> AST:
    """Parse unary expression: literals, arrays, objects, unary operators, identifiers."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "ERROR", "value": "Unexpected end of input", "line": 0, "column": 0}
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    # Literal: NUMBER
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        return {"type": "NUMBER_LITERAL", "value": float(token_value) if "." in token_value else int(token_value), "line": line, "column": column}
    
    # Literal: STRING
    if token_type == "STRING":
        parser_state["pos"] += 1
        return {"type": "STRING_LITERAL", "value": token_value, "line": line, "column": column}
    
    # Literal: TRUE
    if token_type == "TRUE":
        parser_state["pos"] += 1
        return {"type": "BOOLEAN_LITERAL", "value": True, "line": line, "column": column}
    
    # Literal: FALSE
    if token_type == "FALSE":
        parser_state["pos"] += 1
        return {"type": "BOOLEAN_LITERAL", "value": False, "line": line, "column": column}
    
    # Literal: NULL
    if token_type == "NULL":
        parser_state["pos"] += 1
        return {"type": "NULL_LITERAL", "value": None, "line": line, "column": column}
    
    # Array literal
    if token_type == "LEFT_BRACKET":
        parser_state["pos"] += 1
        return _parse_array_literal(parser_state, line, column)
    
    # Object literal
    if token_type == "LEFT_BRACE":
        parser_state["pos"] += 1
        return _parse_object_literal(parser_state, line, column)
    
    # Unary operators: NEGATE, NOT, BITWISE_NOT, PLUS
    if token_type in ("NEGATE", "NOT", "BITWISE_NOT", "PLUS"):
        parser_state["pos"] += 1
        operand = _parse_unary(parser_state)
        return {"type": "UNARY_EXPRESSION", "operator": token_type, "operand": operand, "line": line, "column": column}
    
    # Identifier
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {"type": "IDENTIFIER", "value": token_value, "line": line, "column": column}
    
    # Unknown token - ERROR
    parser_state["error"] = f"Unexpected token: {token_type}"
    return {"type": "ERROR", "value": f"Unexpected token: {token_type}", "line": line, "column": column}


# === helper functions ===
# No helper functions needed - logic is straightforward token dispatch


# === OOP compatibility layer ===
# Not needed - this is a parser function, not a framework entry point
