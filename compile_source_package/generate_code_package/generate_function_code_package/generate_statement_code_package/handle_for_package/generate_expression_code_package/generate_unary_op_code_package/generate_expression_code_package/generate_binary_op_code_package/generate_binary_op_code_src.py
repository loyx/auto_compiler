# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ..generate_expression_code_src import generate_expression_code

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
#   "type": str,
#   "operator": str,
#   "left": Dict,
#   "right": Dict,
# }

# === main function ===
def generate_binary_op_code(expr: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate ARM assembly code for binary operations."""
    operator = expr["operator"]
    left = expr["left"]
    right = expr["right"]
    code = ""
    
    # Handle short-circuit operators
    if operator == "&&":
        return _generate_logical_and(left, right, func_name, label_counter, var_offsets, next_offset)
    elif operator == "||":
        return _generate_logical_or(left, right, func_name, label_counter, var_offsets, next_offset)
    
    # Standard binary operators: compute left, save to x1, compute right, apply op
    left_code, next_offset = generate_expression_code(left, func_name, label_counter, var_offsets, next_offset)
    code += left_code
    
    code += "MOV x1, x0\n"
    
    right_code, next_offset = generate_expression_code(right, func_name, label_counter, var_offsets, next_offset)
    code += right_code
    
    code += _generate_binary_instruction(operator)
    
    return code, next_offset

# === helper functions ===
def _generate_logical_and(left: dict, right: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate code for && operator with short-circuit."""
    code = ""
    
    left_code, next_offset = generate_expression_code(left, func_name, label_counter, var_offsets, next_offset)
    code += left_code
    
    end_label = f"L_{func_name}_end_{label_counter['counter']}"
    label_counter["counter"] += 1
    
    code += "CMP x0, #0\n"
    code += f"BEQ {end_label}\n"
    
    right_code, next_offset = generate_expression_code(right, func_name, label_counter, var_offsets, next_offset)
    code += right_code
    
    code += f"{end_label}:\n"
    
    return code, next_offset

def _generate_logical_or(left: dict, right: dict, func_name: str, label_counter: dict, var_offsets: dict, next_offset: int) -> Tuple[str, int]:
    """Generate code for || operator with short-circuit."""
    code = ""
    
    left_code, next_offset = generate_expression_code(left, func_name, label_counter, var_offsets, next_offset)
    code += left_code
    
    end_label = f"L_{func_name}_end_{label_counter['counter']}"
    label_counter["counter"] += 1
    
    code += "CMP x0, #0\n"
    code += f"BNE {end_label}\n"
    
    right_code, next_offset = generate_expression_code(right, func_name, label_counter, var_offsets, next_offset)
    code += right_code
    
    code += f"{end_label}:\n"
    
    return code, next_offset

def _generate_binary_instruction(operator: str) -> str:
    """Generate ARM instruction for standard binary operator."""
    op_map = {
        "+": "ADD x0, x1, x0\n",
        "-": "SUB x0, x1, x0\n",
        "*": "MUL x0, x1, x0\n",
        "/": "SDIV x0, x1, x0\n",
        "==": "CMP x1, x0\nCSET x0, EQ\n",
        "!=": "CMP x1, x0\nCSET x0, NE\n",
        "<": "CMP x1, x0\nCSET x0, LT\n",
        ">": "CMP x1, x0\nCSET x0, GT\n",
        "<=": "CMP x1, x0\nCSET x0, LE\n",
        ">=": "CMP x1, x0\nCSET x0, GE\n",
        "&": "AND x0, x1, x0\n",
        "|": "ORR x0, x1, x0\n",
        "^": "EOR x0, x1, x0\n",
        "<<": "LSL x0, x1, x0\n",
        ">>": "ASR x0, x1, x0\n",
    }
    return op_map.get(operator, f"// Unsupported operator: {operator}\n")

# === OOP compatibility layer ===
