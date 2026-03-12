# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

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
#   "op": str,           # "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="
#   "left": dict,        # 左操作数表达式 dict
#   "right": dict,       # 右操作数表达式 dict
# }

# === main function ===
def _generate_binop_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generates ARM64 assembly code for binary operations."""
    op = expr["op"]
    left = expr["left"]
    right = expr["right"]
    
    # Generate code for left operand
    left_code = generate_expression_code(left, func_name, var_offsets)
    
    # Save left result from x0 to x9
    save_left = "    mov x9, x0\n"
    
    # Generate code for right operand
    right_code = generate_expression_code(right, func_name, var_offsets)
    
    # Apply binary operation based on operator
    if op == "+":
        binop_instr = "    add x0, x9, x0\n"
    elif op == "-":
        binop_instr = "    sub x0, x9, x0\n"
    elif op == "*":
        binop_instr = "    mul x0, x9, x0\n"
    elif op == "/":
        binop_instr = "    sdiv x0, x9, x0\n"
    elif op == "==":
        binop_instr = "    cmp x9, x0\n    cset x0, eq\n"
    elif op == "!=":
        binop_instr = "    cmp x9, x0\n    cset x0, ne\n"
    elif op == "<":
        binop_instr = "    cmp x9, x0\n    cset x0, lt\n"
    elif op == ">":
        binop_instr = "    cmp x9, x0\n    cset x0, gt\n"
    elif op == "<=":
        binop_instr = "    cmp x9, x0\n    cset x0, le\n"
    elif op == ">=":
        binop_instr = "    cmp x9, x0\n    cset x0, ge\n"
    else:
        raise ValueError(f"Unsupported binary operator: {op}")
    
    # Concatenate all code
    return left_code + save_left + right_code + binop_instr

# === helper functions ===

# === OOP compatibility layer ===
