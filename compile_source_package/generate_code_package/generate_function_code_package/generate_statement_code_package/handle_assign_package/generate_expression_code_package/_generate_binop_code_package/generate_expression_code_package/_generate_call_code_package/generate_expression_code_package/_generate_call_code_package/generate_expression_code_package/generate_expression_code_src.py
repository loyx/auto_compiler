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
# Expr possible fields:
# {
#   "type": str,       # Expression type: "CALL", "BINOP", "VAR", "CONST"
#   "function": str,   # For CALL: function name to call
#   "arguments": list, # For CALL: list of expression dicts (max 8)
#   "op": str,         # For BINOP: operator (+, -, *, /, %, &, |, ^, <<, >>, ==, !=, <, <=, >, >=)
#   "left": dict,      # For BINOP: left operand expression
#   "right": dict,     # For BINOP: right operand expression
#   "name": str,       # For VAR: variable name
#   "value": int,      # For CONST: constant integer value (64-bit signed)
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """
    Generate ARM64 assembly code for any expression type.
    All expression types produce result in x0 register.
    """
    expr_type = expr.get("type")
    
    if expr_type == "CONST":
        return _generate_const_code(expr, var_offsets)
    elif expr_type == "VAR":
        return _generate_var_code(expr, var_offsets)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr, func_name, var_offsets)
    elif expr_type == "CALL":
        return _generate_call_code(expr, func_name, var_offsets)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# Helper functions are delegated to separate files

# === OOP compatibility layer ===
# Not required for this function node