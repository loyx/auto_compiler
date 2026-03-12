# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

DeclarationAST = Dict[str, Any]
# DeclarationAST possible fields:
# {
#   "type": "DECLARATION",
#   "kind": str,  # "let" or "const"
#   "name": str,  # variable name
#   "value": AST | None,  # initializer expression
#   "line": int,
#   "column": int
# }

# === main function ===
def _parse_declaration(parser_state: dict) -> dict:
    """Parse a declaration statement (LET/CONST)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Step 1: Record LET/CONST token position
    keyword_token = tokens[pos]
    line = keyword_token["line"]
    column = keyword_token["column"]
    kind = keyword_token["value"].lower()
    
    # Step 2: Consume LET or CONST token
    _consume_token(parser_state, keyword_token["type"])
    
    # Step 3: Consume IDENT token (variable name)
    ident_token = _consume_token(parser_state, "IDENT")
    name = ident_token["value"]
    
    # Step 4: Check for ASSIGN and parse initializer if present
    value = None
    if parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] == "ASSIGN":
            _consume_token(parser_state, "ASSIGN")
            value = _parse_expression(parser_state)
    
    # Step 5: Consume optional SEMICOLON
    if parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        if current_token["type"] == "SEMICOLON":
            _consume_token(parser_state, "SEMICOLON")
    
    # Step 6: Return DECLARATION AST node
    return {
        "type": "DECLARATION",
        "kind": kind,
        "name": name,
        "value": value,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed - logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed - this is a parser function, not a framework entry point
