# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub-functions needed for this simple evaluator

# === ADT defines ===
Expr = Dict[str, Any]
# Expr possible fields (for LITERAL):
# {
#   "type": "LITERAL",
#   "value": Any,          # int or bool (0/1)
# }

# === main function ===
def _eval_literal(expr: Expr) -> Tuple[str, int, str]:
    """
    Evaluate LITERAL expression and generate ARM assembly to load constant into R0.
    
    Args:
        expr: Dict with 'type'='LITERAL' and 'value' field (int or bool)
    
    Returns:
        Tuple[str, int, str]: (generated_code, offset_delta, register_name)
    
    Raises:
        ValueError: If 'value' field is missing or type is unsupported
    """
    # Check for required 'value' field
    if "value" not in expr or expr["value"] is None:
        raise ValueError("Missing required field 'value' in LITERAL expression")
    
    value = expr["value"]
    
    # Handle boolean values
    if isinstance(value, bool):
        int_value = 1 if value else 0
        code = f"    MOV R0, #{int_value}"
        return (code, 0, "R0")
    
    # Handle integer values
    if isinstance(value, int):
        code = f"    MOV R0, #{value}"
        return (code, 0, "R0")
    
    # Handle unsupported types
    type_name = type(value).__name__
    raise ValueError(f"Unsupported literal type: {type_name}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
