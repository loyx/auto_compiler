# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields for EXPRESSION:
# {
#   "type": "EXPRESSION",
#   "func_name": str,
#   "args": list,
# }

# === main function ===
def handle_expression_stmt(stmt: dict, func_name: str, var_offsets: dict) -> str:
    """Handle EXPRESSION statement: generate function call with argument loading."""
    target_func = stmt.get("func_name", "")
    args = stmt.get("args", [])
    
    code_lines = []
    for i, arg in enumerate(args[:8]):
        arg_code = generate_expression_code(arg, func_name, var_offsets)
        code_lines.append(arg_code)
        if i < len(args[:8]) - 1:
            code_lines.append(f"mov x{i+1}, x0")
    
    code_lines.append(f"bl {target_func}")
    return "\n".join(code_lines)

# === helper functions ===

# === OOP compatibility layer ===
