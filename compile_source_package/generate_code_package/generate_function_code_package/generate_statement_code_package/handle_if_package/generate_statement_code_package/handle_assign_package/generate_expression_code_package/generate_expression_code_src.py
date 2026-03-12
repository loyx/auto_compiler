# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_ident_package._handle_ident_src import _handle_ident
from ._handle_binary_package._handle_binary_src import _handle_binary
from ._handle_unary_package._handle_unary_src import _handle_unary

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # maps variable name to stack slot index
# }

Expr = Dict[str, Any]
# Expr possible fields by type:
# LITERAL: {"type": "LITERAL", "value": int|float}
# IDENT: {"type": "IDENT", "name": str}
# BINARY: {"type": "BINARY", "op": str, "left": Expr, "right": Expr}
# UNARY: {"type": "UNARY", "op": str, "operand": Expr}
# Binary ops: "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||"
# Unary ops: "-", "!"


# === main function ===
def generate_expression_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generate ARM64 assembly code for expression evaluation."""
    expr_type = expr["type"]
    
    if expr_type == "LITERAL":
        return _handle_literal(expr, next_offset)
    elif expr_type == "IDENT":
        return _handle_ident(expr, var_offsets, next_offset)
    elif expr_type == "BINARY":
        return _handle_binary(expr, var_offsets, next_offset)
    elif expr_type == "UNARY":
        return _handle_unary(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")


# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node