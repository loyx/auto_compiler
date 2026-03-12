# === std / third-party imports ===
from typing import Dict, Any, Tuple, List

# === sub function imports ===
# Note: generate_expression_code is the parent dispatcher, not a child
# We import it for recursive argument evaluation
from ..generate_expression_code_src import generate_expression_code

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
def _handle_call(function: str, args: list, var_offsets: Dict[str, int], next_offset: int) -> Tuple[str, int, int]:
    """
    Generate assembly code for function call expressions.
    
    Args:
        function: The function name to call
        args: List of argument expression AST nodes (Expr dicts)
        var_offsets: Variable name to stack offset mapping
        next_offset: Current next available stack offset
    
    Returns:
        Tuple of (assembly_code, result_offset, final_next_offset)
        - assembly_code: Generated assembly including argument evaluation and CALL instruction
        - result_offset: Stack offset where the call result is stored
        - final_next_offset: Updated next available stack offset after the call
    """
    assembly_parts: List[str] = []
    first_arg_offset: int = None
    
    # Evaluate each argument left-to-right
    for i, arg_expr in enumerate(args):
        arg_code, arg_offset, next_offset = generate_expression_code(arg_expr, var_offsets, next_offset)
        assembly_parts.append(arg_code)
        if i == 0:
            first_arg_offset = arg_offset
    
    # Determine result offset
    # If there are arguments, result replaces them at the first argument's offset
    # If no arguments, result goes to a new temporary slot
    if len(args) > 0:
        result_offset = first_arg_offset
    else:
        result_offset = next_offset
    
    # Generate CALL instruction
    num_args = len(args)
    call_instruction = f"CALL {function} {num_args}"
    assembly_parts.append(call_instruction)
    
    # Combine all assembly parts
    assembly_code = "\n".join(assembly_parts)
    
    return assembly_code, result_offset, next_offset

# === helper functions ===
# No helper functions needed for this simple implementation

# === OOP compatibility layer ===
# Not needed - this is a pure function node