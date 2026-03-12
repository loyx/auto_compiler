# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields for CALL:
# {
#   "type": "CALL",
#   "name": str,           # function name to call
#   "args": list,          # list of argument expression dicts
# }

# === main function ===
def _generate_call_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate ARM64 assembly code for function call expression."""
    args = expr.get("args", [])
    
    if len(args) > 8:
        raise ValueError("Too many arguments (max 8 supported)")
    
    code_lines = []
    call_name = expr.get("name", "")
    
    for i, arg_expr in enumerate(args):
        # Evaluate argument expression (result in x0)
        arg_code = generate_expression_code(arg_expr, func_name, var_offsets)
        code_lines.append(arg_code)
        
        # Move result to appropriate argument register (x0-x7)
        if i > 0:
            code_lines.append(f"mov x{i}, x0")
    
    # Generate function call instruction
    code_lines.append(f"bl {call_name}")
    
    return "\n".join(code_lines)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
