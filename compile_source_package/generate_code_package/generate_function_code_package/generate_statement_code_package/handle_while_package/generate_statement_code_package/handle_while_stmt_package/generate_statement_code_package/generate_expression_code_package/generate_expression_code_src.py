# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._handle_literal_package._handle_literal_src import _handle_literal
from ._handle_variable_package._handle_variable_src import _handle_variable
from ._handle_binary_op_package._handle_binary_op_src import _handle_binary_op
from ._handle_unary_op_package._handle_unary_op_src import _handle_unary_op
from ._handle_call_package._handle_call_src import _handle_call

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,           # "literal", "variable", "binary_op", "unary_op", "call"
#   "value": Any,          # for literal
#   "name": str,           # for variable
#   "operator": str,       # for binary_op/unary_op
#   "left": dict,          # for binary_op
#   "right": dict,         # for binary_op
#   "operand": dict,       # for unary_op
#   "function": str,       # for call
#   "args": list,          # for call
# }

# === main function ===
def generate_expression_code(expr: Expr, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int, int]:
    """Generate assembly code for an expression AST node.
    
    Dispatches based on expr["type"] to appropriate handler.
    Returns: (assembly_code, result_stack_offset, updated_next_offset)
    """
    expr_type = expr.get("type")
    
    if expr_type == "literal":
        return _handle_literal(expr.get("value"), next_offset)
    elif expr_type == "variable":
        return _handle_variable(expr.get("name"), var_offsets, next_offset)
    elif expr_type == "binary_op":
        return _handle_binary_op(
            expr.get("operator"),
            expr.get("left"),
            expr.get("right"),
            var_offsets,
            next_offset
        )
    elif expr_type == "unary_op":
        return _handle_unary_op(
            expr.get("operator"),
            expr.get("operand"),
            var_offsets,
            next_offset
        )
    elif expr_type == "call":
        return _handle_call(
            expr.get("function"),
            expr.get("args"),
            var_offsets,
            next_offset
        )
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed - this is a pure function node