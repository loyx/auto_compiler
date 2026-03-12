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
#   "type": "CALL",
#   "func_name": str,      # function name to call
#   "args": list,          # list of argument expression dicts
# }

# === main function ===
def generate_call_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate ARM64 code for CALL expression type."""
    # Extract func_name
    func_name = expr.get("func_name")
    if func_name is None:
        raise ValueError("CALL expression missing func_name field")
    
    # Extract args (default to empty list)
    args = expr.get("args", [])
    
    # Validate argument count
    if len(args) > 8:
        raise ValueError("Too many arguments (max 8)")
    
    # Define parameter registers
    param_registers = ["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7"]
    
    # Generate code for each argument
    code_lines = []
    current_offset = next_offset
    
    for i, arg_expr in enumerate(args):
        target_reg = param_registers[i]
        
        # Recursively generate code for argument
        arg_code, current_offset, result_reg = generate_expression_code(
            arg_expr, var_offsets, current_offset
        )
        
        # Accumulate argument code
        code_lines.append(arg_code)
        
        # Move to target register if needed
        if result_reg != target_reg:
            code_lines.append(f"    mov {target_reg}, {result_reg}\n")
    
    # Generate function call instruction
    code_lines.append(f"    bl {func_name}\n")
    
    # Combine all code
    combined_code = "".join(code_lines)
    
    # Return result (x0 is always the result register per ARM64 convention)
    return (combined_code, current_offset, "x0")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
