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

Stmt = Dict[str, Any]
# Stmt possible fields for ASSIGN:
# {
#   "type": "ASSIGN",
#   "target": str,           # Variable name to assign to
#   "value": dict,           # Expression to assign
# }

# === main function ===
def handle_assign(stmt: dict, func_name: str, var_offsets: dict) -> str:
    """
    Handle ASSIGN statement type.
    Generate expression code for value and store to target variable's stack offset.
    """
    # Extract target variable name
    target = stmt["target"]
    
    # Look up stack offset for target variable
    offset = var_offsets.get(target, 0)
    
    # Generate code for value expression (result will be in x0)
    value_expr = stmt.get("value")
    if value_expr is not None:
        expr_code = generate_expression_code(value_expr, func_name, var_offsets)
    else:
        expr_code = ""
    
    # Generate store instruction: str x0, [sp, #{offset}]
    store_code = f"str x0, [sp, #{offset}]"
    
    # Combine and return complete code
    if expr_code:
        return expr_code + "\n" + store_code
    else:
        return store_code

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed - this is a pure function node, not a framework entry point
