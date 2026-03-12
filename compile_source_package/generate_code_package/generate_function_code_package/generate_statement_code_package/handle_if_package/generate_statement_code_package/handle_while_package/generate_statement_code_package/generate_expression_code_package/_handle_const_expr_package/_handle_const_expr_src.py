# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub functions needed for this simple helper

# === ADT defines ===
Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "CONST" | "VAR" | "BINOP" | "UNOP"
#   "value": int,          # for CONST: integer value
#   "name": str,           # for VAR: variable name
#   "op": str,             # for BINOP/UNOP: operator string
#   "left": dict,          # for BINOP: left operand expr dict
#   "right": dict,         # for BINOP: right operand expr dict
#   "operand": dict,       # for UNOP: operand expr dict
# }

# === main function ===
def _handle_const_expr(expr: Expr, next_reg: int) -> Tuple[str, str, int]:
    """Generate ARM64 assembly code for a CONST expression.
    
    Args:
        expr: Expression dict with "type"="CONST" and "value" field
        next_reg: Next available register index (1-15)
    
    Returns:
        Tuple of (assembly_code, result_register_name, next_reg+1)
    """
    value = expr["value"]
    reg_name = f"x{next_reg}"
    code = f"    mov {reg_name}, #{value}"
    return (code, reg_name, next_reg + 1)

# === helper functions ===
# No additional helpers needed

# === OOP compatibility layer ===
# Not needed for this helper function
