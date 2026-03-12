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
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": "ASSIGN",
#   "target": str,
#   "value": dict,
# }

# === main function ===
def handle_assign(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle ASSIGN statement code generation for ARM32 assembly."""
    target = stmt["target"]
    value_expr = stmt["value"]
    
    # Look up target variable offset; raise ValueError if undefined
    if target not in var_offsets:
        raise ValueError(f"Undefined variable: {target}")
    
    target_offset = var_offsets[target]
    
    # Evaluate value expression into r0
    eval_code, eval_offset = evaluate_expression(value_expr, func_name, label_counter, var_offsets, next_offset)
    
    # Store r0 to variable stack location
    store_instr = f"str r0, [sp, #{target_offset}]"
    
    # Combine assembly code
    assembly_code = eval_code + store_instr + "\n"
    
    # Offset does not change for assignment (value already evaluated)
    return (assembly_code, eval_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node