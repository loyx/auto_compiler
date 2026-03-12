# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,       # statement type, e.g., "ASSIGN"
#   "target": str,     # variable name for ASSIGN
#   "value": dict,     # expression dict for ASSIGN
# }

# === main function ===
def handle_assign_stmt(stmt: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Handle ASSIGN statement.
    
    1. Generate code for the value expression (RHS evaluated first)
    2. Allocate stack offset for target variable if it's new
    3. Emit STORE_OFFSET instruction to store the value
    4. Return (assembly_code, updated_next_offset)
    
    Modifies var_offsets in-place for new variables.
    """
    target = stmt["target"]
    value = stmt["value"]
    
    # Generate code for the expression first (RHS)
    expr_code, next_offset = generate_expression_code(value, var_offsets, next_offset)
    
    # Allocate offset for target if it's a new variable
    if target not in var_offsets:
        var_offsets[target] = next_offset
        next_offset += 8  # ARM64 stack slot size: 8 bytes per variable
    
    # Generate STORE instruction
    offset = var_offsets[target]
    store_code = f"STORE_OFFSET {offset}\n"
    
    return expr_code + store_code, next_offset

# === helper functions ===

# === OOP compatibility layer ===
