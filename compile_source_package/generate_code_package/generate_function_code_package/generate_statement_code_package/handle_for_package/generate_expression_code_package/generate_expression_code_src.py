# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
# Note: Using lazy imports to avoid circular dependency
# generate_binary_op_code and generate_call_code need to call generate_expression_code recursively
# so we import them inside the function or use a different approach

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
#   "type": str,  # "LITERAL" | "IDENTIFIER" | "BINARY_OP" | "UNARY_OP" | "CALL"
#   "value": int | bool,
#   "literal_type": str,
#   "name": str,
#   "operator": str,
#   "left": dict,
#   "right": dict,
#   "operand": dict,
#   "callee": str,
#   "args": list,
# }

# === main function ===
def generate_expression_code(expr: ExprDict, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for an expression, leaving result in x0."""
    # Lazy imports to avoid circular dependency
    from .generate_literal_code_package.generate_literal_code_src import generate_literal_code
    from .generate_identifier_code_package.generate_identifier_code_src import generate_identifier_code
    from .generate_binary_op_code_package.generate_binary_op_code_src import generate_binary_op_code
    from .generate_unary_op_code_package.generate_unary_op_code_src import generate_unary_op_code
    from .generate_call_code_package.generate_call_code_src import generate_call_code
    
    expr_type = expr["type"]
    
    if expr_type == "LITERAL":
        return generate_literal_code(expr, next_offset)
    elif expr_type == "IDENTIFIER":
        return generate_identifier_code(expr, var_offsets, next_offset)
    elif expr_type == "BINARY_OP":
        return generate_binary_op_code(expr, func_name, label_counter, var_offsets, next_offset)
    elif expr_type == "UNARY_OP":
        return generate_unary_op_code(expr, var_offsets, next_offset)
    elif expr_type == "CALL":
        return generate_call_code(expr, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node