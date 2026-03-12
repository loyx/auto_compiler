# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_unary_op_package._handle_unary_op_src import _handle_unary_op
from ._handle_call_package._handle_call_src import _handle_call

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "literal", "variable", "binary_op", "unary_op", "call"
#   "value": Any,          # for literal
#   "name": str,           # for variable
#   "operator": str,       # for binary_op/unary_op
#   "left": dict,          # for binary_op
#   "right": dict,         # for binary_op
#   "operand": dict,       # for unary_op
#   "function": str,       # for call
#   "args": list,          # for call
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, int]:
    """Dispatch expression code generation based on expr type."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        value = expr["value"]
        code = f"LOAD_CONST {value}\n"
        return (code, next_offset, next_offset + 1)
    
    elif expr_type == "variable":
        name = expr["name"]
        offset = var_offsets[name]
        code = f"LOAD_VAR {name}\n"
        return (code, offset, next_offset)
    
    elif expr_type == "binary_op":
        return _handle_binary_op(
            expr["operator"],
            expr["left"],
            expr["right"],
            var_offsets,
            next_offset
        )
    
    elif expr_type == "unary_op":
        return _handle_unary_op(
            expr["operator"],
            expr["operand"],
            var_offsets,
            next_offset
        )
    
    elif expr_type == "call":
        return _handle_call(
            expr["function"],
            expr["args"],
            var_offsets,
            next_offset
        )
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No inline helpers; all logic delegated to child functions

# === OOP compatibility layer ===
# Not required for this function node
