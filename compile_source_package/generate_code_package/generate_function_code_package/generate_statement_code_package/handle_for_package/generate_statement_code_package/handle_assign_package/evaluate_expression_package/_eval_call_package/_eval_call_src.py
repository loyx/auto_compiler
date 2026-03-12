# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..evaluate_expression_src import evaluate_expression

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

Expr = Dict[str, Any]
# Expr possible fields (for CALL):
# {
#   "type": "CALL",
#   "func_name": str,
#   "arguments": list,
# }

# === main function ===
def _eval_call(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Evaluate CALL expression and generate ARM assembly for function call."""
    if "func_name" not in expr:
        raise ValueError("CALL expression missing 'func_name' field")
    if "arguments" not in expr:
        raise ValueError("CALL expression missing 'arguments' field")
    
    callee = expr["func_name"]
    arguments = expr["arguments"]
    
    code_lines = []
    arg_count = len(arguments)
    num_stack_args = max(0, arg_count - 4)
    
    # Evaluate first 4 arguments left-to-right, place in R0-R3
    for i in range(min(4, arg_count)):
        arg_code, _, arg_reg = evaluate_expression(arguments[i], func_name, label_counter, var_offsets, next_offset)
        code_lines.append(arg_code)
        if i > 0:
            code_lines.append(f"    MOV R{i}, {arg_reg}")
    
    # Evaluate remaining arguments and push in reverse order
    if num_stack_args > 0:
        for i in range(arg_count - 1, 3, -1):
            arg_code, _, arg_reg = evaluate_expression(arguments[i], func_name, label_counter, var_offsets, next_offset)
            code_lines.append(arg_code)
            code_lines.append(f"    PUSH {{{arg_reg}}}")
    
    # Emit BL instruction
    code_lines.append(f"    BL {callee}")
    
    # Stack cleanup if stack args were pushed
    if num_stack_args > 0:
        cleanup_bytes = num_stack_args * 4
        code_lines.append(f"    ADD SP, SP, #{cleanup_bytes}")
    
    generated_code = "\n".join(code_lines)
    return (generated_code, 0, "R0")

# === helper functions ===

# === OOP compatibility layer ===
