# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ..generate_expression_code_src import generate_expression_code

# === ADT defines ===
VarOffsets = Dict[str, int]
# VarOffsets possible fields:
# {
#   "var_name": int,  # stack offset from sp for this variable
# }

Expr = Dict[str, Any]
# Expr possible fields:
# {
#   "type": str,       # Expression type: "CALL", "BINOP", "VAR", "CONST"
#   "function": str,   # For CALL: function name to call
#   "arguments": list, # For CALL: list of expression dicts (max 8)
#   "op": str,         # For BINOP: operator (+, -, *, /, %, &, |, ^, <<, >>, ==, !=, <, <=, >, >=)
#   "left": dict,      # For BINOP: left operand expression
#   "right": dict,     # For BINOP: right operand expression
#   "name": str,       # For VAR: variable name
#   "value": int,      # For CONST: constant integer value (64-bit signed)
# }

# === main function ===
def _generate_call_code(expr: dict, func_name: str, var_offsets: dict) -> str:
    """Generate ARM64 assembly code for CALL expressions."""
    # Validate required fields
    if "function" not in expr:
        raise KeyError("CALL expression missing 'function' field")
    if "arguments" not in expr:
        raise KeyError("CALL expression missing 'arguments' field")
    
    arguments = expr["arguments"]
    function_name = expr["function"]
    
    # Validate argument count
    if len(arguments) > 8:
        raise ValueError(f"CALL expression has {len(arguments)} arguments, maximum is 8")
    
    lines = []
    
    # Evaluate each argument left-to-right
    for i, arg in enumerate(arguments):
        # Generate code for this argument (result in x0)
        arg_code = generate_expression_code(arg, func_name, var_offsets)
        lines.append(arg_code)
        
        # If not last argument, save x0 to corresponding register
        if i < len(arguments) - 1:
            if i == 0:
                pass  # x0 stays in x0
            else:
                lines.append(f"    mov x{i}, x0")
    
    # Emit function call
    lines.append(f"    bl {function_name}")
    
    return "\n".join(lines)

# === helper functions ===

# === OOP compatibility layer ===
