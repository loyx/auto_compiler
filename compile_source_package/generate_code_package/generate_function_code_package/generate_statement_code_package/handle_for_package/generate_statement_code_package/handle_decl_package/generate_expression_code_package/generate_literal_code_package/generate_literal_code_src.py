# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - this is a leaf node

# === ADT defines ===
Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "LITERAL",
#   "value": Any,        # int, float, bool (None not supported)
# }

# === main function ===
def generate_literal_code(expr: dict) -> Tuple[str, int]:
    """
    Generate ARM assembly code for LITERAL expressions.
    
    Args:
        expr: Dictionary with "type"="LITERAL" and "value" field.
              Value can be int, float, or bool. None is not supported.
    
    Returns:
        Tuple[code_string, result_register] where result_register is always 0 (R0)
    
    Raises:
        ValueError: If value is None or of unsupported type
    """
    value = expr.get("value")
    
    # Check for None explicitly
    if value is None:
        raise ValueError("None is not supported as a literal value")
    
    # Handle bool (must check before int since bool is subclass of int)
    if isinstance(value, bool):
        int_value = 1 if value else 0
        code = f"MOV R0, #{int_value}"
        return (code, 0)
    
    # Handle int
    if isinstance(value, int):
        if -4095 <= value <= 4095:
            code = f"MOV R0, #{value}"
        else:
            code = f"LDR R0, ={value}"
        return (code, 0)
    
    # Handle float
    if isinstance(value, float):
        code = f"LDR R0, ={value}"
        return (code, 0)
    
    # Unsupported type
    raise ValueError(f"Unsupported literal value type: {type(value).__name__}")

# === helper functions ===
# No helper functions needed - logic is simple and inline

# === OOP compatibility layer ===
# Not needed - this is a pure function node, no framework requires class wrapper
