# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields for UNOP:
# {
#   "type": "UNOP",
#   "op": str,         # "-", "!"
#   "operand": dict,   # 操作数表达式 dict
# }

# === main function ===
def _generate_unop_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generates ARM64 assembly code for unary operations.
    
    Supports '-' (arithmetic negation) and '!' (logical not).
    Result is placed in x0 register.
    """
    op = expr["op"]
    operand = expr["operand"]
    
    # Generate code for operand first
    code = generate_expression_code(operand, func_name, var_offsets)
    
    # Apply unary operation
    if op == "-":
        code += "neg x0, x0\n"
    elif op == "!":
        code += "cmp x0, #0\n"
        code += "cset x0, eq\n"
    else:
        raise ValueError(f"Unsupported unary operator: '{op}'")
    
    return code

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
