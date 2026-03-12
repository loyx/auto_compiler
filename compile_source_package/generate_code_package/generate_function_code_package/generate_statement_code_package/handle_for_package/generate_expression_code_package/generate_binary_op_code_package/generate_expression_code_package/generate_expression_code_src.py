# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_binary_op_code_package.generate_binary_op_code_src import generate_binary_op_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "for_cond": int,
#   "for_end": int,
#   "for_update": int,
#   "skip": int,
#   "true": int,
#   "false": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

ExprDict = Dict[str, Any]
# ExprDict possible fields:
# {
#   "type": str,
#   "operator": str,
#   "left": ExprDict,
#   "right": ExprDict,
#   "value": Any,
#   "name": str,
# }


# === main function ===
def generate_expression_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM64 assembly code for any expression type."""
    expr_type = expr.get("type")
    
    if expr_type == "LITERAL":
        return _generate_literal_code(expr, next_offset)
    elif expr_type == "VARIABLE":
        return _generate_variable_code(expr, var_offsets, next_offset)
    elif expr_type == "BINARY_OP":
        return generate_binary_op_code(expr, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unsupported expression type: {expr_type}")


# === helper functions ===
def _generate_literal_code(expr: dict, next_offset: int) -> Tuple[str, int]:
    """Generate code to load a literal value into x0."""
    value = expr.get("value")
    
    if isinstance(value, bool):
        int_value = 1 if value else 0
        code = f"MOV x0, #{int_value}"
    elif isinstance(value, int):
        code = f"MOV x0, #{value}"
    elif isinstance(value, float):
        raise ValueError("Float literals not supported")
    elif isinstance(value, str):
        raise ValueError("String literals not supported")
    else:
        raise ValueError(f"Unsupported literal value type: {type(value)}")
    
    return code, next_offset


def _generate_variable_code(expr: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate code to load a variable from stack into x0."""
    var_name = expr.get("name")
    offset = var_offsets.get(var_name)
    
    if offset is None:
        raise ValueError(f"Unknown variable: {var_name}")
    
    code = f"LDR x0, [sp, #{offset}]"
    return code, next_offset


# === OOP compatibility layer ===
