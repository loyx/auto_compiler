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
def generate_binary_op_code(left: dict, right: dict, operator: str, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for binary arithmetic operations."""
    # Evaluate left expression
    left_code, offset_after_left = generate_expression_code(left, var_offsets, next_offset)
    
    # Save left result to stack (8-byte slot at offset_after_left)
    save_code = f"str x0, [sp, #{offset_after_left}]\n"
    
    # Evaluate right expression with updated offset
    right_code, offset_after_right = generate_expression_code(right, var_offsets, offset_after_left + 8)
    
    # Load saved left value into x1
    load_code = f"ldr x1, [sp, #{offset_after_left}]\n"
    
    # Map operator to ARM64 instruction
    op_instruction = _get_op_instruction(operator)
    
    # Assemble full code
    full_code = left_code + save_code + right_code + load_code + op_instruction + "\n"
    
    return full_code, offset_after_right

# === helper functions ===
def _get_op_instruction(operator: str) -> str:
    """Map binary operator to ARM64 instruction."""
    op_map = {
        "+": "add x0, x1, x0",
        "-": "sub x0, x1, x0",
        "*": "mul x0, x1, x0",
        "/": "sdiv x0, x1, x0"
    }
    return op_map[operator]

# === OOP compatibility layer ===
