# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """
    Parse unary expression: operator followed by primary expression.
    Input: parser_state with pos pointing to unary operator.
    Output: UNARY_OP AST node.
    Side effect: updates parser_state["pos"].
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Get current token (unary operator)
    op_token = tokens[pos]
    operator = op_token["value"]
    line = op_token["line"]
    column = op_token["column"]
    
    # Consume the operator token
    parser_state["pos"] = pos + 1
    
    # Parse the operand (primary expression)
    operand_ast = _parse_primary(parser_state)
    
    # Build UNARY_OP AST node
    return {
        "type": "UNARY_OP",
        "children": [operand_ast],
        "value": operator,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node