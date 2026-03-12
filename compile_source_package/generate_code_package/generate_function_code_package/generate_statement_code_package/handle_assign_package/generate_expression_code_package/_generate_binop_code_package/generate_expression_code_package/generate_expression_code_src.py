# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._generate_binop_code_package._generate_binop_code_src import _generate_binop_code
from ._generate_literal_code_package._generate_literal_code_src import _generate_literal_code
from ._generate_var_code_package._generate_var_code_src import _generate_var_code
from ._generate_call_code_package._generate_call_code_src import _generate_call_code
from ._generate_unop_code_package._generate_unop_code_src import _generate_unop_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields (varies by type):
# For BINOP:
# {
#   "type": "BINOP",
#   "op": str,
#   "left": dict,
#   "right": dict,
# }
# For LITERAL:
# {
#   "type": "LITERAL",
#   "value": int | bool,
#   "literal_type": str,
# }
# For VAR:
# {
#   "type": "VAR",
#   "name": str,
# }
# For CALL:
# {
#   "type": "CALL",
#   "function": str,
#   "arguments": list,
# }
# For UNOP:
# {
#   "type": "UNOP",
#   "op": str,
#   "operand": dict,
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Main dispatcher for ARM64 code generation from expression AST.
    
    Routes expression types to specialized handlers. All handlers must
    ensure result is in x0 register after execution.
    """
    expr_type = expr["type"]
    
    if expr_type == "BINOP":
        return _generate_binop_code(expr, func_name, var_offsets)
    elif expr_type == "LITERAL":
        return _generate_literal_code(expr, func_name, var_offsets)
    elif expr_type == "VAR":
        return _generate_var_code(expr, func_name, var_offsets)
    elif expr_type == "CALL":
        return _generate_call_code(expr, func_name, var_offsets)
    elif expr_type == "UNOP":
        return _generate_unop_code(expr, func_name, var_offsets)
    else:
        raise ValueError(f"Unknown expression type: '{expr_type}'")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
