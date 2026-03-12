# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_assignment_package._parse_assignment_src import _parse_assignment
from ._parse_expression_statement_package._parse_expression_statement_src import _parse_expression_statement
from ._parse_declaration_package._parse_declaration_src import _parse_declaration

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,           # token type (e.g., "IDENT", "SEMICOLON", "ASSIGN")
#   "value": str,          # token value (e.g., "x", ";", "=")
#   "line": int,           # source line number
#   "column": int          # source column number
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,           # node type (e.g., "ASSIGNMENT", "EXPRESSION", "DECLARATION")
#   "children": list,      # list of child AST nodes
#   "value": str,          # node value (e.g., "=", "x")
#   "line": int,           # source line number
#   "column": int          # source column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,        # list of Token
#   "pos": int,            # current position in tokens
#   "filename": str,       # source filename
#   "error": str           # error message (if any)
# }

# === main function ===
def _parse_statement(parser_state: dict) -> dict:
    """Parse a single statement from token stream and return its AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing statement")
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    
    # Dispatch based on statement type
    if token_type == "IDENT":
        # Could be assignment or expression statement
        # Look ahead to check for ASSIGN
        if pos + 1 < len(tokens) and tokens[pos + 1]["type"] == "ASSIGN":
            ast = _parse_assignment(parser_state)
        else:
            ast = _parse_expression_statement(parser_state)
    elif token_type == "KEYWORD":
        # Declaration statement (let/var/const)
        ast = _parse_declaration(parser_state)
    else:
        raise SyntaxError(f"Unexpected token '{current_token['value']}' at line {current_token['line']}, column {current_token['column']}")
    
    # Consume SEMICOLON
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError("Expected ';' at end of statement")
    
    semicolon_token = tokens[parser_state["pos"]]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';' but found '{semicolon_token['value']}' at line {semicolon_token['line']}, column {semicolon_token['column']}")
    
    parser_state["pos"] += 1  # Move past SEMICOLON
    
    return ast

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this parser function node
