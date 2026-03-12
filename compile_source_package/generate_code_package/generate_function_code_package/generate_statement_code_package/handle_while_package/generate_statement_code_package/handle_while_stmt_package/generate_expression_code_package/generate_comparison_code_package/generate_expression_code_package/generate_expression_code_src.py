# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_literal_code_package.generate_literal_code_src import generate_literal_code
from .generate_variable_code_package.generate_variable_code_src import generate_variable_code
from .generate_binary_op_code_package.generate_binary_op_code_src import generate_binary_op_code
from .generate_unary_op_code_package.generate_unary_op_code_src import generate_unary_op_code
from .generate_comparison_code_package.generate_comparison_code_src import generate_comparison_code
from .generate_logical_op_code_package.generate_logical_op_code_src import generate_logical_op_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "literal" | "variable" | "binary_op" | "unary_op" | "comparison" | "and" | "or"
#   "value": Any,  # for literal type
#   "var_name": str,  # for variable type
#   "left": dict,  # for binary_op/comparison/and/or
#   "right": dict,  # for binary_op/comparison/and/or
#   "operator": str,  # for binary_op/unary_op/comparison
#   "operand": dict,  # for unary_op
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for an expression node."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        return generate_literal_code(expr["value"], next_offset)
    elif expr_type == "variable":
        return generate_variable_code(expr["var_name"], var_offsets, next_offset)
    elif expr_type == "binary_op":
        return generate_binary_op_code(expr["left"], expr["right"], expr["operator"], var_offsets, next_offset)
    elif expr_type == "unary_op":
        return generate_unary_op_code(expr["operand"], expr["operator"], var_offsets, next_offset)
    elif expr_type == "comparison":
        return generate_comparison_code(expr["left"], expr["right"], expr["operator"], var_offsets, next_offset)
    elif expr_type in ("and", "or"):
        return generate_logical_op_code(expr["left"], expr["right"], expr_type, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this function node
