# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

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

Stmt = Dict[str, Any]
# Stmt possible fields for ASSIGN:
# {
#   "type": "ASSIGN",
#   "target": str,       # target variable name
#   "var_name": str,     # alternative field name for target
#   "value": dict        # expression tree to evaluate
# }

# === main function ===
def handle_assign(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for an ASSIGN statement."""
    var_name = stmt.get("target") or stmt.get("var_name")
    value_expr = stmt.get("value")
    
    if var_name not in var_offsets:
        raise ValueError(f"Undefined variable: {var_name}")
    
    offset = var_offsets[var_name]
    expr_code, updated_offset, result_reg = evaluate_expression(
        value_expr, func_name, label_counter, var_offsets, next_offset
    )
    
    store_instr = f"    STR {result_reg}, [SP, #-{offset}]\n"
    return (expr_code + store_instr, updated_offset)

# === helper functions ===
# No helper functions needed; logic delegated to evaluate_expression

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
