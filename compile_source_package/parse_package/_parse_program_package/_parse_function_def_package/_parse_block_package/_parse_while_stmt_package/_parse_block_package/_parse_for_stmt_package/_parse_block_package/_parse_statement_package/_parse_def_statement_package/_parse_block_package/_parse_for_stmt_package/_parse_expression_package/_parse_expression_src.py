# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op
from ._parse_array_literal_package._parse_array_literal_src import _parse_array_literal
from ._parse_dict_literal_package._parse_dict_literal_src import _parse_dict_literal

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
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse an expression from token stream.
    
    Handles: literals, identifiers, binary operations, function calls,
    array/dict literals. Uses precedence climbing for binary ops.
    """
    if parser_state["pos"] >= len(parser_state["tokens"]):
        raise SyntaxError(f"Unexpected end of input in {parser_state['filename']}")
    
    token = parser_state["tokens"][parser_state["pos"]]
    
    # Check for array literal
    if token["type"] == "LBRACKET":
        return _parse_array_literal(parser_state)
    
    # Check for dict literal
    if token["type"] == "LBRACE":
        return _parse_dict_literal(parser_state)
    
    # Parse primary expression (literals, identifiers, function calls)
    left = _parse_primary(parser_state)
    
    # Parse binary operations with precedence climbing
    return _parse_binary_op(parser_state, 0)


# === helper functions ===
def _get_operator_precedence(op_type: str) -> int:
    """Return precedence level for operator type. Higher = binds tighter."""
    precedence_map = {
        "OR": 1,
        "AND": 2,
        "EQ": 3, "NEQ": 3,
        "LT": 4, "GT": 4, "LTE": 4, "GTE": 4,
        "PLUS": 5, "MINUS": 5,
        "MUL": 6, "DIV": 6,
    }
    return precedence_map.get(op_type, 0)


# === OOP compatibility layer ===
