# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,
#   "value": Any,
#   "var_name": str,
#   "left": dict,
#   "right": dict,
#   "operator": str,
#   "operand": dict,
# }

# === main function ===
def generate_unary_op_code(operand: dict, operator: str, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 code for unary operations (negation).
    
    Evaluates operand recursively, then applies negation (NEG x0, x0).
    Result left in x0 register.
    """
    if operator != "-":
        raise ValueError(f"Unsupported unary operator: {operator}")
    
    if operand is None:
        raise ValueError("Unary operand cannot be None")
    
    # Recursively evaluate operand
    code, new_offset = generate_expression_code(operand, var_offsets, next_offset)
    
    # Apply negation
    code += "    NEG x0, x0\n"
    
    return code, new_offset

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node