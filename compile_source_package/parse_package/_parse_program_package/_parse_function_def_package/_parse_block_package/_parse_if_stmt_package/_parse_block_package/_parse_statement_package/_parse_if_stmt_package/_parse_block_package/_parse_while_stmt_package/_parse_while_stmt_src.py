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
    """Parse while statement. WHILE '(' condition ')' block
    
    Resource IO:
    - Reads parser_state["tokens"], parser_state["filename"], parser_state["pos"]
    - Writes parser_state["pos"] (advances position through tokens)
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # Record WHILE token position
    while_token = _get_current_token(parser_state)
    line = while_token["line"]
    column = while_token["column"]
    
    # Consume WHILE token
    _consume_token(parser_state, "WHILE", filename, line, column)
    
    # Consume LPAREN
    _consume_token(parser_state, "LPAREN", filename, line, column)
    
    # Parse condition expression
    condition = _parse_expression(parser_state)
    
    # Consume RPAREN
    _consume_token(parser_state, "RPAREN", filename, line, column)
    
    # Parse body block
    body = _parse_block(parser_state)
    
    # Build WHILE AST node
    return {
        "type": "WHILE",
        "condition": condition,
        "body": body,
        "line": line,
        "column": column
    }

# === helper functions ===
def _get_current_token(parser_state: ParserState) -> Token:
    """Get current token at parser_state["pos"]."""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return {"type": "EOF", "value": "", "line": 0, "column": 0}
    return tokens[pos]

def _consume_token(parser_state: ParserState, expected_type: str, 
                   filename: str, line: int, column: int) -> None:
    """Consume current token if it matches expected type, else raise SyntaxError."""
    token = _get_current_token(parser_state)
    if token["type"] != expected_type:
        raise SyntaxError(
            f"{filename}:{line}:{column}: Expected {expected_type}, got {token['type']}"
        )
    parser_state["pos"] += 1

# === OOP compatibility layer ===
