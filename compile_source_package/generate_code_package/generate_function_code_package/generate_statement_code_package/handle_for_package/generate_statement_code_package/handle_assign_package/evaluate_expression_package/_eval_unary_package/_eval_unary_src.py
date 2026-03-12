# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..evaluate_expression_src import evaluate_expression

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields (for UNARY):
# {
#   "type": "UNARY",
#   "op": str,             # "-" (negation) or "!" (logical NOT)
#   "operand": dict,       # nested expression
# }

# === main function ===
def _eval_unary(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Evaluate UNARY expression and generate ARM assembly code."""
    # Validate required fields
    if "op" not in expr:
        raise ValueError("Missing required field: 'op'")
    if "operand" not in expr:
        raise ValueError("Missing required field: 'operand'")
    
    op = expr["op"]
    operand = expr["operand"]
    
    # Recursively evaluate operand
    operand_code, operand_offset, _ = evaluate_expression(
        operand, func_name, label_counter, var_offsets, next_offset
    )
    
    # Generate unary operation code
    if op == "-":
        # Negation: RSB R0, R0, #0 (Reverse Subtract: 0 - R0)
        unary_code = "RSB R0, R0, #0"
    elif op == "!":
        # Logical NOT: CMP R0, #0; MOVEQ R0, #1; MOVNE R0, #0
        unary_code = "CMP R0, #0\nMOVEQ R0, #1\nMOVNE R0, #0"
    else:
        raise ValueError(f"Unsupported unary operator: {op}")
    
    # Combine code
    if operand_code:
        full_code = operand_code + "\n" + unary_code
    else:
        full_code = unary_code
    
    # Unary operation itself does not allocate stack space
    offset_delta = operand_offset
    
    return (full_code, offset_delta, "R0")

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed: this is a helper function node, not a framework entry point
