# === std / third-party imports ===
from typing import Any, Dict, Tuple, Callable

# === sub function imports ===
from ._generate_op_code_package._generate_op_code_src import _generate_op_code

# === ADT defines ===
LabelCounter = Dict[str, int]
# LabelCounter possible fields:
# {
#   "if_else": int,
#   "if_end": int,
# }

VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,
# }

Expression = Dict[str, Any]
# Expression possible fields:
# {
#   "type": str,  # "LITERAL" | "IDENTIFIER" | "BINARY_OP" | "CALL"
#   "value": int,  # for LITERAL
#   "name": str,  # for IDENTIFIER
#   "op": str,  # for BINARY_OP
#   "left": Dict,  # for BINARY_OP
#   "right": Dict,  # for BINARY_OP
#   "func_name": str,  # for CALL
#   "args": list,  # for CALL
# }

EvalFunc = Callable[[dict, str, dict, dict, int], Tuple[str, int]]
# EvalFunc possible fields:
# {
#   "callable": function that evaluates an expression and returns (assembly_code, next_offset)
# }


# === main function ===
def _handle_binary_op(
    expr: dict,
    func_name: str,
    label_counter: dict,
    var_offsets: dict,
    next_offset: int,
    eval_func: EvalFunc
) -> Tuple[str, int]:
    """
    Handle BINARY_OP expression type.
    Recursively evaluates left and right operands, generates ARM assembly for the operation.
    Returns Tuple[assembly code string, updated next_offset].
    """
    op = expr["op"]
    left_expr = expr["left"]
    right_expr = expr["right"]
    
    # Evaluate left operand
    left_code, left_offset = eval_func(left_expr, func_name, label_counter, var_offsets, next_offset)
    
    # Save left result (R0) to stack: push onto stack
    stack_save_code = f"    STR R0, [SP, #-4]!\n"
    stack_offset = left_offset + 1  # One 4-byte slot allocated
    
    # Evaluate right operand
    right_code, right_offset = eval_func(right_expr, func_name, label_counter, var_offsets, stack_offset)
    
    # Restore left result to R1: pop from stack
    stack_restore_code = f"    LDR R1, [SP], #4\n"
    final_offset = right_offset - 1  # One slot deallocated
    
    # Generate operation-specific code
    op_code = _generate_op_code(op)
    
    # Combine all code
    combined_code = left_code + stack_save_code + right_code + stack_restore_code + op_code
    
    return (combined_code, final_offset)


# === helper functions ===
# No helper functions - all logic delegated to child


# === OOP compatibility layer ===
# Not needed - this is a helper function node, not a framework entry point
