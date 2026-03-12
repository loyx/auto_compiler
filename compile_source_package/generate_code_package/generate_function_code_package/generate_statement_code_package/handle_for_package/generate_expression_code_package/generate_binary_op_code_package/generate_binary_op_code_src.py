# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from .generate_expression_code_package.generate_expression_code_src import generate_expression_code
from .generate_operator_instruction_package.generate_operator_instruction_src import generate_operator_instruction

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
def generate_binary_op_code(expr: ExprDict, func_name: str, label_counter: LabelCounter, var_offsets: VarOffsets, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for a BINARY_OP expression."""
    operator = expr["operator"]
    left = expr["left"]
    right = expr["right"]
    
    code_lines = []
    
    # Step 1: Generate code for left operand (result in x0)
    left_code, next_offset = generate_expression_code(left, func_name, label_counter, var_offsets, next_offset)
    code_lines.append(left_code)
    
    # Step 2: Push x0 to stack
    code_lines.append("str x0, [sp, #-16]!")
    next_offset += 16
    
    # Step 3: Generate code for right operand (result in x0)
    right_code, next_offset = generate_expression_code(right, func_name, label_counter, var_offsets, next_offset)
    code_lines.append(right_code)
    
    # Step 4: Restore left operand from stack to x1
    code_lines.append("ldr x1, [sp], #16")
    next_offset -= 16
    
    # Step 5: Apply operator-specific ARM instruction
    op_code, next_offset = generate_operator_instruction(operator, func_name, label_counter, next_offset)
    code_lines.append(op_code)
    
    return "\n".join(code_lines), next_offset

# === helper functions ===

# === OOP compatibility layer ===
