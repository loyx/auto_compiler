# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._get_binary_op_instruction_package._get_binary_op_instruction_src import _get_binary_op_instruction
from ._get_unary_op_instruction_package._get_unary_op_instruction_src import _get_unary_op_instruction

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # variable name to stack offset mapping
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "literal", "variable", "binary_op", "unary_op"
#   "value_type": str,     # "int" or "bool" (for literal type)
#   "value": Any,          # literal value (int)
#   "name": str,           # variable name (for variable type)
#   "op": str,             # operator (for binary_op/unary_op)
#   "left": dict,          # left operand (for binary_op)
#   "right": dict,         # right operand (for binary_op)
#   "operand": dict,       # operand (for unary_op)
# }


# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for expression evaluation.
    
    Result of any expression is always in x0 register.
    Returns tuple of (assembly code string, updated next_offset).
    """
    expr_type = expr["type"]
    
    if expr_type == "literal":
        return _generate_literal(expr, next_offset)
    elif expr_type == "variable":
        return _generate_variable(expr, var_offsets, next_offset)
    elif expr_type == "binary_op":
        return _generate_binary_op(expr, var_offsets, next_offset)
    elif expr_type == "unary_op":
        return _generate_unary_op(expr, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")


# === helper functions ===
def _generate_literal(expr: Expr, next_offset: int) -> Tuple[str, int]:
    """Generate code for literal value."""
    value = expr["value"]
    code = f"mov x0, #{value}\n"
    return code, next_offset


def _generate_variable(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate code for variable access."""
    name = expr["name"]
    if name not in var_offsets:
        raise KeyError(f"Variable '{name}' not found in var_offsets")
    offset = var_offsets[name]
    code = f"ldr x0, [sp, #{offset}]\n"
    return code, next_offset


def _generate_binary_op(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate code for binary operation."""
    op = expr["op"]
    left = expr["left"]
    right = expr["right"]
    
    left_code, next_offset = generate_expression_code(left, var_offsets, next_offset)
    temp_offset = next_offset
    code_parts = [left_code, f"str x0, [sp, #{temp_offset}]\n"]
    next_offset += 8
    
    right_code, next_offset = generate_expression_code(right, var_offsets, next_offset)
    code_parts.append(right_code)
    code_parts.append(f"ldr x1, [sp, #{temp_offset}]\n")
    code_parts.append(_get_binary_op_instruction(op))
    
    return "".join(code_parts), next_offset


def _generate_unary_op(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate code for unary operation."""
    op = expr["op"]
    operand = expr["operand"]
    
    operand_code, next_offset = generate_expression_code(operand, var_offsets, next_offset)
    code_parts = [operand_code, _get_unary_op_instruction(op)]
    
    return "".join(code_parts), next_offset


# === OOP compatibility layer ===
# Not needed for this function node