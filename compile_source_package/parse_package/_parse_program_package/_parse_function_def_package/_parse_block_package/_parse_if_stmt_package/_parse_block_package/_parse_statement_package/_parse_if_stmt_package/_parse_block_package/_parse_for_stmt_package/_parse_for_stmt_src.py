# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
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
def _parse_for_stmt(parser_state: dict) -> dict:
    """Parse for statement and return FOR AST node."""
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # Record FOR token position
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected FOR")
    
    for_token = tokens[parser_state["pos"]]
    start_line = for_token["line"]
    start_column = for_token["column"]
    
    # Consume FOR token
    _consume_token(parser_state, "FOR")
    
    # Consume LPAREN
    _consume_token(parser_state, "LPAREN")
    
    # Parse initializer (can be empty)
    initializer = None
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] != "SEMICOLON":
        initializer = _parse_expression(parser_state)
    
    # Consume first SEMICOLON
    _consume_token(parser_state, "SEMICOLON")
    
    # Parse condition (can be empty)
    condition = None
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] != "SEMICOLON":
        condition = _parse_expression(parser_state)
    
    # Consume second SEMICOLON
    _consume_token(parser_state, "SEMICOLON")
    
    # Parse increment (can be empty)
    increment = None
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] != "RPAREN":
        increment = _parse_expression(parser_state)
    
    # Consume RPAREN
    _consume_token(parser_state, "RPAREN")
    
    # Parse body block
    body = _parse_block(parser_state)
    
    # Build FOR AST node
    return {
        "type": "FOR",
        "initializer": initializer,
        "condition": condition,
        "increment": increment,
        "body": body,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===
# No helper functions needed; all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function
