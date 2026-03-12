# === std / third-party imports ===
from typing import Tuple, Dict, Any

# === sub function imports ===
# No subfunctions needed

# === ADT defines ===
Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "LITERAL"
#   "value": int or bool,
#   "literal_type": str  # "int" or "bool"
# }

# === main function ===
def generate_literal_code(expr: Expr, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a LITERAL expression."""
    literal_type = expr["literal_type"]
    value = expr["value"]
    
    if literal_type == "bool":
        code = f"mov x0, #{1 if value else 0}"
    elif literal_type == "int":
        code = f"mov x0, #{value}"
    else:
        raise ValueError(f"Unknown literal type: {literal_type}")
    
    return (code, next_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
