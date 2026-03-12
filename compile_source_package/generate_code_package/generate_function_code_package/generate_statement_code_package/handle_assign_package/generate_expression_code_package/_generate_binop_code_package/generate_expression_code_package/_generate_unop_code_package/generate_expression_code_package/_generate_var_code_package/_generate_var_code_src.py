# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions for this module

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
#   "name": str,       # variable name
# }

# === main function ===
def _generate_var_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """
    Generates ARM64 assembly code for variable access.
    
    Extracts variable name from expr["name"], looks up stack offset
    from var_offsets, and generates load instruction.
    
    Args:
        expr: Expression dict with "type"="VAR", "name" (str)
        func_name: Current function name (not used for VAR, kept for signature consistency)
        var_offsets: Variable offset mapping from names to stack offsets
    
    Returns:
        Assembly code string with variable value loaded into x0
    
    Raises:
        KeyError: If "name" field missing from expr or variable not in var_offsets
    """
    # Extract variable name from expression
    var_name = expr["name"]
    
    # Look up stack offset for this variable
    offset = var_offsets[var_name]
    
    # Generate ARM64 load instruction
    return f"ldr x0, [sp, #{offset}]"

# === helper functions ===
# No helper functions needed for this simple module

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node, not a framework entry point
