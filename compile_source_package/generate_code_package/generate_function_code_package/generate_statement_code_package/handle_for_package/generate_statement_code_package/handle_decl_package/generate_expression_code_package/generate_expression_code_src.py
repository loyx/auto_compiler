# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_literal_code_package.generate_literal_code_src import generate_literal_code
from .generate_identifier_code_package.generate_identifier_code_src import generate_identifier_code
from .generate_binop_code_package.generate_binop_code_src import generate_binop_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "expr": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "LITERAL" | "BINOP" | "IDENTIFIER" | "CALL",
#   "value": Any,        # for LITERAL: int, float, bool
#   "op": str,          # for BINOP: arithmetic/bitwise/comparison operators
#   "left": dict,       # for BINOP: left operand expression
#   "right": dict,      # for BINOP: right operand expression
#   "name": str,        # for IDENTIFIER: variable name
#   "var_type": str,    # for IDENTIFIER: "int", "char", "short", "float", etc.
#   "func_name": str,   # for CALL: function name
#   "args": list,       # for CALL: list of argument expressions
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict) -> Tuple[str, int]:
    """
    Generate ARM assembly code to evaluate an expression.
    
    Dispatches to appropriate handler based on expression type.
    
    Returns:
        Tuple[code_string, result_register] where result_register is typically 0 (R0)
    """
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        return generate_literal_code(expr)
    elif expr_type == "IDENTIFIER":
        return generate_identifier_code(expr, var_offsets)
    elif expr_type == "BINOP":
        return generate_binop_code(expr, func_name, label_counter, var_offsets)
    elif expr_type == "CALL":
        raise NotImplementedError("CALL expressions not supported in current implementation")
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")


# === helper functions ===
# No helper functions in this file - all logic delegated to child nodes

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
