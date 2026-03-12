# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ..generate_expression_code_package.generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields for CALL:
# {
#   "type": "CALL",
#   "function": str,     # 被调用函数名
#   "arguments": list,   # 参数列表，每个元素是表达式 dict
# }

# === main function ===
def _generate_call_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generates ARM64 assembly code for function calls."""
    # Validate required fields
    if "function" not in expr:
        raise KeyError("Missing 'function' field in CALL expression")
    if "arguments" not in expr:
        raise KeyError("Missing 'arguments' field in CALL expression")
    
    target_func = expr["function"]
    arguments = expr["arguments"]
    
    # Validate argument count (ARM64 supports x0-x7 for first 8 args)
    if len(arguments) > 8:
        raise ValueError(f"Too many arguments: {len(arguments)}. Maximum 8 supported (x0-x7).")
    
    code_lines = []
    
    # Generate code for each argument
    for i, arg in enumerate(arguments):
        # Generate code for this argument expression (result will be in x0)
        arg_code = generate_expression_code(arg, func_name, var_offsets)
        code_lines.append(arg_code)
        
        # Move result to appropriate register (x0-x7)
        if i > 0:
            # For arguments 1-7, move from x0 to x1-x7
            code_lines.append(f"    mov x{i}, x0")
    
    # Call the function
    code_lines.append(f"    bl {target_func}")
    
    # Return value is already in x0 per ARM64 convention
    return "\n".join(code_lines)

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# Not required for this function node