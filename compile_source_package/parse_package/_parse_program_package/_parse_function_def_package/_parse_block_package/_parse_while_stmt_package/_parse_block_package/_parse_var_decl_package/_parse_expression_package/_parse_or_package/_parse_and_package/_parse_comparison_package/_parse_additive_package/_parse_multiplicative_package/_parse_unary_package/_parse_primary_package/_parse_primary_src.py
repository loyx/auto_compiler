# === std / third-party imports ===
from typing import Any, Dict, Tuple

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
#   "pos": int,
#   "filename": str,
#   "error": str
# }


# === main function ===
def _parse_primary(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """Parse a primary expression (NUMBER, IDENTIFIER, or parenthesized expression)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for unexpected end of input
    if pos >= len(tokens):
        raise SyntaxError(
            f"Syntax error at {parser_state['filename']}: unexpected end of input"
        )
    
    current_token = tokens[pos]
    
    # Handle NUMBER literal
    if current_token["type"] == "NUMBER":
        token, new_state = _consume_token(parser_state, "NUMBER")
        return {
            "type": "NUMBER_LITERAL",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }, new_state
    
    # Handle IDENTIFIER
    elif current_token["type"] == "IDENTIFIER":
        token, new_state = _consume_token(parser_state, "IDENTIFIER")
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }, new_state
    
    # Handle parenthesized expression
    elif current_token["type"] == "LPAREN":
        lparen_token, after_paren_state = _consume_token(parser_state, "LPAREN")
        expr_ast, after_expr_state = _parse_expression(after_paren_state)
        _, final_state = _consume_token(after_expr_state, "RPAREN")
        
        return {
            "type": "PAREN_EXPR",
            "children": [expr_ast],
            "line": lparen_token["line"],
            "column": lparen_token["column"]
        }, final_state
    
    # Handle unexpected token type
    else:
        raise SyntaxError(
            f"Syntax error at {parser_state['filename']}:{current_token['line']}:{current_token['column']}: "
            f"unexpected token '{current_token['value']}' of type {current_token['type']}"
        )


# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not needed for this parser function node
