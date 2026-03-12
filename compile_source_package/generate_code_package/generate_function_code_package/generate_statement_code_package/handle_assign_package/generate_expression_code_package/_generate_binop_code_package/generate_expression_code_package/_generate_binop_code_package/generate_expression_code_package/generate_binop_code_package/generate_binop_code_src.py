# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import parent dispatcher for recursive operand processing
from ..generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,       # "BINOP", "VAR", "LITERAL"
#   "op": str,         # For BINOP: "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="
#   "left": dict,      # For BINOP: left operand expression dict
#   "right": dict,     # For BINOP: right operand expression dict
#   "name": str,       # For VAR: variable name
#   "value": int,      # For LITERAL: integer literal value
# }

# === main function ===
def generate_binop_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate ARM64 assembly code for binary operations with result in x0."""
    # Validate required fields
    if "op" not in expr:
        raise ValueError(f"Missing 'op' field in BINOP expression for {func_name}")
    if "left" not in expr:
        raise ValueError(f"Missing 'left' field in BINOP expression for {func_name}")
    if "right" not in expr:
        raise ValueError(f"Missing 'right' field in BINOP expression for {func_name}")
    
    op = expr["op"]
    left_expr = expr["left"]
    right_expr = expr["right"]
    
    # Generate code for left operand (result in x0), save to x1
    left_code = generate_expression_code(left_expr, func_name, var_offsets)
    save_left = "    mov x1, x0"
    
    # Generate code for right operand (result in x0), save to x2
    right_code = generate_expression_code(right_expr, func_name, var_offsets)
    save_right = "    mov x2, x0"
    
    # Restore left to x0, then apply operation
    restore_left = "    mov x0, x1"
    
    # Determine operation based on op type
    if op == "+":
        op_code = "    add x0, x0, x2"
    elif op == "-":
        op_code = "    sub x0, x0, x2"
    elif op == "*":
        op_code = "    mul x0, x0, x2"
    elif op == "/":
        op_code = "    sdiv x0, x0, x2"
    elif op == "==":
        op_code = "    cmp x0, x2\n    cset x0, eq"
    elif op == "!=":
        op_code = "    cmp x0, x2\n    cset x0, ne"
    elif op == "<":
        op_code = "    cmp x0, x2\n    cset x0, lt"
    elif op == ">":
        op_code = "    cmp x0, x2\n    cset x0, gt"
    elif op == "<=":
        op_code = "    cmp x0, x2\n    cset x0, le"
    elif op == ">=":
        op_code = "    cmp x0, x2\n    cset x0, ge"
    else:
        raise ValueError(f"Unsupported operator '{op}' in {func_name}")
    
    # Concatenate all assembly lines
    assembly_lines = [
        left_code,
        save_left,
        right_code,
        save_right,
        restore_left,
        op_code
    ]
    
    return "\n".join(assembly_lines)

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# Not needed - this is a pure function node, not a framework entry point
