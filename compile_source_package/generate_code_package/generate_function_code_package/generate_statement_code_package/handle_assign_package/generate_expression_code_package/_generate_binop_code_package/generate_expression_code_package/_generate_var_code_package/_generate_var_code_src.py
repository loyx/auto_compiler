# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple code generation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields for VAR:
# {
#   "type": "VAR",
#   "name": str,  # 变量名
# }

# === main function ===
def _generate_var_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """
    Generates ARM64 assembly code for variable references.
    
    Looks up the variable name in var_offsets to get the stack offset,
    then generates 'ldr x0, [sp, #offset]' instruction.
    
    Args:
        expr: VAR expression dict with "name" field
        func_name: Current function name (not used, passed for consistency)
        var_offsets: Variable offset mapping from names to stack offsets
        
    Returns:
        ARM64 assembly string with result in x0 register
        
    Raises:
        KeyError: If "name" field missing or variable not in var_offsets
    """
    # Validate required field
    if "name" not in expr:
        raise KeyError("Missing required field 'name' in VAR expression")
    
    var_name = expr["name"]
    
    # Look up offset
    if var_name not in var_offsets:
        raise KeyError(f"Variable '{var_name}' not found in var_offsets")
    
    offset = var_offsets[var_name]
    
    # Generate ARM64 load instruction
    return f"ldr x0, [sp, #{offset}]"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this internal code generation function
