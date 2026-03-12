# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions delegated

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
#   "type": "VAR_DECL",
#   "name": str,
#   "init": dict (optional),
# }

# === main function ===
def handle_var_decl(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """
    Handle VAR_DECL statement code generation for ARM32 assembly.
    
    Allocates stack space for a variable, optionally initializes it,
    and updates the variable offset mapping.
    """
    # Extract variable name
    var_name = stmt["name"]
    
    # Assign current next_offset to this variable
    var_offset = next_offset
    
    # Add to var_offsets dict (modifies in-place)
    var_offsets[var_name] = var_offset
    
    # Build assembly code
    assembly_lines = []
    
    # Add comment for clarity
    assembly_lines.append(f"@ declare variable {var_name} at offset {var_offset}")
    
    # If initialization expression exists, generate code to evaluate and store
    if "init" in stmt and stmt["init"] is not None:
        init_expr = stmt["init"]
        # Generate code to evaluate init expression into r0
        # (assuming init expr evaluation returns value in r0)
        assembly_lines.append(f"    @ evaluate init expression for {var_name}")
        assembly_lines.append(f"    MOV r0, #{init_expr.get('value', 0)}")
        # Store r0 to stack at [sp, #offset]
        assembly_lines.append(f"    STR r0, [sp, #{var_offset}]")
    
    # Increment next_offset by 4 (32-bit word)
    updated_offset = next_offset + 4
    
    # Join assembly lines
    assembly_code = "\n".join(assembly_lines)
    
    return (assembly_code, updated_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
