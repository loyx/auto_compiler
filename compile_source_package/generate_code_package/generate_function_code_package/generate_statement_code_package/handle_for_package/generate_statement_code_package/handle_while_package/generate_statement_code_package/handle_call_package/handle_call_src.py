# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_expression_package.evaluate_expression_src import evaluate_expression

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "while_cond": int,
#   "while_end": int,
#   "if_cond": int,
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": "CALL",
#   "function": str,
#   "args": list,
# }

# === main function ===
def handle_call(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM32 assembly for function call statement."""
    args = stmt.get("args", [])
    target_func = stmt.get("function", "")
    
    lines = []
    current_offset = next_offset
    
    # Evaluate each argument and place in r0-r3 or stack
    for i, arg_expr in enumerate(args):
        arg_code, current_offset, result_reg = evaluate_expression(arg_expr, var_offsets, current_offset)
        lines.append(arg_code)
        
        if i < 4:
            # First 4 args go in r0-r3
            if result_reg != f"r{i}":
                lines.append(f"    mov r{i}, {result_reg}")
        else:
            # Args beyond 4 go on stack
            stack_slot = (i - 4) * 4
            lines.append(f"    str {result_reg}, [sp, #{stack_slot}]")
    
    # Generate function call
    lines.append(f"    bl {target_func}")
    
    assembly = "\n".join(lines)
    return (assembly, current_offset)

# === helper functions ===

# === OOP compatibility layer ===
