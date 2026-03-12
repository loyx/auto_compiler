# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_literal_code_package.generate_literal_code_src import generate_literal_code
from .generate_var_code_package.generate_var_code_src import generate_var_code
from .generate_binop_code_package.generate_binop_code_src import generate_binop_code
from .generate_unaryop_code_package.generate_unaryop_code_src import generate_unaryop_code
from .generate_call_code_package.generate_call_code_src import generate_call_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack offset mapping
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "literal", "var", "binop", "unaryop", "call"
#   "value": Any,          # literal value for "literal" type
#   "name": str,           # variable name for "var" type
#   "op": str,             # operator for binop/unaryop
#   "left": dict,          # left operand for binop
#   "right": dict,         # right operand for binop
#   "operand": dict,       # operand for unaryop
#   "func": str,           # function name for "call"
#   "args": list,          # arguments for "call"
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for an expression AST node."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        return generate_literal_code(expr["value"], next_offset)
    elif expr_type == "var":
        return generate_var_code(expr["name"], var_offsets, next_offset)
    elif expr_type == "binop":
        return generate_binop_code(expr["op"], expr["left"], expr["right"], var_offsets, next_offset)
    elif expr_type == "unaryop":
        return generate_unaryop_code(expr["op"], expr["operand"], var_offsets, next_offset)
    elif expr_type == "call":
        return generate_call_code(expr["func"], expr["args"], var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
