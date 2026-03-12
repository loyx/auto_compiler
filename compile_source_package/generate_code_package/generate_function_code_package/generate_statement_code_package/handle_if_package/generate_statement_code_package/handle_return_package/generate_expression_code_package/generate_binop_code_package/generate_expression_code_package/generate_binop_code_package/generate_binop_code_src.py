# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": "VAR" | "NUM" | "BINOP",
#   "name": str,        # for VAR type: variable name
#   "value": int,       # for NUM type: numeric value
#   "op": str,          # for BINOP type: "ADD" | "SUB" | "MUL" | "DIV"
#   "left": Expr,       # for BINOP type: left operand
#   "right": Expr,      # for BINOP type: right operand
# }

# === main function ===
def generate_binop_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int, str]:
    """Generates ARM64 assembly code for binary operations."""
    op = expr["op"]
    left = expr["left"]
    right = expr["right"]
    
    # Generate code for left operand
    left_code, next_offset, _ = generate_expression_code(left, var_offsets, next_offset)
    
    # Save left result to stack
    left_offset = next_offset
    save_left = f"    str x0, [sp, #{left_offset}]\n"
    next_offset += 8
    
    # Generate code for right operand
    right_code, next_offset, _ = generate_expression_code(right, var_offsets, next_offset)
    
    # Reload left operand into x1
    reload_left = f"    ldr x1, [sp, #{left_offset}]\n"
    
    # Emit arithmetic instruction based on op
    op_instructions = {
        "ADD": "add x0, x1, x0\n",
        "SUB": "sub x0, x1, x0\n",
        "MUL": "mul x0, x1, x0\n",
        "DIV": "udiv x0, x1, x0\n",
    }
    arith_instr = op_instructions[op]
    
    # Combine all code
    combined_code = left_code + save_left + right_code + reload_left + arith_instr
    
    return (combined_code, next_offset, "x0")

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
