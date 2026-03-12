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
def generate_short_circuit_or(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for short-circuit OR operation.
    
    If left operand is non-zero, skip right evaluation.
    Returns (code, next_offset).
    """
    left_expr = expr["left"]
    right_expr = expr["right"]
    
    # Generate code for left operand (result in x0)
    left_code, next_offset = generate_expr_code(
        left_expr, func_name, label_counter, var_offsets, next_offset
    )
    
    # Generate unique skip label
    skip_count = label_counter.get("skip", 0)
    skip_label = f"L_{func_name}_skip_{skip_count}"
    label_counter["skip"] = skip_count + 1
    
    # Build short-circuit OR code
    # cbnz: compare and branch if non-zero (skip right if left != 0)
    code_lines = [
        left_code.rstrip(),
        f"    cbnz x0, {skip_label}",
    ]
    
    # Generate code for right operand (only if left was zero)
    right_code, next_offset = generate_expr_code(
        right_expr, func_name, label_counter, var_offsets, next_offset
    )
    code_lines.append(right_code.rstrip())
    
    # Place skip label at end
    code_lines.append(f"{skip_label}:")
    
    return "\n".join(code_lines) + "\n", next_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node