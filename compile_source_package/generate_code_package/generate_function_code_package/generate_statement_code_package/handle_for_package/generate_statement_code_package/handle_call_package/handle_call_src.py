# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for CALL:
# {
#   "type": "CALL",
#   "func_name": str,
#   "arguments": list
# }

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": "literal"|"identifier"|"binary"|"unary"|"call",
#   "value": Any (for literal),
#   "name": str (for identifier),
#   "op": str (for binary/unary),
#   "left": Expression (for binary),
#   "right": Expression (for binary),
#   "operand": Expression (for unary),
#   "func_name": str (for call),
#   "arguments": list (for call)
# }

# === main function ===
def handle_call(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a CALL statement."""
    if "func_name" not in stmt:
        raise ValueError("CALL statement missing func_name field")
    
    lines = []
    target_func = stmt["func_name"]
    args = stmt.get("arguments", [])
    num_args = len(args)
    stack_arg_count = max(0, num_args - 4)
    
    # Track if we need to save registers for complex expression evaluation
    needs_save = False
    
    # Evaluate each argument and place in R0-R3 or push to stack
    for i, arg in enumerate(args):
        # Evaluate expression, result ends up in R0
        arg_code = evaluate_expression(arg, var_offsets)
        lines.append(arg_code)
        
        if i < 4:
            # Place in R0-R3
            if i > 0:
                lines.append(f"MOV R{i}, R0")
        else:
            # Push to stack for arguments beyond R0-R3
            lines.append("PUSH {R0}")
    
    # Call the function
    lines.append(f"BL {target_func}")
    
    # Clean up stack arguments (caller responsibility)
    if stack_arg_count > 0:
        lines.append(f"ADD SP, SP, #{stack_arg_count * 4}")
    
    code = "\n".join(lines)
    return code, next_offset

# === helper functions ===

# === OOP compatibility layer ===
