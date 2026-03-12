# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._parse_if_package._parse_if_src import _parse_if
from ._parse_while_package._parse_while_src import _parse_while
from ._parse_return_package._parse_return_src import _parse_return
from ._parse_assignment_package._parse_assignment_src import _parse_assignment
from ._parse_expression_statement_package._parse_expression_statement_src import _parse_expression_statement

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
#   "error": str | None
# }

# === main function ===
def _parse_statement(parser_state: dict) -> dict:
    """Parse a single statement and return corresponding AST node."""
    token = _peek_token(parser_state)
    if token is None:
        raise SyntaxError(f"Unexpected end of input at line 0, column 0")
    
    if token["type"] == "IF":
        return _parse_if(parser_state)
    elif token["type"] == "WHILE":
        return _parse_while(parser_state)
    elif token["type"] == "RETURN":
        return _parse_return(parser_state)
    elif token["type"] == "IDENTIFIER":
        next_token = _peek_token_at(parser_state, parser_state["pos"] + 1)
        if next_token and next_token["type"] == "ASSIGN":
            return _parse_assignment(parser_state)
        else:
            return _parse_expression_statement(parser_state)
    else:
        return _parse_expression_statement(parser_state)

# === helper functions ===
def _peek_token_at(parser_state: dict, pos: int) -> dict | None:
    """Peek token at specific position without modifying pos."""
    tokens = parser_state.get("tokens", [])
    if 0 <= pos < len(tokens):
        return tokens[pos]
    return None

# === OOP compatibility layer ===
