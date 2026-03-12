# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Mutual recursion: import parent dispatcher for recursive operand processing
from ..generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields for BINOP:
# {
#   "type": "BINOP",
#   "op": str,         # "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||"
#   "left": dict,      # left operand expression dict
#   "right": dict,     # right operand expression dict
# }

# === main function ===
def _generate_binop_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """
    Generates ARM64 assembly code for binary operations.
    
    Processes left operand, saves result, processes right operand,
    then applies the binary operation. Final result in x0.
    """
    # Validate required fields
    if "op" not in expr:
        raise KeyError("Missing required field: 'op'")
    if "left" not in expr:
        raise KeyError("Missing required field: 'left'")
    if "right" not in expr:
        raise KeyError("Missing required field: 'right'")
    
    op = expr["op"]
    
    # Generate code for left operand (recursive dispatch)
    left_code = generate_expression_code(expr["left"], func_name, var_offsets)
    
    # Save left result to stack
    save_left = "str x0, [sp, #-16]!"
    
    # Generate code for right operand (recursive dispatch)
    right_code = generate_expression_code(expr["right"], func_name, var_offsets)
    
    # Restore left result into x1
    restore_left = "ldr x1, [sp], #16"
    
    # Apply binary operation based on op type
    if op == "+":
        binop_instr = "add x0, x1, x0"
    elif op == "-":
        binop_instr = "sub x0, x1, x0"
    elif op == "*":
        binop_instr = "mul x0, x1, x0"
    elif op == "/":
        binop_instr = "sdiv x0, x1, x0"
    elif op == "==":
        binop_instr = "cmp x1, x0\ncset x0, eq"
    elif op == "!=":
        binop_instr = "cmp x1, x0\ncset x0, ne"
    elif op == "<":
        binop_instr = "cmp x1, x0\ncset x0, lt"
    elif op == ">":
        binop_instr = "cmp x1, x0\ncset x0, gt"
    elif op == "<=":
        binop_instr = "cmp x1, x0\ncset x0, le"
    elif op == ">=":
        binop_instr = "cmp x1, x0\ncset x0, ge"
    elif op == "&&":
        binop_instr = "and x0, x1, x0"
    elif op == "||":
        binop_instr = "orr x0, x1, x0"
    else:
        raise ValueError(f"Unknown binary operator: {op}")
    
    # Concatenate all code segments
    return f"{left_code}\n{save_left}\n{right_code}\n{restore_left}\n{binop_instr}"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
