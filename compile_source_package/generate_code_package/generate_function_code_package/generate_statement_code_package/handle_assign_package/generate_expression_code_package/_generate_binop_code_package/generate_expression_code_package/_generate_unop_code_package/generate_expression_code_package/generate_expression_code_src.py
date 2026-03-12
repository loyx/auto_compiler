# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._generate_unop_code_package._generate_unop_code_src import _generate_unop_code
from ._generate_binop_code_package._generate_binop_code_src import _generate_binop_code
from ._generate_var_code_package._generate_var_code_src import _generate_var_code
from ._generate_num_code_package._generate_num_code_src import _generate_num_code
from ._generate_call_code_package._generate_call_code_src import _generate_call_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields (varies by expression type):
# For UNOP:
# {
#   "type": "UNOP",
#   "op": str,         # "-", "!"
#   "operand": dict,   # nested expression dict
# }
# For BINOP:
# {
#   "type": "BINOP",
#   "op": str,         # "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||"
#   "left": dict,      # left operand expression dict
#   "right": dict,     # right operand expression dict
# }
# For VAR:
# {
#   "type": "VAR",
#   "name": str,       # variable name
# }
# For NUM:
# {
#   "type": "NUM",
#   "value": int,      # integer literal value
# }
# For CALL:
# {
#   "type": "CALL",
#   "func_name": str,  # function to call
#   "args": list,      # list of argument expression dicts
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """Generates ARM64 assembly code for a given expression.
    
    Dispatches to specialized handlers based on expression type.
    Result is placed in x0 register.
    """
    expr_type = expr["type"]
    
    if expr_type == "UNOP":
        return _generate_unop_code(expr, func_name, var_offsets)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr, func_name, var_offsets)
    elif expr_type == "VAR":
        return _generate_var_code(expr, func_name, var_offsets)
    elif expr_type == "NUM":
        return _generate_num_code(expr, func_name, var_offsets)
    elif expr_type == "CALL":
        return _generate_call_code(expr, func_name, var_offsets)
    else:
        raise ValueError(f"Unsupported expression type: '{expr_type}'")

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for this function node