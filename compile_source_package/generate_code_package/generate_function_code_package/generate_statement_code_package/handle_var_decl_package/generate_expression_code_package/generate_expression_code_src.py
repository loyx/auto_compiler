# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions delegated

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack offset mapping
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "LITERAL", "IDENTIFIER", "BINARY_OP", "FUNCTION_CALL"
#   "value": Any,  # LITERAL type literal value (int or bool)
#   "var_name": str,  # IDENTIFIER type variable name
#   "op": str,  # BINARY_OP operator (ADD, SUB, MUL, DIV, MOD, AND, ORR, EOR)
#   "left": dict,  # BINARY_OP left operand expression
#   "right": dict,  # BINARY_OP right operand expression
#   "func_name": str,  # FUNCTION_CALL function name
#   "args": list,  # FUNCTION_CALL argument list (list of expr dicts)
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate ARM64 assembly code for an expression. Result placed in x0."""
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        return _generate_literal_code(expr, func_name)
    elif expr_type == "IDENTIFIER":
        return _generate_identifier_code(expr, func_name, var_offsets)
    elif expr_type == "BINARY_OP":
        return _generate_binary_op_code(expr, func_name, var_offsets)
    elif expr_type == "FUNCTION_CALL":
        return _generate_function_call_code(expr, func_name, var_offsets)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_literal_code(expr: dict, func_name: str) -> str:
    """Generate code for LITERAL expression."""
    value = expr.get("value")
    if value is None:
        raise ValueError("Literal value cannot be None")
    if isinstance(value, bool):
        int_val = 1 if value else 0
        return f"    mov x0, #{int_val}"
    elif isinstance(value, int):
        return f"    mov x0, #{value}"
    elif isinstance(value, str):
        raise ValueError("String literals not supported in expressions")
    elif isinstance(value, float):
        raise ValueError("Float literals not supported in expressions")
    else:
        raise ValueError(f"Unsupported literal type: {type(value)}")

def _generate_identifier_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate code for IDENTIFIER expression."""
    var_name = expr.get("var_name")
    if var_name not in var_offsets:
        lines = [f"    // ERROR: undefined variable '{var_name}'"]
        lines.append("    mov x0, #0")
        return "\n".join(lines)
    offset = var_offsets[var_name]
    return f"    ldr x0, [sp, #{offset}]"

def _generate_binary_op_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate code for BINARY_OP expression."""
    op = expr.get("op")
    left = expr.get("left")
    right = expr.get("right")
    
    op_map = {
        "ADD": "add x0, x1, x0",
        "SUB": "sub x0, x1, x0",
        "MUL": "mul x0, x1, x0",
        "DIV": "udiv x0, x1, x0",
        "MOD": "udiv x0, x1, x0\n    msub x0, x0, x0, x1",
        "AND": "and x0, x1, x0",
        "ORR": "orr x0, x1, x0",
        "EOR": "eor x0, x1, x0",
    }
    
    if op not in op_map:
        raise ValueError(f"Unsupported binary operator: {op}")
    
    lines = []
    lines.append(generate_expression_code(left, func_name, var_offsets))
    lines.append("    mov x1, x0")
    lines.append(generate_expression_code(right, func_name, var_offsets))
    lines.append(f"    {op_map[op]}")
    
    return "\n".join(lines)

def _generate_function_call_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate code for FUNCTION_CALL expression."""
    callee_name = expr.get("func_name")
    args = expr.get("args", [])
    
    if len(args) > 8:
        raise ValueError(f"Function call exceeds maximum 8 arguments: {len(args)}")
    
    lines = []
    reg_index = 0
    for arg_expr in args:
        arg_code = generate_expression_code(arg_expr, func_name, var_offsets)
        lines.append(arg_code)
        if reg_index < 7:
            next_reg = reg_index + 1
            lines.append(f"    mov x{next_reg}, x0")
        reg_index += 1
    
    lines.append(f"    bl {callee_name}")
    
    return "\n".join(lines)

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
