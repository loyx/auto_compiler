# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_additive(parser_state: dict) -> tuple:
    """Parse additive expressions (+, -) with left-associativity."""
    # 1. Parse left operand (multiplicative level)
    left_ast, parser_state = _parse_multiplicative(parser_state)
    
    # 2. Loop to handle + and - operators (left-associative)
    while True:
        token = _peek_token(parser_state)
        if token is None or token["type"] not in ("PLUS", "MINUS"):
            break
        
        # 3. Consume the operator token
        op_token, parser_state = _consume_token(parser_state, token["type"])
        
        # 4. Parse right operand (multiplicative level)
        right_ast, parser_state = _parse_multiplicative(parser_state)
        
        # 5. Build BINARY_OP AST node
        left_ast = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left_ast, parser_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser helper functions
