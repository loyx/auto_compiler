# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# generate_expression_code is the parent dispatcher, imported from parent module
from ..generate_expression_code_src import generate_expression_code

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

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,
#   "operator": str,  # For UNARY_OP: "-" (negation), "!" (logical not), "~" (bitwise not)
#   "operand": Dict,  # For UNARY_OP - nested expression
# }

# === main function ===
def generate_unary_op_code(
    expr: dict,
    func_name: str,
    label_counter: dict,
    var_offsets: dict,
    next_offset: int
) -> Tuple[str, int]:
    """Generate ARM assembly code for unary operations (-, !, ~)."""
    operator = expr["operator"]
    operand = expr["operand"]
    
    # Recursively process operand
    operand_code, next_offset = generate_expression_code(
        operand, func_name, label_counter, var_offsets, next_offset
    )
    
    # Generate operator-specific instruction
    if operator == "-":
        op_code = "    NEG x0, x0\n"
    elif operator == "!":
        op_code = "    CMP x0, #0\n    CSET x0, EQ\n"
    elif operator == "~":
        op_code = "    MVN x0, x0\n"
    else:
        raise ValueError(f"Unknown unary operator: {operator}")
    
    return operand_code + op_code, next_offset

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a compiler code generation function
