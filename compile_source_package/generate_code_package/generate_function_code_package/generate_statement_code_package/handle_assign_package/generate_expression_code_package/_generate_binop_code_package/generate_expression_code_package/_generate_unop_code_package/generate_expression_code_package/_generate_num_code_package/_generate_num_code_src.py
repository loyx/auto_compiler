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
# Expr possible fields for NUM:
# {
#   "type": "NUM",
#   "value": int,      # integer literal value
# }

# === main function ===
def _generate_num_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """
    Generates ARM64 assembly code for number literals.
    
    Extracts the integer value from expr["value"] and generates
    a move immediate instruction: mov x0, #value
    
    Args:
        expr: Expression dict with "type"="NUM", "value" (int)
        func_name: Current function name (not used for NUM)
        var_offsets: Variable offset mapping (not used for NUM)
    
    Returns:
        Assembly code string with the value loaded into x0
    
    Raises:
        KeyError: If "value" field is missing from expr
    """
    value = expr["value"]
    return f"mov x0, #{value}"

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
