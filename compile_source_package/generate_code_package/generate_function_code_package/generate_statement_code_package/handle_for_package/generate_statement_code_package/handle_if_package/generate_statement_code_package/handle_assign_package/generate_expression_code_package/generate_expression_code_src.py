# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_identifier_package._handle_identifier_src import _handle_identifier
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_call_package._handle_call_src import _handle_call

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,  # "LITERAL" | "IDENTIFIER" | "BINARY_OP" | "CALL"
#   "value": int,  # for LITERAL
#   "name": str,  # for IDENTIFIER
#   "op": str,  # for BINARY_OP
#   "left": Dict,  # for BINARY_OP
#   "right": Dict,  # for BINARY_OP
#   "func_name": str,  # for CALL
#   "args": list,  # for CALL
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code to evaluate an expression, leaving result in R0."""
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        return _handle_literal(expr, next_offset)
    elif expr_type == "IDENTIFIER":
        return _handle_identifier(expr, var_offsets, next_offset)
    elif expr_type == "BINARY_OP":
        return _handle_binary_op(expr, func_name, label_counter, var_offsets, next_offset)
    elif expr_type == "CALL":
        return _handle_call(expr, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions in main file - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node