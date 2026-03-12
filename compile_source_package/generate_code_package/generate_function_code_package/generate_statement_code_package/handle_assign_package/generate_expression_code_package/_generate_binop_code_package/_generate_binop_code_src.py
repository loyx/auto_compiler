# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# generate_expression_code is the dispatcher; declared in delegated_interfaces
# It will be available at runtime through the module's internal structure
# Import for testing/mock purposes - circular import handled at runtime
def generate_expression_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Placeholder - will be replaced by actual dispatcher at runtime."""
    pass

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields for BINOP:
# {
#   "type": "BINOP",
#   "op": str,             # operator like "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="
#   "left": dict,          # left operand expression dict
#   "right": dict,         # right operand expression dict
# }

# === main function ===
def _generate_binop_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """
    Generate ARM64 assembly code for a binary operation expression.
    
    Recursively generates code for left and right operands, saves left result
    in x9, then applies the operation. Final result is in x0.
    """
    # Generate code for left operand (result in x0)
    left_code = generate_expression_code(expr["left"], func_name, var_offsets)
    
    # Save left result to temporary register x9
    save_code = "mov x9, x0"
    
    # Generate code for right operand (result in x0)
    right_code = generate_expression_code(expr["right"], func_name, var_offsets)
    
    # Apply the binary operation
    op = expr["op"]
    op_instructions = _get_operator_instructions(op)
    
    # Combine all code segments
    code_lines = [left_code, save_code, right_code, op_instructions]
    return "\n".join(code_lines)


# === helper functions ===
def _get_operator_instructions(op: str) -> str:
    """
    Map operator string to ARM64 assembly instructions.
    
    Returns the instruction(s) that compute: x0 = x9 op x0
    For comparison operators, returns cmp + cset sequence.
    """
    # Arithmetic operators
    if op == "+":
        return "add x0, x9, x0"
    elif op == "-":
        return "sub x0, x9, x0"
    elif op == "*":
        return "mul x0, x9, x0"
    elif op == "/":
        return "sdiv x0, x9, x0"
    # Comparison operators
    elif op == "==":
        return "cmp x9, x0\ncset x0, eq"
    elif op == "!=":
        return "cmp x9, x0\ncset x0, ne"
    elif op == "<":
        return "cmp x9, x0\ncset x0, lt"
    elif op == ">":
        return "cmp x9, x0\ncset x0, gt"
    elif op == "<=":
        return "cmp x9, x0\ncset x0, le"
    elif op == ">=":
        return "cmp x9, x0\ncset x0, ge"
    else:
        raise ValueError(f"Unsupported binary operator: '{op}'. Supported: +, -, *, /, ==, !=, <, >, <=, >=")


# === OOP compatibility layer ===
# Not needed for this helper function node
