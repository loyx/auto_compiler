# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_cond": int,
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": "RETURN",
#   "value": dict (optional),
# }

# === main function ===
def handle_return(stmt: Stmt, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle RETURN statement ARM32 code generation."""
    if "value" not in stmt or stmt["value"] is None:
        # Void return - generate comment marker only
        return "@ return void\n", next_offset

    # Evaluate return value expression
    expr_code, expr_offset, result_reg = evaluate_expression(
        stmt["value"], var_offsets, next_offset
    )

    # Ensure result is in r0
    if result_reg != "r0":
        move_code = f"MOV r0, {result_reg}\n"
        return expr_code + move_code + "@ return\n", expr_offset
    else:
        return expr_code + "@ return\n", expr_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
