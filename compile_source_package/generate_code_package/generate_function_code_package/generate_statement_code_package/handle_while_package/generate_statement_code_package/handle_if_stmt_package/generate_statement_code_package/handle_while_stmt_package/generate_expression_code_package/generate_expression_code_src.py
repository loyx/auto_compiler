# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_unary_op_package._handle_unary_op_src import _handle_unary_op
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_variable_package._handle_variable_src import _handle_variable
from ._handle_function_call_package._handle_function_call_src import _handle_function_call
from ._handle_logical_op_package._handle_logical_op_src import _handle_logical_op

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
#   "condition": dict,
#   "body": list,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "binary_op", "unary_op", "literal", "variable", "function_call", "logical_op"
#   "operator": str,
#   "left": dict,
#   "right": dict,
#   "operand": dict,
#   "value": int | bool,
#   "literal_type": str,
#   "name": str,
#   "arguments": list,
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for an expression. Result always in x0."""
    expr_type = expr.get("type")
    
    if expr_type == "binary_op":
        return _handle_binary_op(expr, var_offsets, next_offset)
    elif expr_type == "unary_op":
        return _handle_unary_op(expr, var_offsets, next_offset)
    elif expr_type == "literal":
        return _handle_literal(expr, var_offsets, next_offset)
    elif expr_type == "variable":
        return _handle_variable(expr, var_offsets, next_offset)
    elif expr_type == "function_call":
        return _handle_function_call(expr, var_offsets, next_offset)
    elif expr_type == "logical_op":
        return _handle_logical_op(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
