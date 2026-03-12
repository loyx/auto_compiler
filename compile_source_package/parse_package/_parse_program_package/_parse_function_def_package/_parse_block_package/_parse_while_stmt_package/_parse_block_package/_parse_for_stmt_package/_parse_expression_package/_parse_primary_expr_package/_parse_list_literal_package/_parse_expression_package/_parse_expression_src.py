# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_list_literal_package._parse_list_literal_src import _parse_list_literal
from ._parse_literal_package._parse_literal_src import _parse_literal
from ._parse_grouped_or_function_package._parse_grouped_or_function_src import _parse_grouped_or_function
from ._parse_identifier_or_function_package._parse_identifier_or_function_src import _parse_identifier_or_function
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._make_error_node_package._make_error_node_src import _make_error_node

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
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse a general expression. Entry point for expression parsing."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return _make_error_node(parser_state, "Unexpected end of input", pos)
    
    token = tokens[pos]
    token_type = token["type"]
    
    if token_type in ("NUMBER", "STRING", "BOOLEAN", "NONE"):
        return _parse_literal(parser_state)
    elif token_type == "LBRACKET":
        return _parse_list_literal(parser_state)
    elif token_type == "LPAREN":
        return _parse_grouped_or_function(parser_state)
    elif token_type == "IDENTIFIER":
        return _parse_identifier_or_function(parser_state)
    elif token_type in ("MINUS", "NOT"):
        return _parse_unary(parser_state)
    else:
        return _make_error_node(parser_state, f"Unexpected token: {token_type}", pos)

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# Not required for this parser module