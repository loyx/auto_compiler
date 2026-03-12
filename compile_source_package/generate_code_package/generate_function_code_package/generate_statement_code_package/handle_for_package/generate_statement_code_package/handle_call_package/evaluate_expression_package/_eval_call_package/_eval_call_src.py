# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # offset from base pointer for variable
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
def _eval_call(func_name: str, arguments: list, var_offsets: dict) -> str:
    """Generate ARM assembly for function call expression."""
    if not arguments:
        return f"BL {func_name}"
    
    instructions = []
    num_args = len(arguments)
    stack_arg_count = max(0, num_args - 4)
    stack_bytes = stack_arg_count * 4
    
    # Evaluate first 4 arguments into R0-R3
    for i in range(min(4, num_args)):
        arg_asm = evaluate_expression(arguments[i], var_offsets)
        instructions.append(arg_asm)
        if i < 3:
            # Save R0 to R{i} for subsequent args
            instructions.append(f"MOV R{i}, R0")
    
    # Evaluate remaining arguments and push to stack (reverse order)
    if stack_arg_count > 0:
        for i in range(num_args - 1, 3, -1):
            arg_asm = evaluate_expression(arguments[i], var_offsets)
            instructions.append(arg_asm)
            instructions.append("PUSH {R0}")
    
    # Call the function
    instructions.append(f"BL {func_name}")
    
    # Stack cleanup
    if stack_bytes > 0:
        instructions.append(f"ADD SP, SP, #{stack_bytes}")
    
    return "\n".join(instructions)

# === helper functions ===

# === OOP compatibility layer ===
