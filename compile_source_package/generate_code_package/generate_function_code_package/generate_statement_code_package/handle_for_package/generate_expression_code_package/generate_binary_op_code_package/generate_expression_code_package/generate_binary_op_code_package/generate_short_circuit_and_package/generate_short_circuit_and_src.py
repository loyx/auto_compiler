# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expr_code_package.generate_expr_code_src import generate_expr_code

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
def generate_short_circuit_and(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for short-circuit AND operation.
    
    If left operand is 0 (false), skip right evaluation and result is 0.
    Otherwise, evaluate right operand and result is right operand value.
    """
    # Generate unique skip label using current skip counter value
    skip_label = f"{func_name}_and_skip_{label_counter['skip']}"
    label_counter['skip'] += 1  # Increment in-place after using
    
    # Step 1: Evaluate left operand (result in x0)
    left_code, next_offset = generate_expr_code(
        expr["left"], func_name, label_counter, var_offsets, next_offset
    )
    
    # Step 2: Compare x0 to 0 and branch to skip if zero (cbz = compare and branch if zero)
    branch_code = f"    cbz x0, {skip_label}\n"
    
    # Step 3: Evaluate right operand only if left was non-zero (result in x0)
    right_code, next_offset = generate_expr_code(
        expr["right"], func_name, label_counter, var_offsets, next_offset
    )
    
    # Step 4: Place skip label at end
    label_code = f"{skip_label}:\n"
    
    # Combine all code segments
    total_code = left_code + branch_code + right_code + label_code
    
    return (total_code, next_offset)

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# Not needed - this is a pure function node, not a framework entry point
