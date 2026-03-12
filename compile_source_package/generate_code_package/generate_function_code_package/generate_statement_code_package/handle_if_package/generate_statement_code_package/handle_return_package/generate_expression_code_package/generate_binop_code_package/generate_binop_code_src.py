# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ...generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "BINOP",
#   "op": "ADD" | "SUB" | "MUL" | "DIV",
#   "left": Expr,     # left operand expression dict
#   "right": Expr,    # right operand expression dict
# }

# === main function ===
def generate_binop_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate ARM64 code for BINOP expression type.
    
    Recursively evaluates left/right operands, applies operation, result in x0.
    Raises ValueError for unsupported operators.
    """
    # Extract operands and operator
    left_expr = expr["left"]
    right_expr = expr["right"]
    op = expr["op"]
    
    # Recursively generate code for left operand
    left_code, next_offset, left_reg = generate_expression_code(
        left_expr, var_offsets, next_offset
    )
    
    # Recursively generate code for right operand
    right_code, next_offset, right_reg = generate_expression_code(
        right_expr, var_offsets, next_offset
    )
    
    # Map operation to ARM64 instruction
    op_map = {
        "ADD": "add",
        "SUB": "sub",
        "MUL": "mul",
        "DIV": "sdiv"
    }
    
    if op not in op_map:
        raise ValueError(f"Unsupported binary operator: {op}")
    
    instruction = op_map[op]
    
    # Generate operation instruction (result in x0)
    result_reg = "x0"
    binop_instruction = f"    {instruction} {result_reg}, {left_reg}, {right_reg}\n"
    
    # Combine all code
    assembly_code = left_code + right_code + binop_instruction
    
    return (assembly_code, next_offset, result_reg)

# === helper functions ===

# === OOP compatibility layer ===
