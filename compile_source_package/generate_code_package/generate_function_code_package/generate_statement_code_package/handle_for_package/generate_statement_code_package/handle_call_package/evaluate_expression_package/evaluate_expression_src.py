# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._eval_literal_package._eval_literal_src import _eval_literal
from ._eval_identifier_package._eval_identifier_src import _eval_identifier
from ._eval_binary_package._eval_binary_src import _eval_binary
from ._eval_unary_package._eval_unary_src import _eval_unary
from ._eval_call_package._eval_call_src import _eval_call

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": "literal"|"identifier"|"binary"|"unary"|"call",
#   "value": Any (for literal),
#   "name": str (for identifier),
#   "op": str (for binary/unary),
#   "left": Expression (for binary),
#   "right": Expression (for binary),
#   "operand": Expression (for unary),
#   "func_name": str (for call),
#   "arguments": list (for call)
# }

# === main function ===
def evaluate_expression(expr: dict, var_offsets: dict) -> str:
    """Generate ARM assembly code to evaluate a single expression and place result in R0."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        return _eval_literal(expr["value"])
    elif expr_type == "identifier":
        return _eval_identifier(expr["name"], var_offsets)
    elif expr_type == "binary":
        return _eval_binary(expr["op"], expr["left"], expr["right"], var_offsets)
    elif expr_type == "unary":
        return _eval_unary(expr["op"], expr["operand"], var_offsets)
    elif expr_type == "call":
        return _eval_call(expr["func_name"], expr["arguments"], var_offsets)
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
