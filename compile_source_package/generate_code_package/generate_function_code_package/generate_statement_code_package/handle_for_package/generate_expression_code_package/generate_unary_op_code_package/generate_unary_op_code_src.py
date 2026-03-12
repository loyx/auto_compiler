# === std / third-party imports ===
from typing import Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "counter": int,
# }

# === main function ===
def generate_unary_op_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a UNARY_OP expression."""
    operator = expr["operator"]
    operand = expr["operand"]
    
    # Recursively process the operand expression
    operand_code, updated_offset = generate_expression_code(
        operand,
        func_name,
        label_counter,
        var_offsets,
        next_offset
    )
    
    # Apply the unary operator to the result (already in x0)
    if operator == "-":
        code = operand_code + "    neg x0, x0\n"
    elif operator == "!":
        code = operand_code + "    cmp x0, #0\n    cset x0, eq\n"
    elif operator == "~":
        code = operand_code + "    mvn x0, x0\n"
    else:
        raise ValueError(f"Unknown unary operator: {operator}")
    
    return code, updated_offset

# === helper functions ===

# === OOP compatibility layer ===
