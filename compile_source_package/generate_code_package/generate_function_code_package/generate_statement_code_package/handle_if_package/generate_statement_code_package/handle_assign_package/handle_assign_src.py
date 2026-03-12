# === std / third-party imports ===
from typing import Dict, Tuple

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
#   "var_name": int,  # maps variable name to stack slot index
# }

Stmt = Dict[str, any]
# Stmt possible fields for ASSIGN:
# {
#   "type": "ASSIGN",
#   "target": str,      # Variable name to assign to
#   "value": dict,      # Expression dict (LITERAL/IDENT/BINARY/UNARY)
# }

# === main function ===
def handle_assign(stmt: Dict, func_name: str, label_counter: Dict, var_offsets: Dict, next_offset: int) -> Tuple[str, int]:
    """Handle ASSIGN statement: evaluate expression and store result to target variable's stack slot."""
    target_var = stmt["target"]
    expr = stmt["value"]
    
    # Allocate stack slot if variable is new
    if target_var not in var_offsets:
        var_offsets[target_var] = next_offset
        next_offset += 1
    
    # Generate expression evaluation code
    expr_code, next_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
    
    # Generate store instruction (convert slot index to byte offset)
    byte_offset = var_offsets[target_var] * 8
    store_code = f"    str {result_reg}, [sp, #{byte_offset}]"
    
    # Combine code
    if expr_code:
        full_code = expr_code + "\n" + store_code
    else:
        full_code = store_code
    
    return (full_code, next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
