# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_package._parse_or_src import _parse_or

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
#   "line": int,
#   "column": int,
#   "value": Any,
#   "literal_type": str,
#   "name": str,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "callee": AST,
#   "arguments": list
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
    Parse an expression using recursive descent with operator precedence.
    Entry point for expression parsing. Delegates to _parse_or for lowest precedence.
    """
    return _parse_or(parser_state)

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """Get current token at parser_state['pos']."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    return {"type": "EOF", "value": "", "line": 0, "column": 0}

def _advance(parser_state: ParserState) -> Token:
    """Advance pos and return the token that was at pos before advancing."""
    token = _current_token(parser_state)
    parser_state["pos"] += 1
    return token

def _syntax_error(parser_state: ParserState, message: str) -> None:
    """Raise SyntaxError with filename:line:column format."""
    token = _current_token(parser_state)
    filename = parser_state.get("filename", "unknown")
    raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: {message}")

# === OOP compatibility layer ===
# Not needed for this parser function
