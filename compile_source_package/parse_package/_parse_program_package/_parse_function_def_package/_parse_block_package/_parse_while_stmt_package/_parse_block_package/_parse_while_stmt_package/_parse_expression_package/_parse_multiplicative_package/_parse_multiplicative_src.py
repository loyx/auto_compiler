# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_power_package._parse_power_src import _parse_power
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
def _parse_multiplicative(parser_state: dict) -> tuple:
    """Parse multiplicative expressions (*, /, %, //)."""
    ast_node, parser_state = _parse_power(parser_state)
    
    multiplicative_ops = {"STAR", "SLASH", "PERCENT", "DOUBLESLASH"}
    op_map = {"STAR": "*", "SLASH": "/", "PERCENT": "%", "DOUBLESLASH": "//"}
    
    while True:
        token = _peek_token(parser_state)
        if token is None or token.get("type") not in multiplicative_ops:
            break
        
        op_token = _consume_token(parser_state)
        op_symbol = op_map[op_token["type"]]
        
        right_node, parser_state = _parse_power(parser_state)
        
        ast_node = {
            "type": "BINARY_OP",
            "children": [ast_node, right_node],
            "value": op_symbol,
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return ast_node, parser_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function nodes