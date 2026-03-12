# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions for this inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields (for IDENT):
# {
#   "type": "IDENT",
#   "name": str,           # variable name
# }

# === main function ===
def _eval_ident(expr: Expr, var_offsets: VarOffsets) -> Tuple[str, int, str]:
    """
    Evaluate IDENT expression and generate ARM assembly to load variable from stack.
    
    Args:
        expr: IDENT expression dict with 'type'='IDENT' and 'name' field
        var_offsets: Variable offset lookup {var_name: stack_offset}
    
    Returns:
        Tuple[str, int, str]: (generated_code, 0, "R0")
    
    Raises:
        ValueError: If 'name' field is missing or variable is undefined
    """
    # Extract variable name from expr
    if "name" not in expr:
        raise ValueError("Missing required field 'name' in IDENT expression")
    
    name = expr["name"]
    
    # Look up offset in var_offsets
    if name not in var_offsets:
        raise ValueError(f"Undefined variable: {name}")
    
    offset = var_offsets[name]
    
    # Emit LDR instruction to load from stack
    # Format: LDR R0, [SP, #{offset}]
    code = f"    LDR R0, [SP, #{offset}]"
    
    # Return tuple: (generated_code, 0, "R0")
    return (code, 0, "R0")

# === helper functions ===
# No helper functions needed for this simple implementation

# === OOP compatibility layer ===
# Not required for this function node