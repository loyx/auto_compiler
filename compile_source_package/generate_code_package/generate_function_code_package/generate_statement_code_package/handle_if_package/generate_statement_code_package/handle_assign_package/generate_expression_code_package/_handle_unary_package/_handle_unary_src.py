# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..generate_expression_code_src import generate_expression_code

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
# Unary ops: "-", "!"

# === main function ===
def _handle_unary(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate assembly code for UNARY expression."""
    op = expr["op"]
    operand = expr["operand"]
    
    # Recursively generate code for the operand
    operand_code, next_offset, operand_reg = generate_expression_code(
        operand, var_offsets, next_offset
    )
    
    lines = [operand_code] if operand_code else []
    
    if op == "-":
        # Negation
        if operand_reg != "x0":
            lines.append(f"    mov x0, {operand_reg}")
        lines.append("    neg x0, x0")
    elif op == "!":
        # Logical not
        if operand_reg != "x0":
            lines.append(f"    mov x0, {operand_reg}")
        lines.append("    cmp x0, #0")
        lines.append("    cset x0, eq")
    else:
        raise ValueError(f"Unsupported unary operator: {op}")
    
    combined_code = "\n".join(line for line in lines if line)
    return (combined_code, next_offset, "x0")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this handler function
