# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
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
#   "type": str,
#   "func_name": str,
#   "args": list,
# }

# === main function ===
def handle_call(stmt: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle CALL statement code generation for ARM assembly."""
    target_func_name = stmt["func_name"]
    args = stmt["args"]
    
    asm_lines = []
    current_offset = next_offset
    
    # Push arguments in reverse order (ARM calling convention)
    for arg_expr in reversed(args):
        arg_code, current_offset = generate_expression_code(
            arg_expr, func_name, label_counter, var_offsets, current_offset
        )
        asm_lines.append(arg_code)
        # Push R0 onto stack: STR R0, [SP, #-4]!
        asm_lines.append("STR R0, [SP, #-4]!")
    
    # Call the function
    asm_lines.append(f"BL {target_func_name}")
    
    # Stack cleanup: restore SP by arg_count * 4 bytes
    if args:
        asm_lines.append(f"ADD SP, SP, #{len(args) * 4}")
    
    asm_code = "\n".join(asm_lines)
    return (asm_code, current_offset)

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this function node
