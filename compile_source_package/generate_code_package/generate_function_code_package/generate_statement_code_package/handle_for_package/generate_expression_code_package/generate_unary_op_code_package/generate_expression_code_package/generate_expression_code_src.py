# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_literal_code_package.generate_literal_code_src import generate_literal_code
from .generate_identifier_code_package.generate_identifier_code_src import generate_identifier_code
from .generate_binary_op_code_package.generate_binary_op_code_src import generate_binary_op_code
from .generate_unary_op_code_package.generate_unary_op_code_src import generate_unary_op_code
from .generate_call_code_package.generate_call_code_src import generate_call_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "counter": int,
# }

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,  # "LITERAL" | "IDENTIFIER" | "BINARY_OP" | "UNARY_OP" | "CALL"
#   "value": Any,  # For LITERAL
#   "literal_type": str,  # For LITERAL
#   "name": str,  # For IDENTIFIER
#   "operator": str,  # For BINARY_OP, UNARY_OP
#   "left": Dict,  # For BINARY_OP
#   "right": Dict,  # For BINARY_OP
#   "operand": Dict,  # For UNARY_OP
#   "function": Dict,  # For CALL
#   "arguments": list,  # For CALL
# }

# === main function ===
def generate_expression_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Dispatch expression code generation based on expr['type']."""
    expr_type = expr.get("type", "")
    
    if expr_type == "LITERAL":
        return generate_literal_code(expr, next_offset)
    elif expr_type == "IDENTIFIER":
        return generate_identifier_code(expr, var_offsets, next_offset)
    elif expr_type == "BINARY_OP":
        return generate_binary_op_code(expr, func_name, label_counter, var_offsets, next_offset)
    elif expr_type == "UNARY_OP":
        return generate_unary_op_code(expr, func_name, label_counter, var_offsets, next_offset)
    elif expr_type == "CALL":
        return generate_call_code(expr, func_name, label_counter, var_offsets, next_offset)
    else:
        raise ValueError(f"Unknown expression type: {expr_type}")

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node
