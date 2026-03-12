# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """Parse primary expression (identifier, literal, or parenthesized expression)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of input in {parser_state['filename']}"
        )
    
    token = tokens[pos]
    token_type = token["type"]
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "LITERAL":
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "PUNCTUATION" and token["value"] == "(":
        parser_state["pos"] += 1  # consume '('
        expr_ast = _parse_and_expr(parser_state)
        
        # Expect ')'
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Missing ')' in {parser_state['filename']} "
                f"at line {token['line']}, column {token['column']}"
            )
        
        closing_token = tokens[parser_state["pos"]]
        if closing_token["type"] != "PUNCTUATION" or closing_token["value"] != ")":
            raise SyntaxError(
                f"Expected ')' but got {closing_token['value']} in {parser_state['filename']} "
                f"at line {closing_token['line']}, column {closing_token['column']}"
            )
        
        parser_state["pos"] += 1  # consume ')'
        return expr_ast
    
    else:
        raise SyntaxError(
            f"Unexpected token {token['value']} ({token['type']}) in {parser_state['filename']} "
            f"at line {token['line']}, column {token['column']}"
        )

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
