# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..generate_expression_code_src import generate_expression_code

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

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

CallExpr = Dict[str, Any]
# CallExpr possible fields:
# {
#   "type": str,  # "CALL"
#   "callee": str,  # function name to call
#   "args": list,  # list of expression dicts
# }

# === main function ===
def generate_call_code(expr: CallExpr, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a CALL expression."""
    callee = expr["callee"]
    args = expr["args"]
    
    if len(args) > 8:
        raise ValueError(f"Function call exceeds maximum 8 arguments: {len(args)}")
    
    code_lines = []
    
    # Generate code for each argument, save results to stack
    for i, arg_expr in enumerate(args):
        arg_code, next_offset = generate_expression_code(arg_expr, func_name, label_counter, var_offsets, next_offset)
        code_lines.append(arg_code)
        # Save argument result to stack slot
        code_lines.append("str x0, [sp, #-16]!")
    
    # Load arguments from stack into x0-x7 registers (in reverse order to restore correctly)
    for i in range(len(args) - 1, -1, -1):
        code_lines.append(f"ldr x{i}, [sp], #16")
    
    # Call the function
    code_lines.append(f"bl {callee}")
    
    # Result is already in x0
    
    return "\n".join(code_lines), next_offset

# === helper functions ===

# === OOP compatibility layer ===
