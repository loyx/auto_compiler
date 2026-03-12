# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._generate_literal_code_package._generate_literal_code_src import _generate_literal_code
from ._generate_variable_code_package._generate_variable_code_src import _generate_variable_code
from ._generate_binary_op_code_package._generate_binary_op_code_src import _generate_binary_op_code
from ._generate_unary_op_code_package._generate_unary_op_code_src import _generate_unary_op_code
from ._generate_call_code_package._generate_call_code_src import _generate_call_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
#   "while_start": int,
#   "while_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,  # "literal", "variable", "binary_op", "unary_op", "call"
#   "value": int,  # for literal
#   "name": str,  # for variable
#   "operator": str,  # for binary_op/unary_op
#   "left": dict,  # for binary_op
#   "right": dict,  # for binary_op
#   "operand": dict,  # for unary_op
#   "name": str,  # for call (function name)
#   "arguments": list,  # for call
# }

# === main function ===
def generate_expression_code(expr: Expr, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for evaluating an expression. Result in R0."""
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        value = expr.get("value")
        asm = _generate_literal_code(value)
        return (asm, next_offset)
    
    elif expr_type == "variable":
        var_name = expr.get("name")
        asm = _generate_variable_code(var_name, var_offsets)
        return (asm, next_offset)
    
    elif expr_type == "binary_op":
        operator = expr.get("operator")
        left = expr.get("left")
        right = expr.get("right")
        return _generate_binary_op_code(operator, left, right, func_name, label_counter, var_offsets, next_offset)
    
    elif expr_type == "unary_op":
        operator = expr.get("operator")
        operand = expr.get("operand")
        return _generate_unary_op_code(operator, operand, func_name, label_counter, var_offsets, next_offset)
    
    elif expr_type == "call":
        call_func_name = expr.get("name")
        arguments = expr.get("arguments", [])
        return _generate_call_code(call_func_name, arguments, func_name, label_counter, var_offsets, next_offset)
    
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# All helper logic delegated to sub-function modules

# === OOP compatibility layer ===
# Not needed for this function node