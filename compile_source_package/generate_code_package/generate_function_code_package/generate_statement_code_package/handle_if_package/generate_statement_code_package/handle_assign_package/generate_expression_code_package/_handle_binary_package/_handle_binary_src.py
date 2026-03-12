# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# Import parent dispatcher for recursive expression handling
from .. import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # maps variable name to stack slot index
# }

Expr = Dict[str, Any]
# Expr possible fields by type:
# LITERAL: {"type": "LITERAL", "value": int|float}
# IDENT: {"type": "IDENT", "name": str}
# BINARY: {"type": "BINARY", "op": str, "left": Expr, "right": Expr}
# UNARY: {"type": "UNARY", "op": str, "operand": Expr}
# Binary ops: "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||"

# === main function ===
def _handle_binary(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate assembly code for BINARY expression."""
    op = expr["op"]
    left = expr["left"]
    right = expr["right"]
    
    # Handle short-circuit operators first
    if op == "&&":
        return _handle_logical_and(left, right, var_offsets, next_offset)
    elif op == "||":
        return _handle_logical_or(left, right, var_offsets, next_offset)
    
    # For other operators: evaluate left, save to x1, evaluate right, apply op
    left_code, next_offset, left_reg = generate_expression_code(left, var_offsets, next_offset)
    right_code, next_offset, right_reg = generate_expression_code(right, var_offsets, next_offset)
    
    assembly_lines = []
    assembly_lines.extend(left_code.strip().split("\n") if left_code.strip() else [])
    assembly_lines.extend(right_code.strip().split("\n") if right_code.strip() else [])
    
    # Ensure left result is in x1
    if left_reg != "x1":
        assembly_lines.append(f"    mov x1, {left_reg}")
    
    # Apply operation
    if op == "+":
        assembly_lines.append(f"    add x0, x1, {right_reg}")
    elif op == "-":
        assembly_lines.append(f"    sub x0, x1, {right_reg}")
    elif op == "*":
        assembly_lines.append(f"    mul x0, x1, {right_reg}")
    elif op == "/":
        assembly_lines.append(f"    sdiv x0, x1, {right_reg}")
    elif op == "==":
        assembly_lines.append(f"    cmp x1, {right_reg}")
        assembly_lines.append("    cset x0, eq")
    elif op == "!=":
        assembly_lines.append(f"    cmp x1, {right_reg}")
        assembly_lines.append("    cset x0, ne")
    elif op == "<":
        assembly_lines.append(f"    cmp x1, {right_reg}")
        assembly_lines.append("    cset x0, lt")
    elif op == ">":
        assembly_lines.append(f"    cmp x1, {right_reg}")
        assembly_lines.append("    cset x0, gt")
    elif op == "<=":
        assembly_lines.append(f"    cmp x1, {right_reg}")
        assembly_lines.append("    cset x0, le")
    elif op == ">=":
        assembly_lines.append(f"    cmp x1, {right_reg}")
        assembly_lines.append("    cset x0, ge")
    else:
        raise ValueError(f"Unsupported binary operator: {op}")
    
    assembly_code = "\n".join(assembly_lines) + "\n" if assembly_lines else ""
    return assembly_code, next_offset, "x0"

# === helper functions ===
def _handle_logical_and(left: Expr, right: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate short-circuit code for logical AND (&&)."""
    label_end = f"__and_end_{next_offset}"
    
    # Evaluate left operand
    left_code, next_offset, left_reg = generate_expression_code(left, var_offsets, next_offset)
    assembly_lines = left_code.strip().split("\n") if left_code.strip() else []
    
    # If left is 0, skip right and result is 0
    assembly_lines.append(f"    cbz {left_reg}, {label_end}")
    
    # Evaluate right operand
    right_code, next_offset, right_reg = generate_expression_code(right, var_offsets, next_offset)
    right_lines = right_code.strip().split("\n") if right_code.strip() else []
    assembly_lines.extend(right_lines)
    
    # Result is in right_reg, move to x0 if needed
    if right_reg != "x0":
        assembly_lines.append(f"    mov x0, {right_reg}")
    
    assembly_lines.append(f"{label_end}:")
    
    assembly_code = "\n".join(assembly_lines) + "\n" if assembly_lines else ""
    return assembly_code, next_offset, "x0"

def _handle_logical_or(left: Expr, right: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate short-circuit code for logical OR (||)."""
    label_end = f"__or_end_{next_offset}"
    
    # Evaluate left operand
    left_code, next_offset, left_reg = generate_expression_code(left, var_offsets, next_offset)
    assembly_lines = left_code.strip().split("\n") if left_code.strip() else []
    
    # If left is non-zero, skip right and result is 1 (true)
    assembly_lines.append(f"    cbnz {left_reg}, {label_end}")
    
    # Evaluate right operand
    right_code, next_offset, right_reg = generate_expression_code(right, var_offsets, next_offset)
    right_lines = right_code.strip().split("\n") if right_code.strip() else []
    assembly_lines.extend(right_lines)
    
    # Result is in right_reg, move to x0 if needed
    if right_reg != "x0":
        assembly_lines.append(f"    mov x0, {right_reg}")
    
    assembly_lines.append(f"{label_end}:")
    
    assembly_code = "\n".join(assembly_lines) + "\n" if assembly_lines else ""
    return assembly_code, next_offset, "x0"

# === OOP compatibility layer ===
# Not needed for this function node
