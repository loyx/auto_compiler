# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._generate_const_code_package._generate_const_code_src import _generate_const_code
from ._generate_var_code_package._generate_var_code_src import _generate_var_code
from ._generate_binop_code_package._generate_binop_code_src import _generate_binop_code
from ._generate_call_code_package._generate_call_code_src import _generate_call_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields (varies by expression type):
# {
#   "type": str,           # e.g., "CONST", "BINOP", "VAR", "CALL"
#   "value": int,          # for CONST: the constant integer value
#   "op": str,             # for BINOP: operator like "+", "-", "*", "/", "==", etc.
#   "left": dict,          # for BINOP: left operand expression
#   "right": dict,         # for BINOP: right operand expression
#   "name": str,           # for VAR: variable name; for CALL: function name
#   "args": list,          # for CALL: list of argument expression dicts
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate ARM64 assembly code for an expression, result in x0."""
    expr_type = expr.get("type")
    
    if expr_type == "CONST":
        return _generate_const_code(expr["value"])
    elif expr_type == "VAR":
        return _generate_var_code(expr["name"], var_offsets)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr, func_name, var_offsets)
    elif expr_type == "CALL":
        return _generate_call_code(expr, func_name, var_offsets)
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")

# === helper functions ===
# Helper functions are delegated to sub-modules

# === OOP compatibility layer ===
# Not required for this function node
