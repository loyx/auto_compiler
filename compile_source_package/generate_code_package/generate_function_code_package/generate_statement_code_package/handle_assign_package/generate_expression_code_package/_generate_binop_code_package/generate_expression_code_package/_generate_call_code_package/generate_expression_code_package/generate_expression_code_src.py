# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._generate_call_code_package._generate_call_code_src import _generate_call_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,       # Expression type: "CALL", "BINOP", "VAR", "CONST"
#   "function": str,   # For CALL: function name to call
#   "arguments": list, # For CALL: list of expression dicts (max 8)
#   "op": str,         # For BINOP: operator (+, -, *, /, %, &, |, ^, <<, >>, ==, !=, <, <=, >, >=)
#   "left": dict,      # For BINOP: left operand expression
#   "right": dict,     # For BINOP: right operand expression
#   "name": str,       # For VAR: variable name
#   "value": int,      # For CONST: constant integer value (64-bit signed)
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generates ARM64 assembly code for any expression type. Result in x0."""
    expr_type = expr.get("type")
    if expr_type is None:
        raise KeyError("Missing 'type' field in expression")

    if expr_type == "CONST":
        return _generate_const_code(expr)
    elif expr_type == "VAR":
        return _generate_var_code(expr, var_offsets)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr, func_name, var_offsets)
    elif expr_type == "CALL":
        return _generate_call_code(expr, func_name, var_offsets)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_const_code(expr: dict) -> str:
    """Generate code for CONST expression using movz/movn/movk."""
    if "value" not in expr:
        raise KeyError("Missing 'value' field in CONST expression")
    value = expr["value"]
    if not isinstance(value, int) or value < -(2**63) or value >= 2**63:
        raise ValueError(f"Constant value out of 64-bit signed range: {value}")
    if 0 <= value <= 65535:
        return f"    movz x0, #{value}"
    elif -65535 <= value < 0:
        return f"    movn x0, #{abs(value) - 1}"
    else:
        lines = [f"    movz x0, #{value & 0xFFFF}"]
        if value & 0xFFFF0000:
            lines.append(f"    movk x0, #{(value >> 16) & 0xFFFF}, lsl 16")
        if value & 0xFFFF00000000:
            lines.append(f"    movk x0, #{(value >> 32) & 0xFFFF}, lsl 32")
        if value & 0xFFFF000000000000:
            lines.append(f"    movk x0, #{(value >> 48) & 0xFFFF}, lsl 48")
        return "\n".join(lines)

def _generate_var_code(expr: dict, var_offsets: dict) -> str:
    """Generate code for VAR expression by loading from stack."""
    if "name" not in expr:
        raise KeyError("Missing 'name' field in VAR expression")
    name = expr["name"]
    if name not in var_offsets:
        raise KeyError(f"Undefined variable: {name}")
    offset = var_offsets[name]
    return f"    ldr x0, [sp, #{offset}]"

def _generate_binop_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate code for BINOP expression with proper register management."""
    if "op" not in expr:
        raise KeyError("Missing 'op' field in BINOP expression")
    if "left" not in expr:
        raise KeyError("Missing 'left' field in BINOP expression")
    if "right" not in expr:
        raise KeyError("Missing 'right' field in BINOP expression")
    op = expr["op"]
    op_map = {
        "+": "add", "-": "sub", "*": "mul", "/": "sdiv", "%": "rem",
        "&": "and", "|": "orr", "^": "eor", "<<": "lsl", ">>": "lsr",
        "==": "cmp_eq", "!=": "cmp_ne", "<": "cmp_lt", "<=": "cmp_le",
        ">": "cmp_gt", ">=": "cmp_ge"
    }
    if op not in op_map:
        raise ValueError(f"Unsupported binary operator: {op}")
    lines = []
    lines.append(generate_expression_code(expr["left"], func_name, var_offsets))
    lines.append("    mov x8, x0")
    lines.append(generate_expression_code(expr["right"], func_name, var_offsets))
    lines.append("    mov x1, x0")
    lines.append("    mov x0, x8")
    asm_op = op_map[op]
    if asm_op.startswith("cmp_"):
        cond = asm_op[4:]
        lines.append(f"    cmp x0, x1")
        lines.append(f"    cset x0, {cond}")
    elif asm_op == "rem":
        lines.append(f"    sdiv x2, x0, x1")
        lines.append(f"    msub x0, x2, x1, x0")
    else:
        lines.append(f"    {asm_op} x0, x0, x1")
    return "\n".join(lines)

# === OOP compatibility layer ===
# Not required for this function node (pure code generator)
