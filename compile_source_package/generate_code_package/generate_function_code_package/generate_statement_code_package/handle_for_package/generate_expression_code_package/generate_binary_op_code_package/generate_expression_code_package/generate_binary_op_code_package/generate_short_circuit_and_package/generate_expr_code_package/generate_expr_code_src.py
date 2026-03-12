# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_const_code_package.generate_const_code_src import generate_const_code
from .generate_var_code_package.generate_var_code_src import generate_var_code
from .generate_binary_arithmetic_code_package.generate_binary_arithmetic_code_src import generate_binary_arithmetic_code
from .generate_comparison_code_package.generate_comparison_code_src import generate_comparison_code
from .generate_short_circuit_and_package.generate_short_circuit_and_src import generate_short_circuit_and
from .generate_short_circuit_or_package.generate_short_circuit_or_src import generate_short_circuit_or

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "skip": int,
#   "true": int,
#   "false": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

ExprDict = Dict[str, Any]
# ExprDict possible fields:
# {
#   "type": str,
#   "operator": str,
#   "left": ExprDict,
#   "right": ExprDict,
#   "value": Any,
#   "name": str,
# }

# === main function ===
def generate_expr_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for any expression type. Result always in x0."""
    expr_type = expr.get("type", "")
    
    if expr_type == "CONST":
        return generate_const_code(expr.get("value"), next_offset)
    
    elif expr_type == "VAR":
        return generate_var_code(expr.get("name"), var_offsets, next_offset)
    
    elif expr_type == "AND":
        return generate_short_circuit_and(
            expr.get("left"), expr.get("right"),
            func_name, label_counter, var_offsets, next_offset
        )
    
    elif expr_type == "OR":
        return generate_short_circuit_or(
            expr.get("left"), expr.get("right"),
            func_name, label_counter, var_offsets, next_offset
        )
    
    elif expr_type in ("ADD", "SUB", "MUL", "DIV", "MOD"):
        left_code, left_offset = generate_expr_code(expr["left"], func_name, label_counter, var_offsets, next_offset)
        right_code, right_offset = generate_expr_code(expr["right"], func_name, label_counter, var_offsets, left_offset)
        return generate_binary_arithmetic_code(expr_type, left_code, right_code, left_offset, right_offset, right_offset)
    
    elif expr_type in ("EQ", "NE", "LT", "LE", "GT", "GE"):
        left_code, left_offset = generate_expr_code(expr["left"], func_name, label_counter, var_offsets, next_offset)
        right_code, right_offset = generate_expr_code(expr["right"], func_name, label_counter, var_offsets, left_offset)
        return generate_comparison_code(expr_type, left_code, right_code, left_offset, right_offset, right_offset)
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node