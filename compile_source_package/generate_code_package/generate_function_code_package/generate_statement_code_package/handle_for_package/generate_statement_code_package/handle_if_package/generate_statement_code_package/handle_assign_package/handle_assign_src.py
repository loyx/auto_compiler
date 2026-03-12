# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
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
#   "type": str,
#   "var_name": str,
#   "expression": dict,
# }

# === main function ===
def handle_assign(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle ASSIGN statement code generation.
    
    Evaluates expression (result in R0), stores to variable's stack slot via STR.
    Returns Tuple[asm_code, updated_offset].
    """
    var_name = stmt["var_name"]
    offset = var_offsets[var_name]
    
    expr_code, new_offset = generate_expression_code(
        stmt["expression"], func_name, label_counter, var_offsets, next_offset
    )
    
    store_instr = f"STR R0, [FP, #{offset}]"
    asm_code = expr_code + "\n" + store_instr
    
    return asm_code, new_offset

# === helper functions ===

# === OOP compatibility layer ===
