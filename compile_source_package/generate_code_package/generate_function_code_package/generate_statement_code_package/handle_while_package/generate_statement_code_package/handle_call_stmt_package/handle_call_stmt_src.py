# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Stmt = Dict[str, Any]
# Stmt possible fields:
# {
#   "type": str,
#   "function": str,       # function name to call
#   "args": list,          # list of argument expressions
# }

# === main function ===
def handle_call_stmt(stmt: Stmt, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Handle CALL statement. Generate arg expression codes then bl instruction."""
    function_name = stmt.get("function", "")
    if not function_name:
        return "", next_offset

    args = stmt.get("args", [])
    code_parts = []
    current_offset = next_offset

    for arg_expr in args:
        # Generate code for this argument expression
        arg_code, current_offset = generate_expression_code(arg_expr, var_offsets, current_offset)
        code_parts.append(arg_code)
        # Store the result (in x0) to stack slot for this argument
        store_offset = current_offset - 8
        code_parts.append(f"STORE_OFFSET {store_offset}")

    # Generate bl instruction
    code_parts.append(f"bl {function_name}")

    final_code = "\n".join(code_parts)
    return final_code, current_offset

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
