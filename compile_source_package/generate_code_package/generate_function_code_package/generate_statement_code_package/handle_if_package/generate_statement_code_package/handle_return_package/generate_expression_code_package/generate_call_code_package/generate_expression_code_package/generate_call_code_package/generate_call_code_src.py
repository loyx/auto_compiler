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

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,       # expression type: "CALL", "VAR", "NUM", etc.
#   "func_name": str,  # for CALL type
#   "args": list,      # for CALL type
#   "name": str,       # for VAR type
#   "value": int,      # for NUM type
# }

# === main function ===
def generate_call_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generates ARM64 assembly code for CALL type expressions."""
    # Step 1: Validate func_name exists
    if "func_name" not in expr:
        raise ValueError("CALL expression missing func_name field")
    
    func_name = expr["func_name"]
    
    # Step 2: Extract args list (default to empty list)
    args = expr.get("args", [])
    
    # Step 3: Validate args count <= 8
    if len(args) > 8:
        raise ValueError("Too many arguments (max 8)")
    
    # Step 4: Initialize code string and current_offset
    code = ""
    current_offset = next_offset
    
    # Step 5: Process each argument
    for i, arg_expr in enumerate(args):
        # Recursively evaluate argument expression
        arg_code, updated_offset, arg_reg = generate_expression_code(arg_expr, var_offsets, current_offset)
        code += arg_code
        
        # Move result to argument register x0-x7
        if i < 8:
            code += f"    mov x{i}, {arg_reg}\n"
        
        current_offset = updated_offset
    
    # Step 6: Generate call instruction
    code += f"    bl {func_name}\n"
    
    # Step 7: Return result
    return (code, current_offset, "x0")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
