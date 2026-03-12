# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this inline implementation

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # byte offset from stack pointer (multiple of 8)
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # Expression type: "CONST", "VAR", "BINOP"
#   "value": int,          # For CONST: integer constant value
#   "var_name": str,       # For VAR: variable name
#   "op": str,             # For BINOP: operator ("ADD", "SUB", "MUL", "DIV", "AND", "OR", "XOR", "CMP")
#   "left": dict,          # For BINOP: left operand expression dict
#   "right": dict,         # For BINOP: right operand expression dict
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """
    Generate ARM64 assembly code for a single expression.
    Result is always left in x0 register.
    """
    expr_type = expr.get("type")
    
    if expr_type == "CONST":
        return _generate_const_code(expr["value"])
    elif expr_type == "VAR":
        return _generate_var_code(expr["var_name"], var_offsets)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr["op"], expr["left"], expr["right"], func_name, var_offsets)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_const_code(value: int) -> str:
    """Generate code to load integer constant into x0."""
    if abs(value) <= 4095:
        return f"mov x0, #{value}"
    else:
        return f"ldr x0, ={value}"

def _generate_var_code(var_name: str, var_offsets: VarOffsets) -> str:
    """Generate code to load variable from stack into x0."""
    if var_name not in var_offsets:
        raise KeyError(f"Variable not found: {var_name}")
    offset = var_offsets[var_name]
    return f"ldr x0, [sp, #{offset}]"

def _generate_binop_code(op: str, left: Expr, right: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """
    Generate code for binary operation.
    Strategy: evaluate left into x0, save to x1, evaluate right into x0, apply op.
    """
    op_map = {
        "ADD": "add",
        "SUB": "sub",
        "MUL": "mul",
        "DIV": "sdiv",
        "AND": "and",
        "OR": "orr",
        "XOR": "eor",
        "CMP": "cmp",
    }
    
    if op not in op_map:
        raise ValueError(f"Unknown operator: {op}")
    
    asm_instr = op_map[op]
    
    # Evaluate left operand first (result in x0)
    left_code = generate_expression_code(left, func_name, var_offsets)
    
    # Save left result to x1
    save_code = "mov x1, x0"
    
    # Evaluate right operand (result in x0)
    right_code = generate_expression_code(right, func_name, var_offsets)
    
    # Apply operation: result in x0
    # For most ops: instr x0, x1, x0 (left in x1, right in x0)
    if asm_instr == "cmp":
        # cmp doesn't write to x0, it sets flags
        op_code = f"cmp x1, x0"
    else:
        op_code = f"{asm_instr} x0, x1, x0"
    
    return f"{left_code}\n{save_code}\n{right_code}\n{op_code}"

# === OOP compatibility layer ===
# Not needed for this function node
