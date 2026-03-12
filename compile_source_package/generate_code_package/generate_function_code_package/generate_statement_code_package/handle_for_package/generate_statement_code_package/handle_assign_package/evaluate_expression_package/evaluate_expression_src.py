# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._eval_literal_package._eval_literal_src import _eval_literal
from ._eval_ident_package._eval_ident_src import _eval_ident
from ._eval_binop_package._eval_binop_src import _eval_binop
from ._eval_unary_package._eval_unary_src import _eval_unary
from ._eval_call_package._eval_call_src import _eval_call

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields (expression tree):
# {
#   "type": str,           # "BINOP", "UNARY", "LITERAL", "IDENT", "CALL"
#   "op": str,             # for BINOP/UNARY: "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!", "-"
#   "left": dict,          # for BINOP: nested expression
#   "right": dict,         # for BINOP: nested expression
#   "operand": dict,       # for UNARY: nested expression
#   "value": Any,          # for LITERAL: int or bool (0/1)
#   "name": str,           # for IDENT: variable name
#   "func_name": str,      # for CALL: function to call
#   "arguments": list      # for CALL: list of expression trees
# }

# === main function ===
def evaluate_expression(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Evaluate an expression tree and generate ARM assembly code."""
    expr_type = expr.get("type")
    if not expr_type:
        raise ValueError("Missing required field 'type' in expression")
    
    if expr_type == "LITERAL":
        return _eval_literal(expr)
    elif expr_type == "IDENT":
        return _eval_ident(expr, var_offsets)
    elif expr_type == "BINOP":
        return _eval_binop(expr, func_name, label_counter, var_offsets, next_offset)
    elif expr_type == "UNARY":
        return _eval_unary(expr, func_name, label_counter, var_offsets, next_offset)
    elif expr_type == "CALL":
        return _eval_call(expr, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")

# === helper functions ===
# No helper functions - all delegated to child nodes

# === OOP compatibility layer ===
# Not required for this function node