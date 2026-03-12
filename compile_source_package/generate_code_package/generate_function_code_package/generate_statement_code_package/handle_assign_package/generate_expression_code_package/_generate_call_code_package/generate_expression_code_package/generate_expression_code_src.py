# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions - all helpers are internal to this file

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields (multiple expression types):
# {
#   "type": "CALL" | "BINOP" | "VAR" | "CONST",
#   "name": str,           # for CALL: function name
#   "args": list,          # for CALL: list of argument expressions
#   "op": str,             # for BINOP: operator
#   "left": dict,          # for BINOP: left operand expression
#   "right": dict,         # for BINOP: right operand expression
#   "var_name": str,       # for VAR: variable name
#   "value": int,          # for CONST: constant value
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """Recursively generate ARM64 assembly code for an expression."""
    expr_type = expr.get("type")
    
    if expr_type == "CALL":
        return _generate_call_code(expr, func_name, var_offsets)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr, func_name, var_offsets)
    elif expr_type == "VAR":
        var_name = expr["var_name"]
        offset = var_offsets[var_name]
        return f"ldr x0, [sp, #{offset}]"
    elif expr_type == "CONST":
        value = expr["value"]
        if -4096 <= value <= 4095:
            return f"mov x0, #{value}"
        else:
            # Use movz/movk for large values
            low = value & 0xFFFF
            high = (value >> 16) & 0xFFFF
            if high == 0:
                return f"movz x0, #{low}"
            else:
                return f"movz x0, #{high}, lsl #16\nmovk x0, #{low}"
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_call_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """Generate code for a function call expression."""
    callee_name = expr["name"]
    args = expr.get("args", [])
    
    code_lines = []
    
    # Generate code for each argument and store in x0-x7
    for i, arg_expr in enumerate(args):
        if i >= 8:
            raise ValueError(f"Too many arguments (max 8): {len(args)}")
        arg_code = generate_expression_code(arg_expr, func_name, var_offsets)
        code_lines.append(arg_code)
        if i < len(args) - 1:  # Don't save last arg, it stays in x0 for the call
            code_lines.append(f"mov x{i}, x0")
    
    # Call the function
    code_lines.append(f"bl {callee_name}")
    
    # Result is already in x0 from the call
    return "\n".join(code_lines)

def _generate_binop_code(expr: Expr, func_name: str, var_offsets: VarOffsets) -> str:
    """Generate code for a binary operation expression."""
    op = expr["op"]
    left_expr = expr["left"]
    right_expr = expr["right"]
    
    code_lines = []
    
    # Evaluate left operand (result in x0)
    left_code = generate_expression_code(left_expr, func_name, var_offsets)
    code_lines.append(left_code)
    
    # Save left result to x9
    code_lines.append("mov x9, x0")
    
    # Evaluate right operand (result in x0)
    right_code = generate_expression_code(right_expr, func_name, var_offsets)
    code_lines.append(right_code)
    
    # Perform operation: x0 = x9 op x0
    op_map = {
        "+": "add x0, x9, x0",
        "-": "sub x0, x9, x0",
        "*": "mul x0, x9, x0",
        "/": "sdiv x0, x9, x0",
        "%": "sdiv x10, x9, x0\nmsub x0, x10, x0, x9",
        "==": "cmp x9, x0\nmov x0, #0\ncset x0, eq",
        "!=": "cmp x9, x0\nmov x0, #0\ncset x0, ne",
        "<": "cmp x9, x0\nmov x0, #0\ncset x0, lt",
        "<=": "cmp x9, x0\nmov x0, #0\ncset x0, le",
        ">": "cmp x9, x0\nmov x0, #0\ncset x0, gt",
        ">=": "cmp x9, x0\nmov x0, #0\ncset x0, ge",
        "&": "and x0, x9, x0",
        "|": "orr x0, x9, x0",
        "^": "eor x0, x9, x0",
    }
    
    if op not in op_map:
        raise ValueError(f"Unknown binary operator: {op}")
    
    code_lines.append(op_map[op])
    
    return "\n".join(code_lines)

# === OOP compatibility layer ===
# Not needed - this is a pure function node