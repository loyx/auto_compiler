# === std / third-party imports ===
from typing import Dict, Tuple

# === sub function imports ===
# No child functions needed for this inline implementation

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "skip": int,
#   "true": int,
#   "false": int,
# }

OperatorInstruction = Tuple[str, int]
# OperatorInstruction possible fields:
# {
#   "instruction_code": str,  # ARM assembly instruction string
#   "next_offset": int        # Updated stack offset (usually unchanged)
# }

# === main function ===
def generate_operator_instruction(operator: str, func_name: str, label_counter: dict, next_offset: int) -> Tuple[str, int]:
    """
    Generate ARM assembly instruction for a specific binary operator.
    
    Args:
        operator: Binary operator string (+, -, *, /, %, ==, !=, <, >, <=, >=, &&, ||, &, |, ^, <<, >>)
        func_name: Current function name for label naming (used in short-circuit labels)
        label_counter: Mutable label counter {label_type: count}, may be modified in-place
        next_offset: Current next available stack offset
    
    Returns:
        Tuple[str, int]: (instruction_code, next_offset)
    
    Raises:
        ValueError: For unknown operators
    """
    # Arithmetic operators
    if operator == "+":
        return "add x0, x1, x0", next_offset
    elif operator == "-":
        return "sub x0, x1, x0", next_offset
    elif operator == "*":
        return "mul x0, x1, x0", next_offset
    elif operator == "/":
        return "sdiv x0, x1, x0", next_offset
    elif operator == "%":
        # % requires sdiv + msub: x0 = x1 - (x1 / x0) * x0
        code = "sdiv x2, x1, x0\n    msub x0, x2, x0, x1"
        return code, next_offset
    
    # Comparison operators
    elif operator == "==":
        return "cmp x1, x0\n    cset x0, eq", next_offset
    elif operator == "!=":
        return "cmp x1, x0\n    cset x0, ne", next_offset
    elif operator == "<":
        return "cmp x1, x0\n    cset x0, lt", next_offset
    elif operator == ">":
        return "cmp x1, x0\n    cset x0, gt", next_offset
    elif operator == "<=":
        return "cmp x1, x0\n    cset x0, le", next_offset
    elif operator == ">=":
        return "cmp x1, x0\n    cset x0, ge", next_offset
    
    # Logical short-circuit operators
    elif operator == "&&":
        skip_count = label_counter.get("skip", 0)
        label = f"{func_name}_skip_{skip_count}"
        label_counter["skip"] = skip_count + 1
        # &&: if x0 is false (0), skip to label; else continue and mov result
        code = f"cbz x0, {label}\n    mov x0, x1\n{label}:"
        return code, next_offset
    elif operator == "||":
        skip_count = label_counter.get("skip", 0)
        label = f"{func_name}_skip_{skip_count}"
        label_counter["skip"] = skip_count + 1
        # ||: if x0 is true (non-zero), skip to label; else continue and mov result
        code = f"cbnz x0, {label}\n    mov x0, x1\n{label}:"
        return code, next_offset
    
    # Bitwise operators
    elif operator == "&":
        return "and x0, x1, x0", next_offset
    elif operator == "|":
        return "orr x0, x1, x0", next_offset
    elif operator == "^":
        return "eor x0, x1, x0", next_offset
    elif operator == "<<":
        return "lsl x0, x1, x0", next_offset
    elif operator == ">>":
        return "asr x0, x1, x0", next_offset
    
    # Unknown operator
    else:
        raise ValueError(f"Unknown binary operator: {operator}")

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not needed for this function node (not a framework entry point)
