# === std / third-party imports ===
from typing import Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
# No complex ADT needed - uses str only

# === main function ===
def _get_binary_op_instruction(op: str) -> str:
    """
    Returns ARM64 assembly instruction string for binary operator.
    
    Args:
        op: Binary operator name. Must be one of:
            - Comparison: "eq", "ne", "lt", "le", "gt", "ge"
            - Logical: "and", "or"
            - Arithmetic: "add", "sub", "mul", "div"
    
    Returns:
        ARM64 assembly instruction string
    
    Raises:
        ValueError: If operator is unknown
    
    Notes:
        - Assumes x1 contains left operand, x0 contains right operand on entry
        - Result is placed in x0 register
    """
    # Comparison operators mapping to ARM64 condition codes
    comparison_conditions: Dict[str, str] = {
        "eq": "eq",
        "ne": "ne",
        "lt": "lt",
        "le": "le",
        "gt": "gt",
        "ge": "ge",
    }
    
    # Check if comparison operator
    if op in comparison_conditions:
        cond = comparison_conditions[op]
        return f"cmp x1, x0\ncset x0, {cond}\n"
    
    # Logical operators
    logical_ops: Dict[str, str] = {
        "and": "and x0, x1, x0\n",
        "or": "orr x0, x1, x0\n",
    }
    
    if op in logical_ops:
        return logical_ops[op]
    
    # Arithmetic operators
    arithmetic_ops: Dict[str, str] = {
        "add": "add x0, x1, x0\n",
        "sub": "sub x0, x1, x0\n",
        "mul": "mul x0, x1, x0\n",
        "div": "udiv x0, x1, x0\n",
    }
    
    if op in arithmetic_ops:
        return arithmetic_ops[op]
    
    # Unknown operator
    raise ValueError(f"Unknown operator: {op}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a helper function, not a framework entry point
