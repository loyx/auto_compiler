# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_function_call_package._parse_function_call_src import _parse_function_call
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

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
def _parse_expression(parser_state: dict) -> dict:
    """Parse expression from tokens into AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(f"{filename}:0:0: Unexpected end of expression")
    
    # Parse primary expression first
    left = _parse_primary(parser_state)
    
    # Check for function call
    new_pos = parser_state["pos"]
    if new_pos < len(tokens) and tokens[new_pos]["type"] == "LPAREN":
        return _parse_function_call(parser_state, left)
    
    # Parse binary operations with precedence
    return _parse_binary_op(parser_state, left, 0)

# === helper functions ===
def _get_operator_precedence(op_type: str) -> int:
    """Get precedence level for operator type."""
    precedence_map = {
        "OR": 1,
        "AND": 2,
        "EQ": 3, "NEQ": 3, "LT": 3, "LTE": 3, "GT": 3, "GTE": 3,
        "PLUS": 4, "MINUS": 4,
        "MUL": 5, "DIV": 5, "MOD": 5,
        "POWER": 6,
    }
    return precedence_map.get(op_type, 0)

# === OOP compatibility layer ===
