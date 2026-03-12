# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expression_package._parse_or_expression_src import _parse_or_expression

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
def _parse_expression(parser_state: dict) -> dict:
    """Parse an expression and return AST node.
    
    Entry point for expression parsing. Delegates to precedence-based
    parsing functions starting from lowest precedence (or/and).
    """
    ast_node, parser_state = _parse_or_expression(parser_state)
    return ast_node

# === helper functions ===
def _peek_token(parser_state: ParserState) -> Token:
    """Return current token without consuming."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError(
            f"Unexpected end of file at line {parser_state.get('line', '?')}"
        )
    return tokens[pos]

# === OOP compatibility layer ===
