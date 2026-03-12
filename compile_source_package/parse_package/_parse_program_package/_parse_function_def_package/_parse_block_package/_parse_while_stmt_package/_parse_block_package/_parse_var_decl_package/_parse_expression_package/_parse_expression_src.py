# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_package._parse_or_src import _parse_or
from ._consume_token_package._consume_token_src import _consume_token

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
    """
    Parse an expression using recursive descent parsing.
    Entry point that handles assignment and delegates to _parse_or for other expressions.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for end of input
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing expression")
    
    # Check for assignment expression (identifier = expression)
    token = tokens[pos]
    if token["type"] == "IDENTIFIER":
        # Look ahead to check for assignment
        next_pos = pos + 1
        if next_pos < len(tokens) and tokens[next_pos]["type"] == "ASSIGN":
            # This is an assignment expression
            identifier_name = token["value"]
            line, column = token["line"], token["column"]
            
            # Consume identifier and ASSIGN
            parser_state = _consume_token(parser_state, "IDENTIFIER")
            parser_state = _consume_token(parser_state, "ASSIGN")
            
            # Parse the right-hand side expression
            rhs_ast = _parse_expression(parser_state)
            
            return {
                "type": "ASSIGN",
                "value": identifier_name,
                "children": [rhs_ast],
                "line": line,
                "column": column
            }
    
    # Not an assignment, delegate to _parse_or
    ast, parser_state = _parse_or(parser_state)
    return ast

# === helper functions ===
# No helper functions in this file - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this parser function