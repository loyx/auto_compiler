# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._handle_const_expr_package._handle_const_expr_src import _handle_const_expr
from ._handle_var_expr_package._handle_var_expr_src import _handle_var_expr
from ._handle_binop_expr_package._handle_binop_expr_src import _handle_binop_expr
from ._handle_unop_expr_package._handle_unop_expr_src import _handle_unop_expr

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "CONST" | "VAR" | "BINOP" | "UNOP"
#   "value": int,          # for CONST: integer value
#   "name": str,           # for VAR: variable name
#   "op": str,             # for BINOP/UNOP: operator string
#   "left": dict,          # for BINOP: left operand expr dict
#   "right": dict,         # for BINOP: right operand expr dict
#   "operand": dict,       # for UNOP: operand expr dict
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> Tuple[str, str]:
    """Generate ARM64 assembly code for an expression tree.
    
    Args:
        expr: Expression dict with type-specific fields
        func_name: Current function name for context
        var_offsets: Variable name to stack offset mapping
    
    Returns:
        Tuple of (assembly_code_string, result_register_name)
    """
    expr_type = expr.get("type", "")
    next_reg = 1  # Start with x1 (x0 reserved for return values)
    
    if expr_type == "CONST":
        code, result_reg, _ = _handle_const_expr(expr, next_reg)
    elif expr_type == "VAR":
        code, result_reg, _ = _handle_var_expr(expr, var_offsets, next_reg)
    elif expr_type == "BINOP":
        code, result_reg, _ = _handle_binop_expr(expr, func_name, var_offsets, next_reg)
    elif expr_type == "UNOP":
        code, result_reg, _ = _handle_unop_expr(expr, func_name, var_offsets, next_reg)
    else:
        raise RuntimeError(f"Unknown expression type: {expr_type}")
    
    return code, result_reg

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
