# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack offset mapping
# }

Stmt = Dict[str, Any]
# Stmt possible fields for VAR_DECL:
# {
#   "type": "VAR_DECL",
#   "var_name": str,
#   "var_type": str,
#   "init_value": dict,  # Optional expression ADT
# }

# === main function ===
def handle_var_decl(stmt: dict, func_name: str, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Handle VAR_DECL statement. Allocate stack offset and generate init code."""
    var_name = stmt["var_name"]
    var_type = stmt["var_type"]
    init_value = stmt.get("init_value")
    
    # Allocate stack offset for this variable (8 bytes, 64-bit aligned)
    var_offsets[var_name] = next_offset
    new_offset = next_offset + 8
    
    code_lines = []
    code_lines.append(f"    // VAR_DECL: {var_name} ({var_type}) at offset {var_offsets[var_name]}")
    
    # If init_value exists and is not empty, generate expression code and store result
    if init_value:
        expr_code = generate_expression_code(init_value, func_name, var_offsets)
        code_lines.append(expr_code)
        code_lines.append(f"    str x0, [sp, {var_offsets[var_name]}]")
    
    return "\n".join(code_lines), new_offset

# === helper functions ===

# === OOP compatibility layer ===
