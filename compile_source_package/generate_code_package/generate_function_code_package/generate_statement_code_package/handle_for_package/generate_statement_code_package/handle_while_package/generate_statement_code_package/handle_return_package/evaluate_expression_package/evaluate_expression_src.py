# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .evaluate_const_package.evaluate_const_src import evaluate_const
from .evaluate_var_package.evaluate_var_src import evaluate_var
from .evaluate_binop_package.evaluate_binop_src import evaluate_binop
from .evaluate_call_package.evaluate_call_src import evaluate_call

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str (e.g., "BINOP", "VAR", "CONST", "CALL"),
#   "op": str (for BINOP),
#   "left": dict (for BINOP),
#   "right": dict (for BINOP),
#   "name": str (for VAR),
#   "value": Any (for CONST),
#   "func_name": str (for CALL),
#   "args": list (for CALL),
# }

# === main function ===
def evaluate_expression(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Evaluate expression AST and generate ARM32 assembly code."""
    expr_type = expr.get("type", "")
    
    if expr_type == "CONST":
        return evaluate_const(expr.get("value"), next_offset)
    elif expr_type == "VAR":
        return evaluate_var(expr.get("name"), var_offsets, next_offset)
    elif expr_type == "BINOP":
        return evaluate_binop(
            expr.get("op"),
            expr.get("left"),
            expr.get("right"),
            var_offsets,
            next_offset
        )
    elif expr_type == "CALL":
        return evaluate_call(
            expr.get("func_name"),
            expr.get("args", []),
            var_offsets,
            next_offset
        )
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
