# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._expect_token_package._expect_token_src import _expect_token

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
#   "op": str,
#   "operand": AST,
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
    """Parse unary operators (-, NOT)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we have a current token
    if pos >= len(tokens):
        return _parse_primary(parser_state)
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # Handle MINUS unary operator
    if token_type == "MINUS":
        minus_token = _expect_token(parser_state, "MINUS")
        operand = _parse_unary(parser_state)  # Recursive for --x
        return {
            "type": "UNOP",
            "op": "-",
            "operand": operand,
            "line": minus_token["line"],
            "column": minus_token["column"],
            "children": [operand]
        }
    
    # Handle NOT unary operator
    if token_type == "NOT":
        not_token = _expect_token(parser_state, "NOT")
        operand = _parse_unary(parser_state)  # Recursive for NOT NOT x
        return {
            "type": "UNOP",
            "op": "not",
            "operand": operand,
            "line": not_token["line"],
            "column": not_token["column"],
            "children": [operand]
        }
    
    # Not a unary operator, parse primary expression
    return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed - logic is in main function

# === OOP compatibility layer ===
# Not needed for parser function nodes
