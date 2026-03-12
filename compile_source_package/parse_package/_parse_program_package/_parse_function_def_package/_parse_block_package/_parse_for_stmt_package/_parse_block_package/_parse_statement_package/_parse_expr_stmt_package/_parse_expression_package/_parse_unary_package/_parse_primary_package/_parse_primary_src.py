# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_number_package._parse_number_src import _parse_number
from ._parse_string_package._parse_string_src import _parse_string
from ._parse_identifier_package._parse_identifier_src import _parse_identifier
from ._parse_boolean_package._parse_boolean_src import _parse_boolean
from ._parse_paren_package._parse_paren_src import _parse_paren

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
    """
    Parse primary expression by dispatching to specialized handlers.
    Handles: NUMBER, STRING, IDENTIFIER, TRUE, FALSE, LPAREN.
    Raises SyntaxError on invalid input.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    
    if token_type == "NUMBER":
        return _parse_number(token)
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        return _parse_string(token)
    elif token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return _parse_identifier(token)
    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return _parse_boolean(token)
    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return _parse_boolean(token)
    elif token_type == "LPAREN":
        return _parse_paren(parser_state)
    else:
        line = token["line"]
        column = token["column"]
        value = token["value"]
        raise SyntaxError(
            f"Unexpected token '{value}' ({token_type}) at line {line}, column {column}. "
            f"Expected primary expression."
        )

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for parser function node
