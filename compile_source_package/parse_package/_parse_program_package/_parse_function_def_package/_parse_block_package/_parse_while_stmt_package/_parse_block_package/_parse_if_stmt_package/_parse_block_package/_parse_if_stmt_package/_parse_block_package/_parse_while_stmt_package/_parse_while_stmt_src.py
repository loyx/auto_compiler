# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

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

# === main function ===
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """Parse while statement and return WHILE AST node."""
    tokens = parser_state["tokens"]
    
    # Get WHILE token and record position
    while_token = _current_token(parser_state)
    if while_token is None or while_token["type"] != "WHILE":
        raise SyntaxError("Expected WHILE keyword")
    
    line = while_token["line"]
    column = while_token["column"]
    
    # Consume WHILE
    _consume_token(parser_state, "WHILE")
    
    # Consume LPAREN
    _consume_token(parser_state, "LPAREN")
    
    # Parse condition expression
    condition = _parse_expression(parser_state)
    
    # Consume RPAREN
    _consume_token(parser_state, "RPAREN")
    
    # Parse statement block
    body = _parse_block(parser_state)
    
    # Return WHILE AST node
    return {
        "type": "WHILE",
        "condition": condition,
        "body": body,
        "line": line,
        "column": column
    }

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """Get current token at parser_state['pos']."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return None
    return tokens[pos]

def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """Consume current token if it matches expected type."""
    token = _current_token(parser_state)
    if token is None:
        raise SyntaxError(f"Unexpected end of input, expected {expected_type}")
    if token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {token['type']} at line {token['line']}")
    parser_state["pos"] += 1
    return token

# === OOP compatibility layer ===
