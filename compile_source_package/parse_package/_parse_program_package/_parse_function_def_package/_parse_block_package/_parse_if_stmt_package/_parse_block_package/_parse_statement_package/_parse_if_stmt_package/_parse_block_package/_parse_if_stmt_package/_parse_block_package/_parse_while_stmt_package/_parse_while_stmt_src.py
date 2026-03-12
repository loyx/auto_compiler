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
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """
    Parse a WHILE loop statement.
    Grammar: 'while' '(' expression ')' block
    Returns: WHILE AST node with condition and body.
    """
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # Record WHILE token position for error reporting
    current_token = tokens[parser_state["pos"]]
    line = current_token["line"]
    column = current_token["column"]
    
    # 1. Consume WHILE keyword
    _consume_token(parser_state, "WHILE")
    
    # 2. Consume left parenthesis (
    _consume_token(parser_state, "LPAREN")
    
    # 3. Parse condition expression
    condition = _parse_expression(parser_state)
    
    # 4. Consume right parenthesis )
    _consume_token(parser_state, "RPAREN")
    
    # 5. Parse statement block (body)
    body = _parse_block(parser_state)
    
    # 6. Build and return WHILE AST node
    return {
        "type": "WHILE",
        "condition": condition,
        "body": body,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# No OOP wrapper needed for parser functions
