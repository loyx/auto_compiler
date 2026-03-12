# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions needed for this simple logic

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # maps variable name to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "IDENTIFIER",
#   "name": str,        # variable name
#   "var_type": str,    # "int", "char", "short", "float", "long", "pointer", "double"
# }

# === main function ===
def generate_identifier_code(expr: dict, var_offsets: dict) -> Tuple[str, int]:
    """
    Generate ARM assembly code for IDENTIFIER expressions.
    
    Loads a variable from the stack based on its type.
    Returns Tuple[assembly_code_string, result_register].
    """
    # Validate required field
    if "name" not in expr:
        raise KeyError("Missing field: name")
    
    var_name = expr["name"]
    
    # Validate variable exists in offsets
    if var_name not in var_offsets:
        raise KeyError(f"Variable '{var_name}' not found in var_offsets")
    
    offset = var_offsets[var_name]
    
    # Determine var_type (default to "int")
    var_type = expr.get("var_type", "int")
    
    # Select load instruction based on type
    if var_type == "char":
        instruction = f"LDRB R0, [SP, #{offset}]"
    elif var_type == "short":
        instruction = f"LDRH R0, [SP, #{offset}]"
    else:
        # int, float, long, pointer, double, and default
        instruction = f"LDR R0, [SP, #{offset}]"
    
    return (instruction, 0)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node