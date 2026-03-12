# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..generate_expression_code_package.generate_expression_code_src import generate_expression_code

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
def generate_logical_code(left: dict, right: dict, operator: str, var_offsets: dict, next_offset: int, label_counter: int) -> Tuple[str, int, int]:
    """Generate ARM64 code for short-circuit logical operations with branching."""
    if operator == "and":
        return _generate_and_code(left, right, var_offsets, next_offset, label_counter)
    elif operator == "or":
        return _generate_or_code(left, right, var_offsets, next_offset, label_counter)
    else:
        raise ValueError(f"Unknown logical operator: {operator}")

# === helper functions ===
def _generate_and_code(left: Expr, right: Expr, var_offsets: VarOffsets, next_offset: int, label_counter: int) -> Tuple[str, int, int]:
    """Generate short-circuit AND code: if left is false, skip right operand."""
    false_label = f"L_and_{label_counter}"
    end_label = f"L_and_end_{label_counter}"
    
    # Evaluate left operand
    left_code, next_offset, _ = generate_expression_code(left, var_offsets, next_offset, 0)
    
    # Short-circuit: if x0 is zero, jump to false_label
    branch_code = f"    cbz x0, {false_label}\n"
    
    # Evaluate right operand
    right_code, next_offset, _ = generate_expression_code(right, var_offsets, next_offset, 0)
    
    # Jump to end (result already in x0 from right operand)
    end_jump = f"    b {end_label}\n"
    
    # False label: result is 0
    false_section = f"{false_label}:\n    mov x0, #0\n"
    
    # End label
    end_section = f"{end_label}:\n"
    
    full_code = left_code + branch_code + right_code + end_jump + false_section + end_section
    return full_code, next_offset, label_counter + 1

def _generate_or_code(left: Expr, right: Expr, var_offsets: VarOffsets, next_offset: int, label_counter: int) -> Tuple[str, int, int]:
    """Generate short-circuit OR code: if left is true, skip right operand."""
    true_label = f"L_or_{label_counter}"
    end_label = f"L_or_end_{label_counter}"
    
    # Evaluate left operand
    left_code, next_offset, _ = generate_expression_code(left, var_offsets, next_offset, 0)
    
    # Short-circuit: if x0 is non-zero, jump to true_label
    branch_code = f"    cbnz x0, {true_label}\n"
    
    # Evaluate right operand
    right_code, next_offset, _ = generate_expression_code(right, var_offsets, next_offset, 0)
    
    # Jump to end (result already in x0 from right operand)
    end_jump = f"    b {end_label}\n"
    
    # True label: result is 1
    true_section = f"{true_label}:\n    mov x0, #1\n"
    
    # End label
    end_section = f"{end_label}:\n"
    
    full_code = left_code + branch_code + right_code + end_jump + true_section + end_section
    return full_code, next_offset, label_counter + 1

# === OOP compatibility layer ===
