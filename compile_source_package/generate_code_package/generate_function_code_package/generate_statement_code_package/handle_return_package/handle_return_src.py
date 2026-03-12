# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset for variable
# }

Stmt = Dict[str, Any]
# Stmt possible fields for RETURN:
# {
#   "type": "RETURN",
#   "value": dict,  # Return value expression (optional)
# }

# === main function ===
def handle_return(stmt: dict, func_name: str, var_offsets: dict) -> str:
    """Handle RETURN statement type. Generate expression code and jump to function exit label."""
    code_lines = []
    
    # If value expression exists and is not empty, generate code to compute it
    value = stmt.get("value")
    if value is not None and value != {}:
        expr_code = generate_expression_code(value, func_name, var_offsets)
        if expr_code:
            code_lines.append(expr_code)
    
    # Generate jump to exit label
    code_lines.append(f"b {func_name}_exit")
    
    return "\n".join(code_lines)

# === helper functions ===

# === OOP compatibility layer ===
