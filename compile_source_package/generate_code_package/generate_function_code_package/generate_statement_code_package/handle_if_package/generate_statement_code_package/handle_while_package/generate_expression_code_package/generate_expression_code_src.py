# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# No child functions - this is a leaf node

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name mapped to stack offset
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # e.g., "BINOP", "VAR", "CONST"
#   "operator": str,       # for BINOP: e.g., "+", "-", "==", "<"
#   "left": dict,          # left operand (Expr dict)
#   "right": dict,         # right operand (Expr dict)
#   "value": Any,          # for CONST: the constant value
#   "name": str,           # for VAR: variable name
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """
    Recursively evaluate an expression and generate assembly code.
    
    Args:
        expr: Expression dictionary with type-specific fields
        var_offsets: Variable name to stack offset mapping
        next_offset: Current next available stack offset
    
    Returns:
        Tuple of (assembly_code_string, updated_offset, result_register_name)
    """
    expr_type = expr.get("type")
    
    if expr_type == "CONST":
        return _generate_const_code(expr, next_offset)
    elif expr_type == "VAR":
        return _generate_var_code(expr, var_offsets, next_offset)
    elif expr_type == "BINOP":
        return _generate_binop_code(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
def _generate_const_code(expr: Expr, next_offset: int) -> Tuple[str, int, str]:
    """Generate code to load a constant value into a register."""
    value = expr.get("value")
    result_reg = f"x{next_offset}"
    code = f"    mov {result_reg}, #{value}\n"
    return code, next_offset + 1, result_reg

def _generate_var_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate code to load a variable from stack into a register."""
    var_name = expr.get("name")
    if var_name not in var_offsets:
        raise ValueError(f"Variable '{var_name}' not found in var_offsets")
    offset = var_offsets[var_name]
    result_reg = f"x{next_offset}"
    code = f"    ldr {result_reg}, [sp, #{offset}]\n"
    return code, next_offset + 1, result_reg

def _generate_binop_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, str]:
    """Generate code for binary operations (arithmetic or comparison)."""
    operator = expr.get("operator")
    left_expr = expr.get("left")
    right_expr = expr.get("right")
    
    # Recursively evaluate left operand
    left_code, left_offset, left_reg = generate_expression_code(left_expr, var_offsets, next_offset)
    
    # Recursively evaluate right operand
    right_code, right_offset, right_reg = generate_expression_code(right_expr, var_offsets, left_offset)
    
    # Generate operation code
    result_reg = f"x{right_offset}"
    op_code, final_offset = _emit_operation(operator, left_reg, right_reg, result_reg, right_offset)
    
    total_code = left_code + right_code + op_code
    return total_code, final_offset, result_reg

def _emit_operation(operator: str, left_reg: str, right_reg: str, result_reg: str, next_offset: int) -> Tuple[str, int]:
    """Emit assembly instruction for the given operator."""
    # Comparison operators: result is 1 for true, 0 for false
    comparison_ops = {
        "==": "eq",
        "!=": "ne",
        "<": "lt",
        ">": "gt",
        "<=": "le",
        ">=": "ge",
    }
    
    if operator in comparison_ops:
        condition = comparison_ops[operator]
        code = f"    cmp {left_reg}, {right_reg}\n"
        code += f"    cset {result_reg}, {condition}\n"
        return code, next_offset + 1
    elif operator == "+":
        code = f"    add {result_reg}, {left_reg}, {right_reg}\n"
        return code, next_offset + 1
    elif operator == "-":
        code = f"    sub {result_reg}, {left_reg}, {right_reg}\n"
        return code, next_offset + 1
    elif operator == "*":
        code = f"    mul {result_reg}, {left_reg}, {right_reg}\n"
        return code, next_offset + 1
    elif operator == "/":
        code = f"    sdiv {result_reg}, {left_reg}, {right_reg}\n"
        return code, next_offset + 1
    elif operator == "and":
        code = f"    and {result_reg}, {left_reg}, {right_reg}\n"
        return code, next_offset + 1
    elif operator == "or":
        code = f"    orr {result_reg}, {left_reg}, {right_reg}\n"
        return code, next_offset + 1
    else:
        raise ValueError(f"Unknown operator: {operator}")

# === OOP compatibility layer ===
# Not needed - this is a pure function node