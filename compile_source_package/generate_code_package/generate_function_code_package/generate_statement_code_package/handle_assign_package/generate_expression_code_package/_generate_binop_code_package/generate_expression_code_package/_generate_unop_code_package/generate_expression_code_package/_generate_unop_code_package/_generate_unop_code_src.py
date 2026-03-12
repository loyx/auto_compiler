# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ..generate_expression_code_src import generate_expression_code

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

# === main function ===
def _generate_unop_code(expr: Dict[str, Any], func_name: str, var_offsets: Dict[str, int]) -> str:
    """Generate ARM64 assembly code for unary operations."""
    op = expr["op"]
    operand = expr["operand"]

    # Generate code for operand (recursive call to parent dispatcher)
    code = generate_expression_code(operand, func_name, var_offsets)

    if op == "-":
        code += "\n    neg x0, x0"
    elif op == "!":
        code += "\n    cmp x0, #0\n    cset x0, eq"
    else:
        raise ValueError(f"Unsupported unary operator: '{op}'")

    return code

# === helper functions ===
# No helper functions needed - logic is simple and inline

# === OOP compatibility layer ===
# Not needed - this is a handler function, not a framework entry point
