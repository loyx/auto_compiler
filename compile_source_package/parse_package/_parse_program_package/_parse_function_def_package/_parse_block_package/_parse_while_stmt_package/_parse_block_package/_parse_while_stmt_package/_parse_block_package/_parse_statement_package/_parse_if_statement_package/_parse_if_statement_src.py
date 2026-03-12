# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block
from ._peek_token_package._peek_token_src import _peek_token

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
def _parse_if_statement(parser_state: dict) -> dict:
    """
    Parse IF statement (IF token already consumed).
    Expected syntax: IF LPAREN expression RPAREN block [ELSE block]
    Returns IF_STATEMENT AST node.
    """
    # Get IF token position info from already-consumed token
    if_token = parser_state["tokens"][parser_state["pos"] - 1]
    if_line = if_token["line"]
    if_column = if_token["column"]
    
    # 1. Consume LPAREN
    _consume_token(parser_state, "LPAREN")
    
    # 2. Parse condition expression
    condition_ast = _parse_expression(parser_state)
    
    # 3. Consume RPAREN
    _consume_token(parser_state, "RPAREN")
    
    # 4. Parse then block
    then_block_ast = _parse_block(parser_state)
    
    # 5. Check for ELSE
    else_block_ast = None
    next_token = _peek_token(parser_state)
    if next_token is not None and next_token["type"] == "ELSE":
        _consume_token(parser_state, "ELSE")
        else_block_ast = _parse_block(parser_state)
    
    # 6. Return IF_STATEMENT AST
    return {
        "type": "IF_STATEMENT",
        "condition": condition_ast,
        "then_block": then_block_ast,
        "else_block": else_block_ast,
        "line": if_line,
        "column": if_column
    }

# === helper functions ===
# No helper functions needed; all logic delegated to child functions

# === OOP compatibility layer ===
# Not needed for parser function node
