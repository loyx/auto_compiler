# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._peek_token_package._peek_token_src import _peek_token
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
def _parse_primary(parser_state: ParserState) -> tuple:
    """
    Parse primary expressions (literals, identifiers, parenthesized expressions).
    Returns: (AST node, updated_parser_state)
    """
    token = _peek_token(parser_state)
    
    if token is None:
        raise SyntaxError("Expected expression")
    
    token_type = token["type"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "NUMBER":
        consumed = _consume_token(parser_state, "NUMBER")
        ast_node = {
            "type": "LITERAL",
            "value": consumed["value"],
            "line": line,
            "column": column
        }
        return (ast_node, parser_state)
    
    elif token_type == "STRING":
        consumed = _consume_token(parser_state, "STRING")
        ast_node = {
            "type": "LITERAL",
            "value": consumed["value"],
            "line": line,
            "column": column
        }
        return (ast_node, parser_state)
    
    elif token_type == "IDENTIFIER":
        consumed = _consume_token(parser_state, "IDENTIFIER")
        ast_node = {
            "type": "IDENTIFIER",
            "value": consumed["value"],
            "line": line,
            "column": column
        }
        return (ast_node, parser_state)
    
    elif token_type == "LPAREN":
        _consume_token(parser_state, "LPAREN")
        ast_node, parser_state = _parse_expression(parser_state)
        _consume_token(parser_state, "RPAREN")
        return (ast_node, parser_state)
    
    else:
        raise SyntaxError(f"Unexpected token: {token_type}")

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# Not needed for parser function nodes
