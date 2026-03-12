# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_function_call_package._parse_function_call_src import _parse_function_call
from ._parse_paren_expression_package._parse_paren_expression_src import _parse_paren_expression

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
    """Parse primary expression (literals, identifiers, function calls, parenthesized expressions)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of file at {parser_state['filename']}")
    
    token = tokens[pos]
    token_type = token["type"]
    line = token["line"]
    column = token["column"]
    
    # Integer literal
    if token_type == "INT":
        parser_state["pos"] += 1
        return {"type": "literal", "value": int(token["value"]), "children": [], "line": line, "column": column}
    
    # String literal
    if token_type == "STRING":
        parser_state["pos"] += 1
        return {"type": "literal", "value": token["value"][1:-1], "children": [], "line": line, "column": column}
    
    # Boolean literals
    if token_type == "TRUE":
        parser_state["pos"] += 1
        return {"type": "literal", "value": True, "children": [], "line": line, "column": column}
    
    if token_type == "FALSE":
        parser_state["pos"] += 1
        return {"type": "literal", "value": False, "children": [], "line": line, "column": column}
    
    # Identifier or function call
    if token_type == "IDENT":
        parser_state["pos"] += 1
        if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "LPAREN":
            parser_state["pos"] += 1  # consume '('
            return _parse_function_call(parser_state, token["value"], line, column)
        return {"type": "identifier", "value": token["value"], "children": [], "line": line, "column": column}
    
    # Parenthesized expression
    if token_type == "LPAREN":
        parser_state["pos"] += 1  # consume '('
        return _parse_paren_expression(parser_state, line, column)
    
    raise SyntaxError(f"Unexpected token {token_type} at {parser_state['filename']}:{line}:{column}")


# === helper functions ===
# No helper functions; all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
