# === std / third-party imports ===
from typing import Dict

# === sub function imports ===
# No child functions needed for this simple mapping logic

# === ADT defines ===
# No special ADT types needed - uses basic string types
# OperatorMapping possible fields:
# {
#   "operator_name": str,  # e.g., "ADD", "EQ", "BITWISE_AND"
#   "instruction": str     # e.g., "add", "cmp", "and"
# }

# === main function ===
def generate_arithmetic_comparison_code(operator: str, left_code: str, right_code: str) -> str:
    """
    Generate ARM64 assembly instruction for arithmetic, comparison, or bitwise operations.
    
    Assumptions:
    - Left operand value is already in register x1
    - Right operand value is already in register x0
    - Result must end up in register x0
    
    Args:
        operator: Operation type (ADD, SUB, MUL, DIV, MOD, EQ, NE, LT, LE, GT, GE, 
                  BITWISE_AND, BITWISE_OR, BITWISE_XOR)
        left_code: Already generated assembly code for left operand (not used directly)
        right_code: Already generated assembly code for right operand (not used directly)
    
    Returns:
        Assembly instruction string with proper indentation
    """
    # Arithmetic operations: result = x1 op x0, store in x0
    arithmetic_map: Dict[str, str] = {
        "ADD": "add",
        "SUB": "sub",
        "MUL": "mul",
        "DIV": "udiv",
        "MOD": "urem",
    }
    
    # Bitwise operations: result = x1 op x0, store in x0
    bitwise_map: Dict[str, str] = {
        "BITWISE_AND": "and",
        "BITWISE_OR": "orr",
        "BITWISE_XOR": "eor",
    }
    
    # Comparison operations: use cmp + cset
    comparison_map: Dict[str, str] = {
        "EQ": "eq",
        "NE": "ne",
        "LT": "lt",
        "LE": "le",
        "GT": "gt",
        "GE": "ge",
    }
    
    # Handle arithmetic operations
    if operator in arithmetic_map:
        instr = arithmetic_map[operator]
        return f"    {instr} x0, x1, x0"
    
    # Handle bitwise operations
    if operator in bitwise_map:
        instr = bitwise_map[operator]
        return f"    {instr} x0, x1, x0"
    
    # Handle comparison operations
    if operator in comparison_map:
        condition = comparison_map[operator]
        cmp_instr = "    cmp x1, x0"
        cset_instr = f"    cset x0, {condition}"
        return f"{cmp_instr}\n{cset_instr}"
    
    # Unknown operator - raise error
    raise ValueError(f"Unsupported operator: {operator}")

# === helper functions ===
# No helper functions needed for this simple mapping logic

# === OOP compatibility layer ===
# Not needed - this is a pure function node, not a framework entry point
