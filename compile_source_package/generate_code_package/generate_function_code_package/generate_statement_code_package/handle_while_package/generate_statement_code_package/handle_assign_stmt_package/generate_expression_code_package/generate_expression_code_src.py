# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - implementation is inline

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,       # expression type: "CONST", "VAR", "BINOP"
#   "value": Any,      # constant value for CONST
#   "name": str,       # variable name for VAR
#   "op": str,         # operator for BINOP: "+", "-", "*", "/"
#   "left": dict,      # left operand for BINOP
#   "right": dict,     # right operand for BINOP
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate assembly code for an expression.
    
    Dispatches on expr["type"] to handle CONST, VAR, and BINOP expressions.
    Modifies var_offsets in-place for temporary allocations.
    Returns (assembly_code, updated_next_offset).
    """
    expr_type = expr.get("type", "")
    
    if expr_type == "CONST":
        return _generate_const_code(expr, next_offset)
    elif expr_type == "VAR":
        return _generate_var_code(expr, var_offsets, next_offset)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_const_code(expr: Expr, next_offset: int) -> Tuple[str, int]:
    """Generate code to load a constant value onto the stack."""
    value = expr.get("value", 0)
    code = f"    MOV R0, {value}\n    PUSH R0\n"
    return code, next_offset

def _generate_var_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate code to load a variable value from its stack offset."""
    name = expr.get("name", "")
    if name not in var_offsets:
        raise ValueError(f"Undefined variable: {name}")
    offset = var_offsets[name]
    code = f"    MOV R0, [RBP-{offset}]\n    PUSH R0\n"
    return code, next_offset

def _generate_binop_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate code for binary operation: evaluate left, right, then apply op."""
    op = expr.get("op", "")
    left_expr = expr.get("left", {})
    right_expr = expr.get("right", {})
    
    # Generate code for left operand
    left_code, next_offset = generate_expression_code(left_expr, var_offsets, next_offset)
    
    # Store left result in temporary
    temp_offset = next_offset
    var_offsets[f"_temp_{temp_offset}"] = temp_offset
    next_offset += 8
    left_code += f"    POP R0\n    MOV [RBP-{temp_offset}], R0\n"
    
    # Generate code for right operand
    right_code, next_offset = generate_expression_code(right_expr, var_offsets, next_offset)
    
    # Store right result in temporary
    temp_offset2 = next_offset
    var_offsets[f"_temp_{temp_offset2}"] = temp_offset2
    next_offset += 8
    right_code += f"    POP R0\n    MOV [RBP-{temp_offset2}], R0\n"
    
    # Load operands and apply operation
    op_map = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV"
    }
    asm_op = op_map.get(op, op)
    
    result_code = f"    MOV R0, [RBP-{temp_offset2}]\n    MOV R1, [RBP-{temp_offset}]\n    {asm_op} R0, R1\n    PUSH R0\n"
    
    full_code = left_code + right_code + result_code
    return full_code, next_offset

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node