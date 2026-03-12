# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "literal", "variable", "binary_op", "unary_op", "call"
#   "value": Any,          # for literal
#   "name": str,           # for variable
#   "operator": str,       # for binary_op/unary_op
#   "left": dict,          # for binary_op
#   "right": dict,         # for binary_op
#   "operand": dict,       # for unary_op
#   "function": str,       # for call
#   "args": list,          # for call
# }

# === main function ===
def _handle_binary_op(operator: str, left: dict, right: dict, var_offsets: Dict[str, int], next_offset: int) -> Tuple[str, int, int]:
    """
    Generate assembly code for binary operations.
    
    Recursively generates code for left and right operands, then emits
    the appropriate BINARY_OP instruction.
    """
    # Generate left operand code
    left_code, left_offset, next_offset = generate_expression_code(left, var_offsets, next_offset)
    
    # Generate right operand code
    right_code, right_offset, next_offset = generate_expression_code(right, var_offsets, next_offset)
    
    # Map operator to instruction
    if operator not in BINARY_OP_MAP:
        raise ValueError(f"Unsupported binary operator: {operator}")
    
    instruction = BINARY_OP_MAP[operator]
    
    # Assemble final code
    code = left_code + right_code + f"{instruction}\n"
    
    # Result is at left_offset slot (right value consumed by BINARY_OP)
    return code, left_offset, next_offset

# === helper functions ===

# === OOP compatibility layer ===

# Binary operator to assembly instruction mapping
BINARY_OP_MAP: Dict[str, str] = {
    "+": "BINARY_ADD",
    "-": "BINARY_SUBTRACT",
    "*": "BINARY_MULTIPLY",
    "/": "BINARY_DIVIDE",
    "//": "BINARY_FLOOR_DIVIDE",
    "%": "BINARY_MODULO",
    "**": "BINARY_POWER",
    "==": "BINARY_EQUAL",
    "!=": "BINARY_NOT_EQUAL",
    "<": "BINARY_LESS_THAN",
    "<=": "BINARY_LESS_EQUAL",
    ">": "BINARY_GREATER_THAN",
    ">=": "BINARY_GREATER_EQUAL",
    "&": "BINARY_AND",
    "|": "BINARY_OR",
    "^": "BINARY_XOR",
    "<<": "BINARY_LSHIFT",
    ">>": "BINARY_RSHIFT",
}
