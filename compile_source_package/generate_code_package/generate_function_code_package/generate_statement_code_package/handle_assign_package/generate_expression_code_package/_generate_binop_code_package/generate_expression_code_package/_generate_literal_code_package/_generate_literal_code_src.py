# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions required for this module

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields for LITERAL:
# {
#   "type": "LITERAL",
#   "value": int | bool,  # 字面量值 (整数或布尔)
#   "literal_type": str,  # "int" 或 "bool"
# }


# === main function ===
def _generate_literal_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """
    Generates ARM64 assembly code for literal values (int/bool).
    
    For literal_type == "int": generates 'mov x0, #value'
    For literal_type == "bool": generates 'mov x0, #1' (True) or 'mov x0, #0' (False)
    Result is placed in x0 register.
    Raises ValueError if literal_type is neither "int" nor "bool".
    """
    literal_type = expr.get("literal_type")
    value = expr.get("value")
    
    if literal_type == "int":
        return f"mov x0, #{value}"
    elif literal_type == "bool":
        int_value = 1 if value is True else 0
        return f"mov x0, #{int_value}"
    else:
        raise ValueError(f"Invalid literal_type: {literal_type}. Expected 'int' or 'bool'.")


# === helper functions ===
# No helper functions required for this module

# === OOP compatibility layer ===
# Not required for this function node (CLI/utility function)
