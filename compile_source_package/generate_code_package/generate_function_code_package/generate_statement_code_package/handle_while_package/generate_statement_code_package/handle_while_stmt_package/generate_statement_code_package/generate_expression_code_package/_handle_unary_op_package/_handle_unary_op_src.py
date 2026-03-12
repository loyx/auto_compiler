# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No sub-functions imported; recurse_fn is passed as callback from parent

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
def _handle_unary_op(
    operator: str,
    operand: dict,
    var_offsets: VarOffsets,
    next_offset: int,
    recurse_fn: callable
) -> Tuple[str, int, int]:
    """
    Generate assembly code for unary operations.
    
    Calls recurse_fn to generate operand code, then emits UNARY_OP instruction.
    Result stays at the same offset where operand was placed.
    """
    # Recursively generate code for operand
    operand_code, operand_offset, updated_offset = recurse_fn(
        operand, var_offsets, next_offset
    )
    
    # Emit UNARY_OP instruction
    unary_instruction = f"UNARY_OP {operator}\n"
    combined_code = operand_code + unary_instruction
    
    # Result stays at operand's offset
    return (combined_code, operand_offset, updated_offset)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
